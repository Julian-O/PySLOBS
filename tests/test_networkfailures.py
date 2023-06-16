"""
    The Websocket library can raise a number of exceptions due to Network
    failures.

    This test simulates those failures to ensure they are correctly handled.
"""

import asyncio
import logging

from pyslobs import SlobsConnection, config_from_ini_else_stdin, ScenesService
from pyslobs.connection import ProtocolError
from websocket import (
    # WebSocketException,
    WebSocketProtocolException,
    # WebSocketPayloadException,
    WebSocketConnectionClosedException,
    # WebSocketTimeoutException,
    # WebSocketProxyException,
    # WebSocketBadStatusException,
    # WebSocketAddressException,
)


async def trigger_exceptions():
    print("Starting")
    logging.basicConfig(level=logging.INFO)

    connection_config = config_from_ini_else_stdin()

    for triggering_exception in (
        # Try a sample of the most likely events.
        WebSocketConnectionClosedException("Network has caught fire"),
        WebSocketProtocolException("Ping pong net has holes"),
    ):

        def mock_recv():
            raise triggering_exception

        conn = SlobsConnection(connection_config)
        background_task = asyncio.create_task(conn.background_processing())

        await asyncio.sleep(2)

        print("Expecting a warning log message about: ", triggering_exception)
        # Monkey patch the websocket client to raise an exception.
        conn.websocket.socket.recv = mock_recv

        # Do a random commands to trigger a call to recv
        ss = ScenesService(conn)
        try:
            while True:
                print("Sending command.")
                await ss.get_scenes()
        except asyncio.TimeoutError:
            print("Timed out (expected). Giving up.")
        except ProtocolError:
            print("Protocol Error (acceptable). Giving up.")

        # Should shut down cleanly.
        await background_task

        print("Cleanly shut down.")


def main():
    asyncio.run(trigger_exceptions())


if __name__ == "__main__":
    main()
