from pyslobs import ScenesService
import formatters as pp

async def show_active_scene(conn):
    ss = ScenesService(conn)
    active_scene = await ss.active_scene()
    print("Active Scene")
    print(await pp.str_scene_multiline(active_scene, "", as_tree=True))
    print("------------")
    print("Same Scene, refetched, formatted differently")
    active_scene_2 = await ss.get_scene(active_scene.id)
    print(await pp.str_scene_multiline(active_scene_2, ""))
    print("------------")
    print("All Scenes")
    all_scenes = await ss.get_scenes()
    for scene in all_scenes:
        print(await pp.str_scene_multiline(scene, "", show_nodes=False))


async def exercise_scenesservice_ro(conn):
    await show_active_scene(conn)

if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_scenesservice_ro)
