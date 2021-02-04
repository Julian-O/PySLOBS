from ..apibase import SlobsService, Event
from .typedefs import IStreamingState, _convert_time


class StreamingService(SlobsService):
    def __init__(self, connection):
        super().__init__(connection)

        self.recording_status_change = Event(
            connection, "recordingStatusChange", self.__class__.__name__
        )

        self.replay_buffer_status_change = Event(
            connection, "replayBufferStatusChange", self.__class__.__name__
        )
        self.streaming_status_change = Event(
            connection, "streamingStatusChange", self.__class__.__name__
        )

    async def get_model(self):
        response = await self._connection.command("getModel", self._prepared_params())
        return IStreamingState(
            recording_status=response["recordingStatus"],
            recording_status_time=_convert_time(response["recordingStatusTime"]),
            replay_buffer_status=response["replayBufferStatus"],
            replay_buffer_status_time=_convert_time(response["replayBufferStatusTime"]),
            streaming_status=response["streamingStatus"],
            streaming_status_time=_convert_time(response["streamingStatusTime"]),
        )

    async def save_replay(self):
        response = await self._connection.command("saveReplay", self._prepared_params())
        self._check_empty(response)

    async def start_replay_buffer(self):
        response = await self._connection.command(
            "startReplayBuffer", self._prepared_params()
        )
        self._check_empty(response)

    async def stop_replay_buffer(self):
        response = await self._connection.command(
            "stopReplayBuffer", self._prepared_params()
        )
        self._check_empty(response)

    async def toggle_recording(self):
        response = await self._connection.command(
            "toggleRecording", self._prepared_params()
        )
        self._check_empty(response)

    # Warning: According to the API, this may never return?!
    # Warning: If called too quickly, may fail without notice.
    async def toggle_streaming(self):
        response = await self._connection.command(
            "toggleStreaming", self._prepared_params()
        )
        self._check_empty(response)
