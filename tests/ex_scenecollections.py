import asyncio
from pyslobs import SceneCollectionsService, ISceneCollectionCreateOptions
import formatters as pp


async def show_active_collection(conn):
    scs = SceneCollectionsService(conn)
    active_collection = await scs.active_collection()
    print("Active Collection")
    print(active_collection)
    print("-------")
    print("Collections")
    for collection in await scs.collections():
        print("Collection:", collection)
    print("-------")
    print("Scene Collections Schema")
    await asyncio.sleep(1)  # Try to avoid overloading server
    schemas = await scs.fetch_scene_collections_schema()
    for schema in schemas:
        print(pp.str_scenecollectionschema_multiline(schema, ""))

    # print(await pp.str_scene_multiline(active_scene, "", as_tree=True))


async def create_load_delete_collection(conn):
    scs = SceneCollectionsService(conn)
    await asyncio.sleep(1)  # Try to avoid overloading server
    original_collection = await scs.active_collection()
    await asyncio.sleep(1)  # Try to avoid overloading server

    # Next command can be too slow.
    conn.TIMEOUT += 15
    sc = await scs.create(ISceneCollectionCreateOptions("SceneCollectionExercise"))
    conn.TIMEOUT -= 15
    await asyncio.sleep(1)  # Try to avoid overloading server
    await scs.rename("SceneCollectionExercise2", sc.id)
    await asyncio.sleep(1)  # Try to avoid overloading server
    await scs.delete(sc.id)
    await asyncio.sleep(1)  # Try to avoid overloading server
    await scs.load(original_collection.id)


async def exercise_scenecollections_ro(conn):
    await show_active_collection(conn)


async def exercise_scenecollections_rw(conn):
    await create_load_delete_collection(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_scenecollections_rw)
