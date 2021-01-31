from ..apibase import SlobsClass
from .typedefs import IFader, IAudioSourceModel, MonitoringType
from .factories import register


class AudioSource(SlobsClass):
    async def get_model(self):
        response = await self._connection.command("getModel", self._prepared_params())
        return IAudioSourceModel(
            audio_mixers=response["audioMixers"],
            fader=IFader(
                db=response["fader"]["db"],
                deflection=response["fader"]["deflection"],
                mul=response["fader"]["mul"],
            ),
            force_mono=response["forceMono"],
            mixer_hidden=response["mixerHidden"],
            monitoring_type=MonitoringType(response["monitoringType"]),
            muted=response["muted"],
            name=response["name"],
            source_id=response["sourceId"],
            sync_offset=response["syncOffset"],
        )

    async def set_deflection(self, deflection):
        # I don't know what legal values are (small integers?), but illegal values
        # are simply ignored.
        response = await self._connection.command(
            "setDeflection", self._prepared_params([deflection])
        )
        self._check_empty(response)

    async def set_muted(self, muted):
        response = await self._connection.command(
            "setMuted", self._prepared_params([muted])
        )
        self._check_empty(response)

# Dependency Injection
register(AudioSource)