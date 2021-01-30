"""
    Monitor and display the total time spent in each scene.

    Advanced feature left as exercise left for the reader:
        Subscribe to StreamingService.streaming_status_change and only count time
        spent actively streaming.

"""

import asyncio
from collections import defaultdict
import logging
import time

from tests.config import token
from pyslobs import SlobsConnection, SubscriptionPreferences, CLOSED, ScenesService


class SceneTime:
    def __init__(self, connection, completed_event):
        self._started = False
        self._ss = ScenesService(connection)
        self._time_per_scene = None
        self._current_scene_name = None
        self._scene_started = None
        self._completed_event = completed_event

    async def start(self):
        self._time_per_scene = defaultdict(lambda: 0)
        self._scene_started = time.monotonic()
        await self._ss.scene_switched.subscribe(
            self._on_switch,
            SubscriptionPreferences(notify_on_close=True, notify_on_unsubscribe=False),
        )
        self._current_scene_name = (await self._ss.active_scene()).name
        self._started = True
        print("The current scene is:", self._current_scene_name)
        print("Change scenes in StreamLabs OBS to see this example in action.")

    def _dump_stats(self):
        print("Current Scene:", self._current_scene_name)
        print("Time spent per scene:")
        data = self._time_per_scene.items()
        for scene_name, time_in_seconds in sorted(
            data, key=lambda tup: tup[1], reverse=True
        ):
            hours = int(time_in_seconds) // 3600
            minutes = int(time_in_seconds) % 3600 // 60
            seconds = int(time_in_seconds) % 60
            print(f"{hours}h{minutes:02d}m{seconds:02d}s: {scene_name}")
        print("----")

    async def _on_switch(self, key, message):
        if not self._started:
            # Subscription has come very fast - before we finish setting up.
            return

        now = time.monotonic()
        elapsed = now - self._scene_started

        # Could use source_id as key, but using scene name, because it seems appropriate
        # to combine two scenes with the same name, and to separate two scenes if the
        # scene name changes mid-stream
        self._time_per_scene[self._current_scene_name] += elapsed

        if message != CLOSED:
            self._scene_started = now
            self._current_scene_name = message["name"]
        else:
            self._completed_event.set()

        self._dump_stats()


async def scene_time(conn):
    try:
        completed_event = asyncio.Event()
        st = SceneTime(conn, completed_event)
        await st.start()
        await completed_event.wait()
    except Exception:
        logging.exception("Unexpected exception")
    finally:
        await conn.close()


async def main():
    conn = SlobsConnection(token())
    await asyncio.gather(conn.background_processing(), scene_time(conn))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
