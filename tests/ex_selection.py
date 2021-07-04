import asyncio
from pathlib import Path
from pyslobs import SelectionService, ScenesService, SourcesService

# import formatters as pp
from preservers import TestScene


async def display_status(conn) -> None:
    sts = SelectionService(conn)
    scs = ScenesService(conn)

    print(
        "Selection is in scene: ",
        (await scs.get_scene(await sts.scene_id())).name,
        "(via scene_id)",
    )
    print("Selection is in scene: ", (await sts.get_scene()).name, "(via get_scene)")

    model = await sts.get_model()
    print(f"Currently there are {len(model.selected_ids)} item(s) selected.")


async def direct_selection(conn) -> None:
    sts = SelectionService(conn)
    sos = SourcesService(conn)
    ss = ScenesService(conn)

    path = Path(__file__).parent / "testpattern.jpg"

    async with TestScene(conn) as scene:
        await ss.make_scene_active(scene.source_id)
        new_source = await sos.create_source(
            "test pattern", "image_source", {"file": str(path)}, options=None
        )

        first = await scene.add_source(source_id=new_source.source_id, options=None)
        await scene.add_source(source_id=new_source.source_id, options=None)
        middle = await scene.add_source(source_id=new_source.source_id, options=None)
        await scene.add_source(source_id=new_source.source_id, options=None)
        last = await scene.add_source(source_id=new_source.source_id, options=None)

        # We have 5 entries for test patterns. The last added is selected.
        selected_ids = await sts.get_ids()
        assert len(selected_ids) == 1
        assert first.id_ not in selected_ids
        assert middle.id_ not in selected_ids
        assert last.id_ in selected_ids

        # Select them all
        await sts.select_all()
        selected_ids = await sts.get_ids()
        assert len(selected_ids) == 5
        assert first.id_ in selected_ids
        assert middle.id_ in selected_ids
        assert last.id_ in selected_ids

        # Deselect two.
        await sts.deselect([first.id_, last.id_])
        selected_ids = await sts.get_ids()
        assert first.id_ not in selected_ids
        assert middle.id_ in selected_ids
        assert last.id_ not in selected_ids

        # Repeat the check using is_selected.
        assert await sts.is_selected(middle.id_)
        assert not await sts.is_selected(last.id_)

        # Invert the selection.
        await sts.invert()
        selected_ids = await sts.get_ids()
        assert first.id_ in selected_ids
        assert middle.id_ not in selected_ids
        assert last.id_ in selected_ids

        # Select one more.
        await sts.add([middle.id_])
        selected_ids = await sts.get_ids()
        assert first.id_ in selected_ids
        assert middle.id_ in selected_ids
        assert last.id_ in selected_ids

        # Inspect via get_model
        model = await sts.get_model()
        assert model.last_selected_id == middle.id_
        assert set(model.selected_ids) == set([first.id_, middle.id_, last.id_])
        # Select only one
        await sts.select([middle.id_])
        selected_ids = await sts.get_ids()
        assert first.id_ not in selected_ids
        assert middle.id_ in selected_ids
        assert last.id_ not in selected_ids

        scene_items = await sts.get_items()
        assert len(scene_items) == 1
        assert scene_items[0].id_ == middle.id_

        await sts.reset()
        scene_items = await sts.get_items()
        assert not scene_items


async def exercise_selection_ro(conn):
    await display_status(conn)


async def exercise_selection_rw(conn):
    await direct_selection(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_selection_ro)
    run_exercise(exercise_selection_rw)
