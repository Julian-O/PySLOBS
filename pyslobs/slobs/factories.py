"""
    When a json dict is received in a reply, we create a Python instance
    equivalent.

    This code should not be used by the client, but it is shared between a
    number of SlobsService and SlobsClasses so it has been grouped together.
"""
from .typedefs import TSceneNodeType, ITransform

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
    # We see inconsistency in choices of API here.
    if isinstance(json_dict["transform"]["position"], list):
        transform_position = {"x": json_dict["transform"]["position"][0],
                              "y": json_dict["transform"]["position"][1]}
    else:
        transform_position = json_dict["transform"]["position"]
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
        transform=ITransform(
            # Not showing full commitment here. Should make these sub-dictionaries
            # into named tuples as well.
            crop=json_dict["transform"]["crop"],
            position=transform_position,
            rotation=json_dict["transform"]["rotation"],
            scale=json_dict["transform"]["scale"]),
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

