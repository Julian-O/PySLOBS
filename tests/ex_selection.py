import asyncio
from pathlib import Path
from pyslobs import SelectionService, ScenesService, SourcesService, IVec2, ITransform

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

        # Count them
        assert (await sts.get_size()) == 5

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


async def manipulate_selected(conn) -> None:
    sts = SelectionService(conn)
    sos = SourcesService(conn)
    ss = ScenesService(conn)

    path = Path(__file__).parent / "testpattern.jpg"

    async with TestScene(conn) as scene:
        await ss.make_scene_active(scene.source_id)
        new_source = await sos.create_source(
            "test pattern 2", "image_source", {"file": str(path)}, options=None
        )

        first = await scene.add_source(source_id=new_source.source_id, options=None)
        await sts.select_all()
        print(
            "Bounding rectangle of original test pattern", await sts.get_bounding_rect()
        )
        # Centre it.
        await sts.center_on_screen()
        # Flip it
        await sts.flip_x()
        await sts.flip_y()
        # Enlarge it
        await sts.fit_to_screen()

        # Scale it - no origin
        # Send right code, but doesn't display for unclear reasons.
        # Tried treating as factor and as final size.
        await sts.scale(IVec2(5, 5))
        await sts.scale(IVec2(1, 1), IVec2(2, 2))
        await sts.scale_with_offset(IVec2(10, 10), IVec2(2, 2))
        # Enlarge it
        await sts.stretch_to_screen()
        await sts.reset_transform()
        await sts.rotate(45)
        await sts.set_transform(dict(rotation=12))
        await sts.set_visibility(False)
        await sts.set_visibility(True)
        await sts.set_stream_visible(False)
        await sts.set_stream_visible(True)
        await sts.set_recording_visible(False)
        await sts.set_settings(dict(locked=True))
        await sts.set_settings(dict(locked=False, recordingVisible=True))


async def exercise_selection_ro(conn):
    await display_status(conn)


async def exercise_selection_rw(conn):
    await direct_selection(conn)
    await manipulate_selected(conn)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    from tests.runexercise import run_exercise

    run_exercise(exercise_selection_rw)
