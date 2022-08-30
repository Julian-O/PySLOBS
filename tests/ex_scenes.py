import asyncio
from pyslobs import ScenesService
import formatters as pp
from preservers import TestScene


async def show_active_scene(conn):
    ss = ScenesService(conn)
    active_scene = await ss.active_scene()
    print("Active Scene")
    print(await pp.str_scene_multiline(active_scene, "", as_tree=True))
    print("------------")
    print("Same Scene, refetched, formatted differently")
    active_scene_2 = await ss.get_scene(active_scene.id_)
    print(await pp.str_scene_multiline(active_scene_2, ""))
    print("------------")
    active_scene_id_3 = await ss.active_scene_id()
    assert active_scene.id_ == active_scene_id_3
    assert active_scene_2.id_ == active_scene_id_3
    print("All Scenes")
    all_scenes = await ss.get_scenes()
    for scene in all_scenes:
        print(await pp.str_scene_multiline(scene, "", show_nodes=False))


async def show_add_delete_scene(conn):
    # This is actually tested by the preserver itself.
    async with TestScene(conn) as ts:
        print("Scene added.")
        await ts.make_active()
        print("Scene made active (via scene).")
        await asyncio.sleep(2)
    print("Scene deleted, old scene made active (via sceneservice)")


async def exercise_scenesservice_ro(conn):
    await show_active_scene(conn)


async def exercise_scenesservice_rw(conn):
    await show_add_delete_scene(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_scenesservice_ro)
