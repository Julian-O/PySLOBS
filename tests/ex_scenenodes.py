import asyncio
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

    async with TestScene(conn) as ts:
        print("Scene added.")
        await ts.make_active()
        print("Scene made active (via scene).")
        folder = await ts.create_folder("test_folder")
        print("Added folder")
        scene_node = await ts.add_source(source.source_id)
        print("Created scene_node from source")
        # Add node to folder.
        await folder.add(scene_node.scene_item_id)

        # Can't figure out how to create a subfolder!
        # subfolder = await ts.create_folder("sub_folder")
        # # Make node for source.
        # print("Before: Subfolder's parent: ", await subfolder.get_parent())
        # await subfolder.set_parent(folder.resource_id)
        # print("Added subfolder to folder")
        # print("After: Subfolder's parent: ", await subfolder.get_parent())

        print("Name before:", folder.name)
        await folder.set_name("Test folder renamed")
        print("Name after:", folder.name)

        # This exercises get_folders and get_items
        print(
            await pp.str_scene_multiline(
                ts, indent="", as_tree=True, folders_first=True
            )
        )

        print("Before scaling", scene_node.transform)
        await scene_node.set_scale(IVec2(1.5, 2.0))
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

        print(
            "Before setting",
            scene_node.locked,
            scene_node.visible,
            scene_node.stream_visible,
        )
        await scene_node.set_settings(
            dict(locked=True, visible=False, stream_visible=False)
        )
        print(
            "After setting - proxy value",
            scene_node.locked,
            scene_node.visible,
            scene_node.stream_visible,
        )
        items = await folder.get_items()
        assert len(items) == 1
        refetched_scene_node = items[0]
        print(
            "After setting - refetched value",
            refetched_scene_node.locked,
            refetched_scene_node.visible,
            refetched_scene_node.stream_visible,
        )

        await asyncio.sleep(2)
    print("Scene deleted, old scene made active (via sceneservice)")

    # Source is implicitly deleted (!)


async def exercise_scenenodes_rw(conn):
    await modify_scene_nodes(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_scenenodes_rw)
