from ..apibase import SlobsService
from .typedefs import IPerformanceState


class PerformanceService(SlobsService):
    async def get_model(self):
        response = await self._connection.command("getModel", self._prepared_params())
        return IPerformanceState(
            cpu=response["CPU"],
            bandwidth=response["numberDroppedFrames"],
            frame_rate=response["numberDroppedFrames"],
            number_dropped_frames=response["numberDroppedFrames"],
            percentage_dropped_frames=response["percentageDroppedFrames"],
        )
