from ..apibase import SlobsService, Event
from .typedefs import ITransitionsServiceState


class TransitionsService(SlobsService):
    def __init__(self, connection):
        super().__init__(connection)

        self.studio_mode_changed = Event(
            connection, "studioModeChanged", self.__class__.__name__
        )

    async def disable_studio_mode(self):
        # Warning: Intermittently fails with ProtocolError
        response = await self._connection.command(
            "disableStudioMode", self._prepared_params()
        )
        self._check_empty(response)

    async def enable_studio_mode(self):
        # Warning: Intermittently fails with ProtocolError
        response = await self._connection.command(
            "enableStudioMode", self._prepared_params()
        )
        self._check_empty(response)

    async def execute_studio_mode_transition(self):
        response = await self._connection.command(
            "executeStudioModeTransition", self._prepared_params()
        )
        self._check_empty(response)

    async def get_model(self) -> ITransitionsServiceState:
        response = await self._connection.command("getModel", self._prepared_params())
        return ITransitionsServiceState(studio_mode=response["studioMode"])
