import asyncio
from pathlib import Path
from pyslobs import ScenesService, SourcesService, ISourceAddOptions, IVec2
import formatters as pp
from preservers import TestScene


async def modify_scene_nodes(conn):
    ss = SourcesService(conn)
    source = await ss.create_source(
        name="Exercise Browser Source",
        type_="browser_source",
        settings={"url": "http://twitter.com/PuzzlingOldMan"},
        options=ISourceAddOptions(channel=None, is_temporary=False),
    )
    print("Added source", source)
    path = Path(__file__).parent / "testpattern.jpg"

    source = await ss.create_source(
        "test pattern", "image_source", {"file": str(path)}, options=None
    )

    async with TestScene(conn) as ts:
        print("Scene added.")
        await ts.make_active()
        print("Scene made active (via scene).")
        folder = await ts.create_folder("test_folder")
        print("Added folder")
        scene_node = await ts.add_source(source.source_id)
        print("Created scene_node from source. Here is the default transform:")
        print(scene_node.transform)

        # Make sure that the position is an integer (see Issue #7 in GitHub)
        assert scene_node.transform.position.x == 0

        # Add node to folder.
        await folder.add(scene_node.scene_item_id)

        subfolder = await ts.create_folder("sub_folder")

        # # I cannot figure how to use set_parent()
        # for potential_parameter in (
        #     folder.id_,
        #     folder.resource_id,
        #     folder.node_id,
        #     await folder.get_node_index(),
        #     folder.scene_id,
        #     folder.source_id,
        # ):
        #     print("Before: Subfolder's parent: ", await subfolder.get_parent())
        #     await subfolder.set_parent(potential_parameter)
        #     print("Tried to use", potential_parameter)
        #     print("After: Subfolder's parent: ", await subfolder.get_parent())

        print("Name before:", folder.name)
        await folder.set_name("Test folder renamed")
        print("Name after:", folder.name)
        assert folder.name == "Test folder renamed"

        # This exercises get_folders and get_items
        print(
            await pp.str_scene_multiline(
                ts, indent="", as_tree=True, folders_first=True
            )
        )

        # Exercise scaling
        print("Before scaling", scene_node.transform)
        await scene_node.set_scale(IVec2(0.5, 0.8))
        print("After scaling - proxy value", scene_node.name, scene_node.transform)
        items = await folder.get_items()
        assert len(items) == 1
        refetched_scene_node = items[0]
        print(
            "After scaling - refetched value",
            refetched_scene_node.name,
            refetched_scene_node.transform,
        )
        # Why does the position change? Checked the data being transmitted and it
        # appears to be a bug in StreamLabs.

        print("Wait a moment for the pattern to appear.")
        await asyncio.sleep(5)
        print(
            "Before setting",
            scene_node.locked,
            scene_node.visible,
            scene_node.stream_visible,
        )

        print("Pattern should now disappear from the screen.")
        await scene_node.set_settings(
            dict(locked=True, visible=False, stream_visible=False)
        )
        print(
            "After setting - proxy value",
            scene_node.locked,
            scene_node.visible,
            scene_node.stream_visible,
        )
        await asyncio.sleep(15)

        print("Pattern should now reappear on screen (not in stream though).")
        assert not scene_node.visible
        await scene_node.set_visibility(visible=True)
        assert scene_node.visible
        assert not scene_node.stream_visible

        await asyncio.sleep(5)

        items = await folder.get_items()
        assert len(items) == 1
        refetched_scene_node = items[0]
        print(
            "After setting - refetched value",
            refetched_scene_node.locked,
            refetched_scene_node.visible,
            refetched_scene_node.stream_visible,
        )
        assert refetched_scene_node.locked
        assert refetched_scene_node.visible
        assert not refetched_scene_node.stream_visible

        await asyncio.sleep(2)
    print("Scene deleted, old scene made active (via sceneservice)")

    # Source is implicitly deleted (!)


async def exercise_scenenodes_rw(conn):
    await modify_scene_nodes(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_scenenodes_rw)
