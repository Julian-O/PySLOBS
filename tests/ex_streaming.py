import asyncio
from pyslobs import StreamingService
import formatters as pp
from preservers import StudioModeDisabled, NotStreamingPreserver, TestScene


async def display_status(conn) -> None:
    sts = StreamingService(conn)
    model = await sts.get_model()
    print(
        f"Streaming: {model.streaming_status}," f" Recording: {model.recording_status}"
    )


async def record_and_stream(conn) -> None:
    # WARNING: If you are logged in to a streaming service, this may broadcast on your
    # stream.
    sts = StreamingService(conn)

    async with NotStreamingPreserver(conn):
        async with StudioModeDisabled(conn):
            async with TestScene(conn):
                await display_status(conn)
                print("Toggle recording")
                await sts.toggle_recording()
                await asyncio.sleep(2)
                await display_status(conn)
                print("Toggle streaming")
                await sts.toggle_streaming()
                await asyncio.sleep(2)
                await display_status(conn)
                print("Toggle recording")
                await sts.toggle_recording()
                await asyncio.sleep(2)
                await display_status(conn)
                print("Toggle streaming")
                await sts.toggle_streaming()
                await asyncio.sleep(2)
                await display_status(conn)


async def exercise_streaming_ro(conn):
    await display_status(conn)


async def exercise_streaming_destructive(conn):
    await record_and_stream(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_streaming_ro)
