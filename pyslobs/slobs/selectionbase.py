from __future__ import annotations  # Postponed eval of annotations. Fixed in 3.10
from typing import Optional

from .typedefs import IRectangle, ISelectionModel
from .scenenode import SceneNode
from .factories import (
    selection_factory,
    sceneitemfolder_factory,
    sceneitem_factory,
    scenenode_factory,
)

""" SelectionService and Selection share a lot in common.
    A mixin to support both. """


class SelectionBase:
    async def scene_id(self) -> str:
        response = await self._connection.command("sceneId", self._prepared_params())
        return response

    async def add(self, ids: list[str]):  # -> Selection
        response = await self._connection.command(
            "sceneId", self._prepared_params([ids])
        )
        return selection_factory(self._connection, response)

    async def center_on_screen(self) -> None:
        response = await self._connection.command(
            "centerOnScreen", self._prepared_params([])
        )
        self._check_empty(response)

    async def clone(self):  # -> Selection:
        response = await self._connection.command("clone", self._prepared_params())
        return selection_factory(self._connection, response)

    async def copy_to(
        self, scene_id: str, folder_id: Optional[str], duplicate_sources: Optional[bool]
    ) -> None:
        response = await self._connection.command(
            "copyTo", self._prepared_params([scene_id, folder_id, duplicate_sources])
        )
        self._check_empty(response)

    async def deselect(self, ids: list[str]):  # -> Selection:
        response = await self._connection.command(
            "deselect", self._prepared_params([ids])
        )
        return selection_factory(self._connection, response)

    async def fit_to_screen(self) -> None:
        response = await self._connection.command(
            "fitToScreen", self._prepared_params([])
        )
        self._check_empty(response)

    async def flip_x(self) -> None:
        response = await self._connection.command("flipX", self._prepared_params([]))
        self._check_empty(response)

    async def flip_y(self) -> None:
        response = await self._connection.command("flipY", self._prepared_params([]))
        self._check_empty(response)

    async def get_bounding_rect(self) -> IRectangle:
        response = await self._connection.command(
            "getBoundingRect", self._prepared_params([])
        )
        if response:
            return IRectangle(
                x=response["x"],
                y=response["y"],
                width=response["width"],
                height=response["height"],
            )
        else:
            return None

    async def get_folders(self) -> list[str]:
        response = await self._connection.command(
            "getFolders", self._prepared_params([])
        )
        return [
            sceneitemfolder_factory(self._connection, subitem) for subitem in response
        ]

    async def get_ids(self) -> list[str]:
        response = await self._connection.command("getIds", self._prepared_params([]))
        return response

    async def get_inverted(self) -> list[SceneNode]:
        response = await self._connection.command(
            "getInverted", self._prepared_params([])
        )
        return scenenode_factory(self._connection, response)

    async def get_inverted_ids(self) -> list[str]:
        response = await self._connection.command(
            "getInvertedIds", self._prepared_params([])
        )
        return response

    async def get_items(self) -> list[SceneItem]:
        response = await self._connection.command("getItems", self._prepared_params([]))
        return sceneitem_factory(self._connection, response)

    async def getLastSelected(self) -> SceneNode:
        response = await self._connection.command(
            "getLastSelectedId", self._prtepared_params()
        )
        return scenenode_factory(self._connection, response)

    async def get_last_selected_id(self) -> bool:
        response = await self._connection.command(
            "getLastSelectedId", self._prepared_params()
        )
        return response

    async def get_model(self) -> ISelectionModel:
        response = await self._connection.command("getModel", self._prepared_params())
        return ISelectionModel(
            last_selected_id=response.get("lastSelectedId", []),
            selected_ids=response["selectedIds"],
        )

    async def get_root_nodes(self) -> list[SceneNode]:
        response = await self._connection.command(
            "getRootNodes", self._prepared_params()
        )
        return [scenenode_factory(self._connection, subitem) for subitem in response]

    async def get_scene(self) -> list[SceneNode]:
        response = await self._connection.command("getScene", self._prepared_params())
        return scenenode_factory(self._connection, response)

    async def get_size(self) -> bool:
        response = await self._connection.command("getSize", self._prepared_params())
        return response

    async def get_sources(self) -> list[Sources]:
        response = await self._connection.command("getSources", self._prepared_params())
        return [source_factory(self._connection, subitem) for subitem in response]

    async def get_visual_items(self) -> list[SceneItems]:
        response = await self._connection.command(
            "getVisualItems", self._prepared_params()
        )
        return [sceneitem_factory(self._connection, subitem) for subitem in response]

    async def invert(self) -> Selection:
        response = await self._connection.command("invert", self._prepared_params())
        return [scenenode_factory(self._connection, subitem) for subitem in response]

    async def is_scene_folder(self) -> bool:
        response = await self._connection.command(
            "isSceneFolder", self._prepared_params()
        )
        return response

    async def is_scene_item(self) -> bool:
        response = await self._connection.command(
            "isSceneItem", self._prepared_params()
        )
        return response

    async def is_selected(self, node_id: str) -> bool:
        response = await self._connection.command(
            "isSelected", self._prepared_params([node_id])
        )
        return response

    async def move_to(self, scene_id: str, folder_id: Optional[str]) -> None:
        response = await self._connection.command(
            "moveTo", self._prepared_params([scene_id, folder_id])
        )
        self._check_empty(response)

    async def place_after(self, scene_node_id: str) -> None:
        response = await self._connection.command(
            "placeBefore", self._prepared_params([scene_node_id])
        )
        self._check_empty(response)

    async def place_before(self, scene_node_id: str) -> None:
        response = await self._connection.command(
            "placeBefore", self._prepared_params([scene_node_id])
        )
        self._check_empty(response)

    async def remove(self) -> None:
        response = await self._connection.command("remove", self._prepared_params([]))
        self._check_empty(response)

    async def reset(self) -> Selection:
        response = await self._connection.command("reset", self._prepared_params([]))
        return selection_factory(self._connection(), response)

    async def reset_transform(self) -> None:
        response = await self._connection.command(
            "resetTransform", self._prepared_params([])
        )
        self._check_empty(response)

    async def rotate(self, deg: int) -> None:
        response = await self._connection.command(
            "resetTransform", self._prepared_params([deg])
        )
        self._check_empty(response)

    async def scale(self, scale: IVec2, origin: Optional[IVec2]) -> None:
        response = await self._connection.command(
            "resetTransform", self._prepared_params([scale, origin])
        )
        self._check_empty(response)

    async def scale_with_offset(self, scale : IVec2, offset: IVec2) -> None:
        response = await self._connection.command(
            "scaleWithOffset", self._prepared_params([scale, origin])
        )
        self._check_empty(response)

    async def select(self, ids : list[ids]) -> Selection:
        response = await self._connection.command(
            "select", self._prepared_params([ids])
        )
        return [selection_factory(self._connection, subitem) for subitem in response]

    async def select_all(self) -> None:
        response = await self._connection.command(
            "selectAll", self._prepared_params([])
        )
        self._check_empty(response)

    async def set_content_crop(self) -> None:
        response = await self._connection.command(
            "setContentCrop", self._prepared_params([])
        )
        self._check_empty(response)

    async def set_parent(self, folder_id: str) -> None:
        response = await self._connection.command(
            "setParent", self._prepared_params([folder_id])
        )
        self._check_empty(response)

    async def set_recording_visible(self, recording_visible : bool) -> None:
        response = await self._connection.command(
                "setRecordingVisible", self._prepared_params([recording_visible])
                )
        self._check_empty(response)

    async def set_settings(self, settings: dict) -> None:
        response = await self._connection.command(
                "setSettings", self._prepared_params([settings])
                )
        self._check_empty(response)

    async def set_stream_visible(self, stream_visible : bool) -> None:
        response = await self._connection.command(
                "setStreamVisible", self._prepared_params([stream_visible])
                )
        self._check_empty(response)

    async def set_transform(self, transform : IPartialTransform) -> None:
        # The definition of IPartialTransform is a dictionary that may optionally
        # contain:
        #    position (2-tuple)
        #    scale (2-tuple)
        #    crop (a dictionary that may contain top, bottom, left, right mapping to
        #           ints)
        #    rotation
        response = await self._connection.command(
                "setTransform", self._prepared_params([transform])
                )
        self._check_empty(response)

    async def set_visibility(self, visible: boolean) -> None:
        response = await self._connection.command(
            "setVisibility", self._prepared_params([visible])
        )
        self._check_empty(response)

    async def stretch_to_screen(self) -> None:
        response = await self._connection.command(
            "stretchToScreen", self._prepared_params([])
        )
        self._check_empty(response)
