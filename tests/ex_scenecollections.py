from pyslobs import SceneCollectionsService
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
    schemas = await scs.fetch_scene_collections_schema()
    for schema in schemas:
        print(pp.str_scenecollectionschema_multiline(schema, ""))

    # print(await pp.str_scene_multiline(active_scene, "", as_tree=True))


async def exercise_scenecollections_ro(conn):
    await show_active_collection(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_scenecollections_ro)
