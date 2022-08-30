"""
    Some exercises will make changes to the configuration. These are context
    managers to help ensure that the configuration is returned to its original
    state at the end of the exercise.
"""
from datetime import datetime

from pyslobs import (
    TransitionsService,
    StreamingService,
    ScenesService,
    NotificationsService,
)


class StudioModeDisabled:
    """Context Manager to turn off Studio Mode, but restore it to its original
    state at end.
    """

    def __init__(self, connection):
        self._ts = TransitionsService(connection)
        self._initial_studio_mode = None

    async def __aenter__(self):
        self._initial_studio_mode = (await self._ts.get_model()).studio_mode
        if self._initial_studio_mode:
            print("Initial disable.")
            while True:
                try:
                    await self._ts.disable_studio_mode()
                    break
                except ProtocolError:
                    print("Failed. Will retry")
                    await asyncio.sleep(3)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._initial_studio_mode:
            # Leave how we found it.
            while True:
                try:
                    await self._ts.enable_studio_mode()
                    break
                except ProtocolError:
                    print("Failed. Will retry")
                    await asyncio.sleep(3)


class TestScene:
    """
    Context Manager to turn create a Test Scene with no personal info, and delete
    it at the end.
    """

    def __init__(self, connection):
        self._ss = ScenesService(connection)
        self._initial_scene_id = None
        self._safe_test_scene_id = None

    def id_(self):
        return self._safe_test_scene_id

    async def __aenter__(self):
        self._initial_scene_id = await self._ss.active_scene_id()
        safe_test_scene = await self._ss.create_scene(
            "Safe Test Scene " + datetime.now().isoformat()
        )
        self._safe_test_scene_id = safe_test_scene.source_id
        return safe_test_scene

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._ss.make_scene_active(self._initial_scene_id)

        assert self._safe_test_scene_id
        await self._ss.remove_scene(self._safe_test_scene_id)


class NotStreamingPreserver:
    """
    Context Manager to ensure code doesn't run when streaming and
    doesn't accidentally leave streaming on at the end.
    """

    def __init__(self, connection):
        self._ss = StreamingService(connection)

    async def _is_streaming(self):
        return (await self._ss.get_model()).streaming_status != "offline"

    async def __aenter__(self):
        assert not await self._is_streaming(), "Don't run this code while streaming!"
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if await self._is_streaming():
            print("WARNING: Code left in streaming state. Attempting to stop.")
            await self._ss.toggle_streaming()
            print("Check streaming status")


class NotificationsSettingsPreserver:
    """
    Context Manager to ensure Notifications Settings are returned to their original
    value.
    """

    def __init__(self, connection):
        self._ps = NotificationsService(connection)
        self._initial_settings = None

    async def __aenter__(self):
        self._initial_settings = await self._ps.get_settings()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._ps.set_settings(self._initial_settings._asdict())


class AudioSourcePreserver:
    """
    Context Manager to ensure Audio Source is returned to its original
    value.
    """

    def __init__(self, audio_source):
        self._as = audio_source
        self._initial_settings = None

    async def __aenter__(self):
        settings = await self._as.get_model()
        self._initial_settings = settings.fader.deflection, settings.muted
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._as.set_deflection(self._initial_settings[0])
        await self._as.set_muted(self._initial_settings[1])
