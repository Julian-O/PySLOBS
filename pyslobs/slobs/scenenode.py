from typing import Optional
from ..apibase import SlobsClass
from .typedefs import ITransform, TSceneNodeType


def create_scene_node_from_dict_INTERNAL(self, json_dict):
    raise NotImplementedError()


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

    # addToSelection
    # deselect
    # detachParent
    # getItemIndex
    # getModel
    # getNextItem
    # getNextNode
    # getNodeIndex
    # getParent
    # getPath
    # getPrevItem
    # getPrevNode
    # getScene
    # hasParent
    # isFolder
    # isItem
    # isSelected
    # placeAfter
    # placeBefore
    # remove
    # select
    # setParent


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
    # getFolders
    # getItems
    # getNestedNodes
    # getNodes
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

        self._name = name
        self._recording_visible = recording_visible
        self._scene_item_id = scene_item_id
        self._stream_visible = stream_visible
        self._transform = transform
        self._visible = visible

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
