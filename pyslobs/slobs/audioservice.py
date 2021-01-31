from typing import Optional

from ..apibase import SlobsService
from .audiosource import AudioSource
from .factories import audiosource_factory


class AudioService(SlobsService):

    async def get_source(self, source_id) -> Optional[AudioSource]:
        response = await self._connection.command(
            "getSource", self._prepared_params([source_id])
        )
        if not response:
            return None
        return audiosource_factory(self._connection, response)

    async def get_sources(self) -> list[AudioSource]:
        response = await self._connection.command("getSources", self._prepared_params())
        return [
            audiosource_factory(self._connection, audio_source_dict)
            for audio_source_dict in response
        ]

    async def get_sources_for_current_scene(self) -> list[AudioSource]:
        response = await self._connection.command(
            "getSourcesForCurrentScene", self._prepared_params()
        )
        return [
            audiosource_factory(self._connection, audio_source_dict)
            for audio_source_dict in response
        ]

    async def get_sources_for_scene(self, scene_id) -> list[AudioSource]:
        response = await self._connection.command(
            "getSourcesForScene", self._prepared_params([scene_id])
        )
        return [
            audiosource_factory(self._connection, audio_source_dict)
            for audio_source_dict in response
        ]
