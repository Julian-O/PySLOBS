from typing import Optional

from ..apibase import SlobsService
from .audiosource import AudioSource


class AudioService(SlobsService):
    def _create_audio_source_from_dict(self, json_dict):
        return AudioSource(
            self._connection,
            source_id=json_dict["sourceId"],
            resource_id=json_dict["resourceId"],
        )

    async def get_source(self, source_id) -> Optional[AudioSource]:
        audio_source_dict = await self._connection.command(
            "getSource", self._prepared_params([source_id])
        )
        if not audio_source_dict:
            return None
        return self._create_audio_source_from_dict(audio_source_dict)

    async def get_sources(self) -> list[AudioSource]:
        response = await self._connection.command("getSources", self._prepared_params())
        return [
            self._create_audio_source_from_dict(audio_source_dict)
            for audio_source_dict in response
        ]

    async def get_sources_for_current_scene(self) -> list[AudioSource]:
        response = await self._connection.command(
            "getSourcesForCurrentScene", self._prepared_params()
        )
        return [
            self._create_audio_source_from_dict(audio_source_dict)
            for audio_source_dict in response
        ]

    async def get_sources_for_scene(self, scene_id) -> list[AudioSource]:
        response = await self._connection.command(
            "getSourcesForScene", self._prepared_params([scene_id])
        )
        return [
            self._create_audio_source_from_dict(audio_source_dict)
            for audio_source_dict in response
        ]
