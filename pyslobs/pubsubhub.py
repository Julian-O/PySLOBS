"""
    A Publish-Subscribe service.

        - Messages are associated with a key. Only subscribers to that key will receive
          the message.
            - No support for wildcards.
        - Optionally informs subscriber that the queue is being shutdown.
        - Optionally informs subscriber that they have been unsubscribed.
        - Maintain a (limited) buffer of undelivered messages in case a message
          is received before subscriber can subscribe.
        
        Only one asyncio mechanism is supported. Each subscriber must provide a 
        callback_coroutine co-routine.
            - Will be executed in the context of the publisher's loop.
            - Must return fast to prevent stalling the publisher.
            - Callback takes two parameters: key and message.
            - Unsubscribe notifications will have UNSUBSCRIBED as the message.
            - Close notifications will have CLOSED as the key and message.
"""
from __future__ import annotations
import asyncio
from dataclasses import dataclass
import logging
from typing import Any, Callable, Coroutine

LOGGER = logging.getLogger("slobsapi.pubsubhub")


@dataclass(frozen=True)
class SubscriptionPreferences:
    notify_on_unsubscribe: bool = False
    notify_on_close: bool = False

UNSUBSCRIBED = object()
CLOSED = object()

class PubSubHub:

    Callback = Callable[[Any, Any], Coroutine]  # The return value is a coroutine.

    def __init__(self):

        self._subscribers_by_key: dict[
            str, dict[PubSubHub.Callback, SubscriptionPreferences]
        ] = dict()
        # Map from key ->
        #     (dict mapping from callback_coroutine -> SubscriptionPreferences)

        self._undelivered_messages: dict[str, list[any]] = dict()
        # Map from key -> list of messages

    async def subscribe(
        self,
        key: Any,
        callback_coroutine: PubSubHub.Callback,
        subscription_preferences: SubscriptionPreferences = SubscriptionPreferences(),
    ):
        assert asyncio.iscoroutinefunction(callback_coroutine), "Callback must be async"
        if key not in self._subscribers_by_key:
            self._subscribers_by_key[key] = {
                callback_coroutine: subscription_preferences
            }
        else:
            self._subscribers_by_key[key][callback_coroutine] = subscription_preferences

        # If we have any undelivered messages to this key, send them now.

        # Check if response already arrived.
        if key in self._undelivered_messages:
            # Response already arrived!
            LOGGER.debug(
                "Backlog of messages being cleared: %s", self._undelivered_messages[key]
            )
            for message in self._undelivered_messages[key]:
                asyncio.ensure_future(callback_coroutine(key, message))

            del self._undelivered_messages[key]

    async def unsubscribe(self, key: Any, callback_coroutine: Callback):
        if key in self._subscribers_by_key:
            if callback_coroutine in self._subscribers_by_key[key]:
                prefs = self._subscribers_by_key[key][callback_coroutine]
                del self._subscribers_by_key[key][callback_coroutine]
                if not self._subscribers_by_key[key]:
                    del self._subscribers_by_key[key]
                if prefs.notify_on_unsubscribe:
                    asyncio.ensure_future(callback_coroutine(key, UNSUBSCRIBED))

    def has_subscribers(self, key):
        return key in self._subscribers_by_key

    async def publish(self, key: Any, message):
        subscribers = self._subscribers_by_key.get(key, {})

        if not subscribers:
            # Add to undelivered list.
            if key not in self._undelivered_messages:
                self._undelivered_messages[key] = [message]
            elif len(self._undelivered_messages[key]) >= 10:
                LOGGER.warning(
                    "Discarding undelivered message to %s, due to backlog. "
                    "Likely server subscriptions don't match client "
                    "subscriptions.",
                    key,
                )
            else:
                self._undelivered_messages[key].append(message)
        else:
            coroutines = subscribers.keys()
            assert all(
                asyncio.iscoroutinefunction(coroutine) for coroutine in coroutines
            )
            for coroutine in coroutines:
                asyncio.ensure_future(coroutine(key, message))

    async def close(self):
        subscribers_to_notify = [
            callback
            for key in self._subscribers_by_key
            for (callback, prefs) in self._subscribers_by_key[key].items()
            if prefs.notify_on_close
        ]
        for coroutine in subscribers_to_notify:
            asyncio.ensure_future(coroutine(CLOSED, CLOSED))
