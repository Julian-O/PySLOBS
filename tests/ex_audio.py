from pyslobs import AudioService, ScenesService
import tests.formatters as pp
from tests.preservers import AudioSourcePreserver


async def list_all_audio_sources(conn):
    print("All Audio Sources:")
    audioservice = AudioService(conn)
    audio_sources = await audioservice.get_sources()
    print(await pp.str_audiosources_multiline(audio_sources, ""))


async def list_current_scene_audio_sources(conn):
    print("Current Scene Audio Sources:")
    audioservice = AudioService(conn)
    audio_sources = await audioservice.get_sources_for_current_scene()
    print(await pp.str_audiosources_multiline(audio_sources, ""))


async def list_first_scenes_audio_sources(conn):
    ss = ScenesService(conn)
    scenes = await ss.get_scenes()
    scene = scenes[0]
    print("Scene", repr(scene.name), "Audio Sources")

    audioservice = AudioService(conn)
    audio_sources = await audioservice.get_sources_for_scene(scene.source_id)
    print(await pp.str_audiosources_multiline(audio_sources, ""))


async def fetch_first_source(conn):
    print("First Source:")
    audioservice = AudioService(conn)
    audio_sources = await audioservice.get_sources()
    first_source_id = audio_sources[0].source_id

    # Now, go and fetch it again
    first_source = await audioservice.get_source(first_source_id)
    print(await pp.str_audiosource_multiline(first_source, ""))


async def manipulate_audio_source(conn):
    # Get an arbitrary audio source
    audioservice = AudioService(conn)
    audio_sources = await audioservice.get_sources()
    audio_source = audio_sources[0]

    async with AudioSourcePreserver(audio_source):
        await audio_source.set_muted(True)
        assert (
            await (await audioservice.get_source(audio_source.source_id)).get_model()
        ).muted

        await audio_source.set_muted(False)
        assert not (
            await (await audioservice.get_source(audio_source.source_id)).get_model()
        ).muted

        print("Deflection result", await audio_source.set_deflection(0))

        print(
            await pp.str_audiosource_multiline(
                await audioservice.get_source(audio_source.source_id), ""
            )
        )
        assert (
            await (await audioservice.get_source(audio_source.source_id)).get_model()
        ).fader.deflection == 0

        await audio_source.set_deflection(1)
        assert (
            await (await audioservice.get_source(audio_source.source_id)).get_model()
        ).fader.deflection == 1


async def exercise_audioservice_ro(conn):

    await list_current_scene_audio_sources(conn)
    await list_first_scenes_audio_sources(conn)
    await list_all_audio_sources(conn)
    await fetch_first_source(conn)


async def exercise_audioservice_rw(conn):

    await manipulate_audio_source(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_audioservice_ro)
