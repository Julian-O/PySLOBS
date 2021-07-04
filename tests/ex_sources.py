import asyncio
from pathlib import Path

from pyslobs import SourcesService, ISourceAddOptions
import formatters as pp


async def show_all_sources(conn):
    ss = SourcesService(conn)
    sources = await ss.get_sources()
    print("All Sources")
    for source in sources:
        print(await pp.str_source_multiline(source, ""))


async def show_all_source_types(conn):
    ss = SourcesService(conn)
    print("All Source Types")
    for item in await ss.get_available_sources_types_list():
        print(f"+- {item.value:23s}: {item.description}")


async def add_source(conn):
    ss = SourcesService(conn)
    events = {}

    async def callback(key, value):
        events[key] = events.get(key, 0) + 1

    await ss.source_added.subscribe(callback)
    await ss.source_removed.subscribe(callback)
    await ss.source_updated.subscribe(callback)

    source = await ss.create_source(
        name="Exercise Browser Source",
        type_="browser_source",
        settings={"url": "http://twitter.com/PuzzlingOldMan"},
        # Tested with is_temporary = True, and it wasn't found in search,
        # which presumably is correct.
        options=ISourceAddOptions(channel=None, is_temporary=False),
    )

    print("Created browser source:")
    print(await pp.str_source_multiline(source, ""))

    await asyncio.sleep(0.1)
    assert events == {"SourcesService.sourceAdded": 1}

    # Refetch the same source by name
    for source_3 in await ss.get_sources_by_name(source.name):
        assert source_3.name == source.name
        if source_3.source_id == source.source_id:
            break
    else:
        assert False, "Search by name failed"

    await source.set_name("Exercise Browser Source 2")

    await asyncio.sleep(0.1)
    assert events == {
        "SourcesService.sourceAdded": 1,
        "SourcesService.sourceUpdated": 1,
    }

    # Refetch the same source by id
    source_2 = await ss.get_source(source.id)
    assert source_2.name == "Exercise Browser Source 2"

    await ss.remove_source(source.source_id)
    assert events == {
        "SourcesService.sourceAdded": 1,
        "SourcesService.sourceUpdated": 1,
        "SourcesService.sourceRemoved": 1,
    }

    file_source = await ss.add_file(Path(__file__).parent / "testpattern.jpg")

    print("Created source from file:")
    print(await pp.str_source_multiline(file_source, ""))

    await ss.remove_source(file_source.source_id)
    assert events == {
        "SourcesService.sourceAdded": 2,
        "SourcesService.sourceUpdated": 1,
        "SourcesService.sourceRemoved": 2,
    }


async def exercise_sourcesservice_ro(conn):
    await show_all_sources(conn)
    await show_all_source_types(conn)


async def exercise_sourcesservice_rw(conn):
    await add_source(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_sourcesservice_ro)
