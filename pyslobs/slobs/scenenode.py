from __future__ import annotations
from typing import Optional
from ..apibase import SlobsClass
from .typedefs import ITransform, TSceneNodeType, ISceneNodeModel


def create_scene_node_from_dict_INTERNAL(connection, json_dict):
    if json_dict["sceneNodeType"] == "item":
        return create_scene_item_from_dict_INTERNAL(connection, json_dict)
    else:
        assert json_dict["sceneNodeType"] == "folder"
        return create_scene_item_folder_from_dict_INTERNAL(connection, json_dict)


def create_scene_item_from_dict_INTERNAL(connection, json_dict):
    return SceneItem(
        connection=connection,
        resource_id=json_dict["resourceId"],
        source_id=json_dict["sourceId"],
        id_=json_dict["id"],
        # Spec says nodeId should be present, but found it wasn't.
        node_id=json_dict.get("nodeId", None),
        parent_id=json_dict["parentId"],
        scene_id=json_dict["sceneId"],
        scene_node_type=TSceneNodeType(json_dict["sceneNodeType"]),
        name=json_dict["name"],
        locked=json_dict["locked"],
        recording_visible=json_dict["recordingVisible"],
        scene_item_id=json_dict["sceneItemId"],
        stream_visible=json_dict["streamVisible"],
        transform="TBD",
        # 'transform': {'position': {'x': 0, 'y': 0}, 'scale': {'x': 1, 'y': 1},
        #               'crop': {'top': 0, 'bottom': 0, 'left': 0, 'right': 0},
        #               'rotation': 0},
        visible=json_dict["visible"],
    )

def create_scene_item_folder_from_dict_INTERNAL(connection, json_dict):
    # Found children_ids as part of the dict, but not the spec.
    # Might like to add in if useful to avoid a call.
    return SceneItemFolder(
        connection=connection,
        # resourceId/sourceId oddly not part of the returned dict.
        # fall back to id? Doesn't seem to work.
        resource_id=json_dict.get("resourceId", json_dict["id"]),
        source_id=json_dict.get("sourceId"),
        id_=json_dict["id"],
        name=json_dict["name"],
        # Spec says nodeId should be present, but found it wasn't.
        node_id=json_dict.get("nodeId", None),
        parent_id=json_dict["parentId"],
        scene_id=json_dict["sceneId"],
        scene_node_type=TSceneNodeType(json_dict["sceneNodeType"]))

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
        return create_scene_node_from_dict_INTERNAL(reponse)

    async def get_next_item(self):  # -> ISceneItem:
        response = await self._connection.command(
            "getNextItem", self._prepared_params()
        )
        return create_scene_item_from_dict_INTERNAL(response)

    async def get_next_node(self):  # -> ISceneNodeModel:
        response = await self._connection.command(
            "getNextNode", self._prepared_params()
        )
        return create_scene_node_from_dict_INTERNAL(reponse)

    async def get_node_index(self) -> int:
        response = await self._connection.command(
            "getNodeIndex", self._prepared_params()
        )
        return response

    async def get_parent(self) -> ISceneNodeModel:
        response = await self._connection.command("getParent", self._prepared_params())
        return create_scene_item_folder_from_dict_INTERNAL(reponse)

    async def get_path(self) -> str:
        response = await self._connection.command("getPath", self._prepared_params())
        return response

    async def get_prev_item(self):  # -> ISceneItem:
        response = await self._connection.command(
            "getPrevItem", self._prepared_params()
        )
        return create_scene_item_from_dict_INTERNAL(response)

    async def get_prev_node(self) -> ISceneNodeModel:
        response = await self._connection.command(
            "getPrevNode", self._prepared_params()
        )
        return create_scene_node_from_dict_INTERNAL(reponse)

    async def get_scene(self):
        response = await self._connection.command("getScene", self._prepared_params())
        return create_scene_from_dict(reponse)  # Implemented where?

    async def has_parent(self) -> bool:
        response = await self._connection.command("hasParent", self._prepared_params())
        return response

    async def is_folder(self) -> bool:
        response = await self._connection.command("isFolder", self._prepared_params())
        return response

    async def is_item(self):
        response = await self._connection.command("isItem", self._prepared_params())
        print("What does this return? It says *this*, but expect *bool*", response)
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

    # add
    async def get_folders(self) -> list[SceneItemFolder]:
        response = await self._connection.command("getFolders", self._prepared_params())
        return [
            create_scene_item_folder_from_dict_INTERNAL(json_dict)
            for json_dict in response]

    async def get_items(self) -> list[SceneItem]:
        response = await self._connection.command("getItems", self._prepared_params())
        return [
            create_scene_item_from_dict_INTERNAL(self._connection, json_dict)
            for json_dict in response]

    async def get_nested_nodes(self) -> list[SceneItem]:
        response = await self._connection.command("getNestedNodes", self._prepared_params())
        return [
            create_scene_node_from_dict_INTERNAL(self._connection, json_dict)
            for json_dict in response]

    async def get_nodes(self) -> list[SceneItem]:
        response = await self._connection.command("getNodes", self._prepared_params())
        return [
            create_scene_node_from_dict_INTERNAL(self._connection, json_dict)
            for json_dict in response]

    # getSelection
    # setName
    # ungroup


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
    def name(self):
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

    # centerOnScreen
    # fitToScreen
    # flipX
    # flipY
    # getSource
    # resetTransform
    # rotate
    # setContentCrop
    # setScale
    # setSettings
    # setTransform
    # setVisibility
    # stretchToScreen
