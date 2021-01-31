"""
    When a json dict is received in a reply, we create a Python instance
    equivalent.

    This code should not be used by the client, but it is shared between a
    number of SlobsService and SlobsClasses so it has been grouped together.
"""
from .typedefs import TSceneNodeType

CLASSES = {}

# DependencyInjection to avoid circular dependencies.
def register(cls):
    CLASSES[cls.__name__] = cls


def audiosource_factory(conn, json_dict):
    return CLASSES["AudioSource"](
        conn,
        source_id=json_dict["sourceId"],
        resource_id=json_dict["resourceId"],
    )


def scenenode_factory(connection, json_dict):
    if json_dict["sceneNodeType"] == "item":
        return sceneitem_factory(connection, json_dict)
    else:
        assert json_dict["sceneNodeType"] == "folder"
        return sceneitemfolder_factory(connection, json_dict)


def sceneitem_factory(connection, json_dict):
    return CLASSES["SceneItem"](
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


def sceneitemfolder_factory(connection, json_dict):
    # Found children_ids as part of the dict, but not the spec.
    # Might like to add in if useful to avoid a call.
    return CLASSES["SceneItemFolder"](
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
        scene_node_type=TSceneNodeType(json_dict["sceneNodeType"]),
    )


def source_factory(connection, json_dict):
    return CLASSES["Source"](
        connection,
        # resource_ids are missing after a deletion.
        resource_id=json_dict.get("resourceId", None),
        source_id=json_dict.get("sourceId", None),
        async_=json_dict["async"],
        audio=json_dict["audio"],
        channel=json_dict.get("channel", None),
        configurable=json_dict.get("configurable", None),
        do_not_duplicate=json_dict["doNotDuplicate"],
        height=json_dict["height"],
        id_=json_dict["id"],
        muted=json_dict["muted"],
        name_=json_dict["name"],
        type_=json_dict["type"],
        video=json_dict["video"],
        width=json_dict["width"],
    )


def scene_factory(connection, json_dict):
    return CLASSES["Scene"](
        connection,
        # resource_ids are missing after a deletion.
        resource_id=json_dict.get("resourceId", None),
        source_id=json_dict["id"],
        # Names are sometimes missing. Fill in an empty name.
        name=json_dict.get("name", ""),
        id=json_dict["id"],
        nodes=[
            # Having trouble with these nodes not being gettable. Not sure why.
            scenenode_factory(connection, node)
            for node in json_dict["nodes"]
        ],
    )


def selection_factory(connection, json_dict):
    raise CLASSES["Selection"](
        connection,
        # resource_ids are missing after a deletion.
        resource_id=json_dict.get("resourceId", None),
        source_id=json_dict["id"],
        scene_id=json_dict["sceneId"],
    )
