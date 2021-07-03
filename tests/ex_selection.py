import asyncio
from pathlib import Path
from pyslobs import SelectionService, ScenesService, SourcesService
#import formatters as pp
from preservers import TestScene


async def display_status(conn) -> None:
    sts = SelectionService(conn)
    scs = ScenesService(conn)

    print("Selection is in scene: ", (await scs.get_scene(await sts.scene_id())).name)

    model = await sts.get_model()
    print(model)

async def select_items(conn) -> None:
    sts = SelectionService(conn)
    sos = SourcesService(conn)
    path = Path(__file__).parent / "testpattern.jpg"

    async with TestScene(conn) as scene:
        new_source = await sos.create_source(
            "test pattern", "image_source", {"file": str(path)}, options=None
        )
        # I want to change the selection scene to this scene, but I can't see how.

        await scene.add_source(source_id=new_source.source_id, options=None)
        await scene.add_source(source_id=new_source.source_id, options=None)
        await sts.select_all()
        await asyncio.sleep(10)
        # await sos.remove_source(new_source.id)

async def change_visibility(conn) -> None:
    sts = SelectionService(conn)
    sos = SourcesService(conn)
    path = Path(__file__).parent / "testpattern.jpg"

    async with TestScene(conn) as scene:
        new_source = await sos.create_source(
            "test pattern", "image_source", {"file": str(path)}, options=None
        )
        # I want to change the selection scene to this scene, but I can't see how.
        print("Please change to scene to see Test scene to see this in action")
        await asyncio.sleep(5)

        await scene.add_source(source_id=new_source.source_id, options=None)
        await scene.add_source(source_id=new_source.source_id, options=None)
        await sts.select_all()
        await !!!
        await asyncio.sleep(10)
        # await sos.remove_source(new_source.id)

async def exercise_selection_ro(conn):
    await display_status(conn)

async def exercise_selection_rw(conn):
    await change_visbility(conn)
    print("Skipping: await select_items(conn)")



if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_selection_rw)


"""
RO
    async def scene_id(self) -> str:
    async def get_model(self) -> ISelectionModel:

UI
    async def add(self, ids: list[str]):  # -> Selection
    async def deselect(self, ids: list[str]):  # -> Selection:
    async def get_inverted(self) -> list[SceneNode]:
    async def get_inverted_ids(self) -> list[str]:
    async def get_last_selected(self) -> SceneNode:
    async def get_last_selected_id(self) -> bool:
    async def invert(self) -> Selection:
    async def is_selected(self, node_id: str) -> bool:
    async def select(self, ids : list[ids]) -> Selection:
    async def select_all(self) -> None:

RW
    async def center_on_screen(self) -> None:
    async def clone(self):  # -> Selection:
    async def copy_to(
    async def fit_to_screen(self) -> None:
    async def flip_x(self) -> None:
    async def flip_y(self) -> None:
    async def move_to(self, scene_id: str, folder_id: Optional[str]) -> None:
    async def place_after(self, scene_node_id: str) -> None:
    async def place_before(self, scene_node_id: str) -> None:
    async def remove(self) -> None:
    async def reset_transform(self) -> None:
    async def rotate(self, deg: int) -> None:
    async def scale(self, scale: IVec2, origin: Optional[IVec2]) -> None:
    async def scale_with_offset(self, scale : IVec2, offset: IVec2) -> None:
    async def set_content_crop(self) -> None:
    async def set_parent(self, folder_id: str) -> None:
    async def set_recording_visible(self, recording_visible : bool) -> None:
    async def set_settings(self, settings: dict) -> None:
    async def set_stream_visible(self, stream_visible : bool) -> None:
    async def set_transform(self, transform : IPartialTransform) -> None:
    async def set_visibility(self, visible: boolean) -> None:
    async def stretch_to_screen(self) -> None:

    async def get_bounding_rect(self) -> IRectangle:
    async def get_folders(self) -> list[str]:
    async def get_ids(self) -> list[str]:
    async def get_items(self) -> list[SceneItem]:
    async def get_root_nodes(self) -> list[SceneNode]:
    async def get_scene(self) -> list[SceneNode]:
    async def get_size(self) -> bool:
    async def get_sources(self) -> list[Sources]:
    async def get_visual_items(self) -> list[SceneItems]:
    async def is_scene_folder(self) -> bool:
    async def is_scene_item(self) -> bool:
    async def reset(self) -> Selection:
    """
