import asyncio
from collections import defaultdict
import json
import logging
import time
from typing import Any

from websocket import create_connection, WebSocketTimeoutException

from .pubsubhub import PubSubHub, SubscriptionPreferences


class AuthenticationFailure(Exception):
    pass


class ProtocolError(Exception):
    pass


class _SlobsWebSocket:

    """
    _SlobsWebSocket is a class internal to the API. It is not used by
    a client.

    It is responsible for:
        Maintaining the websocket instance.
        Authentication.
        Sending and receiving low_level messages.
        Formatting a JSONRPC message.

    It does NOT use asyncio.
    """

    logger = logging.getLogger("slobsapi._SlobsWebSocket")

    def __init__(self, token, domain="localhost", port=59650, on_close=None):
        self.url = f"ws://{domain}:{port}/api/websocket"
        self.token = token
        self._on_close = on_close
        try:
            self.socket = create_connection(self.url, timeout=20)
        except ConnectionRefusedError as e:
            raise ProtocolError("Couldn't connect. Is StreamLabs OBS running? %s" % e)
        self._authenticate()

    def is_alive(self) -> bool:
        return bool(self.socket)

    def send_message(self, id_, method, params) -> None:
        message_json = json.dumps(self._build_params_dict(id_, method, params))
        self.logger.debug("Sending:  %s", message_json)
        self.socket.send(message_json)

    def receive_message(self):
        while self.socket:
            try:
                raw_message = self.socket.recv()
                self.logger.debug("Received: %s", raw_message)
                if not raw_message:
                    break
                else:
                    try:
                        result = json.loads(raw_message)
                    except json.JSONDecodeError as json_error:
                        raise ProtocolError("%s from %s" % (json_error, raw_message))
                    except TypeError as type_error:
                        raise ProtocolError(type_error)
                    return result
            except WebSocketTimeoutException:
                self.logger.debug("Retrying after timeout.")
            except OSError as e:
                self.logger.warning(
                    "OSError received. Probably socket was closed. Retrying: %s", e
                )
                time.sleep(1)  # To prevent busy-loop
        self.close()
        return None

    def close(self) -> None:
        if self.socket:
            self.socket.close()
            self.socket = None
            if self._on_close:
                self._on_close()

    def _authenticate(self) -> None:
        message_id = "auth_request"
        self.send_message(
            id_=message_id,
            method="auth",
            params=dict(resource="TcpServerService", args=[self.token]),
        )
        response = self.receive_message()

        if response["id"] != message_id:
            raise ProtocolError("Response id mismatch: %s" % response)
        if "result" not in response or response["result"] is not True:
            raise AuthenticationFailure("%s" % response)

    @staticmethod
    def _build_params_dict(id_, method, params):
        request = {"jsonrpc": "2.0", "id": id_, "method": method, "params": params}
        return request


# noinspection PyBroadException
class SlobsConnection:
    """
    SlobsConnection is responsible for:
        Maintaining a SlobsWebsocket
        Assigning unique message ids to messages.
        Allowing users to subscribe to
            single replies
            ongoing resources
        Actively receiving responses
        Some sort of quit.
        Handling the transition from sync to async.
    """

    logger = logging.getLogger("slobsapi.SlobsConnection")

    def __init__(self, token, domain="localhost", port=59650):
        self.websocket = _SlobsWebSocket(token, domain, port, on_close=None)

        self._response_listeners = dict()
        self._event_listeners = defaultdict(lambda: set())
        self._undelivered_response = dict()
        self._undelivered_events = dict()
        self.hub = PubSubHub()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    def is_alive(self):
        return bool(self.websocket) and self.websocket.is_alive()

    async def _send(self, method, params):
        """
        Send message (in separate thread, so blocking doesn't hold up other
        coroutines) and wait for it to be sent.
        Returns the message_id used.
        """
        message_id = _message_id_factory.next()
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            lambda: self.websocket.send_message(message_id, method, params),
        )
        return message_id

    async def _receive_message(self):
        """
        Wait for received message (in separate thread).
        """
        if self.websocket:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self.websocket.receive_message)

    async def _receive_and_dispatch(self):
        """
        Keep receiving messages and passing them on to the relevant queue
        for the consumers to pick up.

        This needs to be awaited to keep messages pumping.
        """
        try:
            while self.websocket and self.websocket.is_alive():
                try:
                    message = await self._receive_message()

                    if message:
                        if "id" in message and message["id"] is not None:
                            # This is a response to an explicit request.
                            key = message["id"]
                            await self.hub.publish(key=key, message=message)
                        else:
                            # This is a response to an subscription.
                            key = message["result"]["resourceId"]
                            data = message["result"].get("data", None)

                            await self.hub.publish(key=key, message=data)
                except AttributeError:
                    if not self.hub:
                        # Connection was closed mid-receive.
                        break
                    raise
        except Exception:
            self.logger.exception("_receive_and_dispatch failing.")
            raise

        await self.close()

    # Give a nicer name for clients that don't need the details.
    background_processing = _receive_and_dispatch

    async def command(self, method, params):
        """
        Send a command that expects a response.
        Wait for result. If the result returns a promise, wait for the promise.
        """
        self.logger.debug("Command being sent: %s(%s)", method, params)
        message_id = await self._send(method, params)
        final_response_queue = asyncio.Queue()  # Callback will push the response here.

        async def callback(key, value):
            try:
                await self._command_accept_result_of_promise(
                    key, value, final_response_queue
                )
            except Exception:
                self.logger.exception("command.callback has failed!")

        assert asyncio.iscoroutinefunction(callback)
        await self.hub.subscribe(key=message_id, callback_coroutine=callback)
        response = await final_response_queue.get()
        await self.hub.unsubscribe(key=message_id, callback_coroutine=callback)

        if isinstance(response, Exception):
            raise response
        else:
            return response

    async def _command_accept_result_of_promise(self, _, response, queue):
        try:
            if "error" in response:
                await queue.put(ProtocolError(response["error"]))
                return

            if "result" not in response:
                await queue.put(ProtocolError("No result found: %s" % response))
                return

            result = response["result"] or {}

            if isinstance(result, dict) and result.get("emitter", "NA") == "PROMISE":
                # Server is informing that the result may be some time.
                # It will come as an event.
                key = result["resourceId"]
                response_as_event_queue = asyncio.Queue()

                async def callback(k, v):
                    try:
                        await self._command_accept_event_as_response(
                            k, v, response_as_event_queue
                        )
                    except Exception:
                        self.logger.exception(
                            "_command_accept_result_of_promise.callback has failed!"
                        )

                await self.hub.subscribe(key, callback)
                response = await response_as_event_queue.get()
                await self.hub.unsubscribe(key, callback)
                await queue.put(response)
            else:
                await queue.put(result)
        except Exception:
            self.logger.exception("_command_accept_result_of_promise has failed!")

    @staticmethod
    async def _command_accept_event_as_response(_, response, queue) -> None:
        try:
            await queue.put(response)
        except Exception:
            self.logger.exception("_command_accept_event_as_response has failed!")

    async def subscribe(
        self,
        method,
        params,
        callback_coroutine,
        subscription_preferences=SubscriptionPreferences(),
    ) -> Any:
        """
        Send a command that subscribes to events.
        Wait for result. The result should include resource_id.
        Return the resource_id, and continue to have callback_coroutine called as the
        events trigger.
        """

        # Command may be unnecessary if there is already a subscription, but we don't
        # know the resource_id here until we ask.
        response = await self.command(method, params)
        if not "_type" in response or response["_type"] != "SUBSCRIPTION":
            raise ProtocolError("Badly formed subscription response: %s" % response)
        try:
            resource_id = response["resourceId"]
        except KeyError:
            raise ProtocolError("Badly formed subscription response: %s" % response)

        await self.hub.subscribe(
            key=resource_id,
            callback_coroutine=callback_coroutine,
            subscription_preferences=subscription_preferences,
        )
        return resource_id

    async def unsubscribe(self, resource_id, callback_coroutine) -> None:
        """
        Send a command that unsubscribes to events (resource should be provided
        in params dict).
        Also, unhook callback_coroutine from hub.
        """

        await self.hub.unsubscribe(
            key=resource_id, callback_coroutine=callback_coroutine
        )
        # Only tell server if no-one else is interested.
        if not self.hub.has_subscribers(resource_id):
            response = await self.command("unsubscribe", {"resource": resource_id})
            if not response:
                raise ProtocolError("Unsubscribe failed.")

    async def close(self):
        self.logger.debug("Request to close connection.")
        if self.websocket:
            socket_to_close = self.websocket
            self.websocket = None  # So we don't recurse.
            socket_to_close.close()

        if self.hub:
            await self.hub.close()
            self.hub = None


class _MessageIdFactory:
    def __init__(self):
        self._message_id = 0

    def next(self):
        self._message_id += 1
        return self._message_id


_message_id_factory = _MessageIdFactory()
