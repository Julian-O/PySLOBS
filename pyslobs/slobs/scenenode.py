from __future__ import annotations

from .factories import (
    scenenode_factory,
    sceneitem_factory,
    sceneitemfolder_factory,
    scene_factory,
    selection_factory,
    source_factory,
    register,
)
from ..apibase import SlobsClass
from .typedefs import ITransform, TSceneNodeType, ISceneNodeModel


class SceneNode(SlobsClass):
    def __init__(
        self,
        connection,
        resource_id: str,
        source_id: str,
        id_: str,
        node_id: str,
        parent_id: str,
        scene_id: str,
        scene_node_type: TSceneNodeType,
    ):
        super().__init__(connection, resource_id=resource_id, source_id=source_id)

        self._id = id_
        self._node_id = node_id
        self._parent_id = parent_id
        self._scene_id = scene_id
        self._scene_node_type = scene_node_type

    def __str__(self):
        return f"{self.__class__.__name__}({self._resource_id}, {self._id})"

    @property
    def id_(self):
        return self._id

    @property
    def node_id(self):
        return self._node_id

    @property
    def parent_id(self):
        return self._parent_id

    @property
    def scene_id(self):
        return self._scene_id

    @property
    def scene_node_type(self):
        return self._scene_node_type

    async def add_to_selection(self) -> None:
        response = await self._connection.command(
            "addToSelection", self._prepared_params()
        )
        self._check_empty(response)

    async def deselect(self) -> None:
        response = await self._connection.command("deselect", self._prepared_params())
        self._check_empty(response)

    async def detach_parent(self) -> None:
        response = await self._connection.command(
            "detachParent", self._prepared_params()
        )
        self._check_empty(response)

    async def get_item_index(self) -> int:
        response = await self._connection.command(
            "getItemIndex", self._prepared_params()
        )
        return response

    async def get_model(self):  # -> ISceneNodeModel:
        response = await self._connection.command("getModel", self._prepared_params())
        return scenenode_factory(reponse)

    async def get_next_item(self):  # -> ISceneItem:
        response = await self._connection.command(
            "getNextItem", self._prepared_params()
        )
        return sceneitem_factory(response)

    async def get_next_node(self):  # -> ISceneNodeModel:
        response = await self._connection.command(
            "getNextNode", self._prepared_params()
        )
        return scenenode_factory(reponse)

    async def get_node_index(self) -> int:
        response = await self._connection.command(
            "getNodeIndex", self._prepared_params()
        )
        return response

    async def get_parent(self) -> ISceneNodeModel:
        response = await self._connection.command("getParent", self._prepared_params())
        return sceneitemfolder_factory(reponse)

    async def get_path(self) -> str:
        response = await self._connection.command("getPath", self._prepared_params())
        return response

    async def get_prev_item(self):  # -> ISceneItem:
        response = await self._connection.command(
            "getPrevItem", self._prepared_params()
        )
        return sceneitem_factory(response)

    async def get_prev_node(self) -> ISceneNodeModel:
        response = await self._connection.command(
            "getPrevNode", self._prepared_params()
        )
        return scenenode_factory(reponse)

    async def get_scene(self):
        response = await self._connection.command("getScene", self._prepared_params())
        return scene_factory(self._connection, response)

    async def has_parent(self) -> bool:
        response = await self._connection.command("hasParent", self._prepared_params())
        return response

    async def is_folder(self) -> bool:
        response = await self._connection.command("isFolder", self._prepared_params())
        return response

    async def is_item(self):
        response = await self._connection.command("isItem", self._prepared_params())
        return response

    async def is_selected(self) -> bool:
        response = await self._connection.command("isSelected", self._prepared_params())
        return response

    async def place_after(self, node_id) -> None:
        response = await self._connection.command(
            "placeAfter", self._prepared_params([node_id])
        )
        self._check_empty(response)

    async def place_before(self, node_id) -> None:
        response = await self._connection.command(
            "placeBefore", self._prepared_params([node_id])
        )
        self._check_empty(response)

    async def remove(self) -> None:
        response = await self._connection.command("remove", self._prepared_params())
        self._check_empty(response)

    async def select(self) -> None:
        response = await self._connection.command("select", self._prepared_params())
        self._check_empty(response)

    async def setParent(self, parent_id: str) -> None:
        response = await self._connection.command(
            "setParent", self._prepared_params([node_id])
        )
        self._check_empty(response)


class SceneItemFolder(SceneNode):
    def __init__(
        self,
        connection,
        resource_id: str,
        source_id: str,
        id_: str,
        node_id: str,
        parent_id: str,
        scene_id: str,
        scene_node_type: TSceneNodeType,
        name: str,
    ):
        super().__init__(
            connection,
            resource_id,
            source_id,
            id_,
            node_id,
            parent_id,
            scene_id,
            scene_node_type,
        )
        self._name = name

    @property
    def scene_node_type(self):
        return self._scene_node_type

    @property
    def name(self):
        return self._name

    async def add(self, scene_node_id: str):
        response = await self._connection.command(
            "add", self._prepared_params([scene_node_id])
        )
        self._check_empty(response)

    async def get_folders(self) -> list[SceneItemFolder]:
        response = await self._connection.command("getFolders", self._prepared_params())
        return [sceneitemfolder_factory(json_dict) for json_dict in response]

    async def get_items(self) -> list[SceneItem]:
        response = await self._connection.command("getItems", self._prepared_params())
        return [
            sceneitem_factory(self._connection, json_dict) for json_dict in response
        ]

    async def get_nested_nodes(self) -> list[SceneItem]:
        response = await self._connection.command(
            "getNestedNodes", self._prepared_params()
        )
        return [
            scenenode_factory(self._connection, json_dict) for json_dict in response
        ]

    async def get_nodes(self) -> list[SceneItem]:
        response = await self._connection.command("getNodes", self._prepared_params())
        return [
            scenenode_factory(self._connection, json_dict) for json_dict in response
        ]

    async def get_selection(self) -> Selection:
        response = await self._connection.command(
            "getSelection", self._prepared_params()
        )
        return selection_factory(self._connection, json_dict)

    async def set_name(self, parent_id: str):
        response = await self._connection.command(
            "setParent", self._prepared_params([parent_id])
        )
        self._check_empty(response)

    async def ungroup(self):
        response = await self._connection.command("ungroup", self._prepared_params())
        self._check_empty(response)


class SceneItem(SceneNode):
    def __init__(
        self,
        connection,
        resource_id: str,
        source_id: str,
        id_: str,
        node_id: str,
        parent_id: str,
        scene_id: str,
        scene_node_type: TSceneNodeType,
        name: str,
        locked: bool,
        recording_visible: bool,
        scene_item_id: str,
        stream_visible: bool,
        transform: ITransform,
        visible: bool,
    ):
        super().__init__(
            connection,
            resource_id,
            source_id,
            id_,
            node_id,
            parent_id,
            scene_id,
            scene_node_type,
        )

        self._locked = locked
        self._name = name
        self._recording_visible = recording_visible
        self._scene_item_id = scene_item_id
        self._stream_visible = stream_visible
        self._transform = transform
        self._visible = visible

    @property
    def locked(self):
        return self._locked

    @property
    def name(self):
        return self._name

    @property
    def recording_visible(self):
        return self._recording_visible

    @property
    def scene_item_id(self):
        return self._scene_item_id

    @property
    def stream_visible(self):
        return self._stream_visible

    @property
    def transform(self):
        return self._transform

    @property
    def visible(self):
        return self._visible

    async def center_on_screen(self):
        response = await self._connection.command(
            "centerOnScreen", self._prepared_params()
        )
        self._check_empty(response)

    async def fit_to_screen(self):
        response = await self._connection.command(
            "fitToScreen", self._prepared_params()
        )
        self._check_empty(response)

    async def flip_x(self):
        response = await self._connection.command("flipX", self._prepared_params())
        self._check_empty(response)

    async def flip_y(self):
        response = await self._connection.command("flipY", self._prepared_params())
        self._check_empty(response)

    async def get_source(self):
        response = await self._connection.command("getSource", self._prepared_params())
        return source_factory(self._connection, response)

    async def reset_transform(self, deg):
        response = await self._connection.command(
            "resetTransform", self._prepared_params([deg])
        )
        self._check_empty(response)

    async def rotate(self, deg):
        response = await self._connection.command(
            "rotate", self._prepared_params([deg])
        )
        self._check_empty(response)

    async def set_content_crop(self):
        response = await self._connection.command(
            "setContentCrop", self._prepared_params()
        )
        self._check_empty(response)

    async def set_scale(new_scale_model: IVec2, origin: Option[IVec2]) -> None:
        response = await self._connection.command(
            "setScale", self._prepared_params(new_scale_model, origin)
        )
        self._check_empty(response)

    async def set_settings(settings: dict[Any]) -> None:
        response = await self._connection.command(
            "setSettings",
            self._prepared_params(
                [
                    {
                        "locked": settings.get("locked", None),
                        "recording_visible": settings.get("recordingVisible", None),
                        "stream_visible": settings.get("streamVisible", None),
                        "transform": settings.get("transform", None),
                        "visible": settings.get("visible", None),
                    }
                ]
            ),
        )
        self._check_empty(response)

    async def set_transform(self, transform: ITransform):
        response = await self._connection.command(
            "setTransform",
            self._prepared_params(
                [
                    {
                        "crop": transform.crop,
                        "position": transform.position,
                        "rotation": transform.rotation,
                        "scale": transform.scale,
                    }
                ]
            ),
        )
        self._check_empty(response)

    async def set_visibility(self, visible):
        response = await self._connection.command(
            "setVisibility", self._prepared_params([visible])
        )
        self._check_empty(response)

    async def stretch_to_screen(self):
        response = await self._connection.command(
            "stretchToScreen", self._prepared_params()
        )
        self._check_empty(response)


register(SceneNode)
register(SceneItem)
register(SceneItemFolder)
