from __future__ import annotations  # Postponed eval of annotations. Fixed in 3.10
from typing import Optional

from .typedefs import IRectangle
from .scenenode import SceneNode

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
        return self._create_selection_from_dict(response)

    async def center_on_screen(self) -> None:
        response = await self._connection.command(
            "centerOnScreen", self._prepared_params([])
        )
        self._check_empty(response)

    async def clone(self):  # -> Selection:
        response = await self._connection.command("clone", self._prepared_params())
        return self._create_selection_from_dict(response)

    async def copy_to(
        self, scene_id: str, folder_id: Optional[str], duplicate_sources: Optional[bool]
    ) -> None:
        response = await self._connection.command(
            "copyTo", self._prepared_params([scene_id, folder_id, duplicate_sources])
        )

    async def deselect(self, ids: list[str]):  # -> Selection:
        response = await self._connection.command(
            "deselect", self._prepared_params([ids])
        )
        return self._create_selection_from_dict(response)

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

    async def get_ids(self) -> list[str]:
        response = await self._connection.command("getIds", self._prepared_params([]))
        return response

    async def get_inverted(self) -> list[SceneNode]:
        response = await self._connection.command(
            "getInverted", self._prepared_params([])
        )
        raise NotImplementedError()
        return []

    async def get_inverted_ids(self) -> list[str]:
        response = await self._connection.command(
            "getInvertedIds", self._prepared_params([])
        )
        return response


#    async def getItems(self) -> list[SceneItem]:
#    async def getLastSelected(self) -> SceneNode:
#    async def getLastSelectedId(self) -> str:
#    async def getModel(self) -> ISelectionModel:
#    async def getRootNodes(self) -> list[SceneNode]:
#    async def getScene(self) -> Scene:
#    async def getSize(self) -> int:
#    async def getSources(self) -> [Sources]
#    async def getVisualItems(self) -> list[SceneItems]:
#    async def invert(self) -> Selection:
#    async def isSceneFolder(self) -> bool:
#    async def isSceneItem(self) -> bool:
#    async def isSelected(self, node_id : str) -> bool:
#    async def moveTo(self, scene_id: str, folder_id: Optional[str]) -> None:
#    async def placeAfter(self, scene_node_id : str) -> None:
#    async def placeBefore(self, scene_node_id : str) -> None:
#    async def remove(self) -> None:
#    async def reset(self) -> Selection:
#    async def resetTransform(self) -> None:
#    async def rotate(self, deg: int) -> None:
#    async def scale(self, scale : IVec2, origin: Optional[IVec2]) -> None:
#    async def scaleWithOffset(self, scale : IVec2, offset: IVec2) -> None:
#    async def select(self, ids : list[ids]) -> Selection:
#    async def selectAll(self) -> Selection:
#    async def setContentCrop(self) -> None:
#    async def setParent(self, folder_id: str) -> None:
#    async def setRecordingVisible(self, recording_visible : bool) -> None:
#    async def setSettings(self, settings: dict) -> None:
#    async def setStreamVisible(self, stream_visible : bool) -> None:
#    async def setTransform(self, transform: IPartialTransform) -> None
#    async def setVisibility(self, visible: boolean) -> None:
#    async def stretchToScreen(self) -> None:
