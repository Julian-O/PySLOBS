from collections import namedtuple
from datetime import datetime
from enum import Enum

_FIELD_MAPS = {
    "life_time": "lifeTime",
    "play_sound": "playSound",
    "show_time": "showTime",
    "subtype": "subType",
}

# Translate from Pythonic dictionary keys to Javascripty ones.
# Only required for dictionaries passed to API by client.
def _translate_dict(raw_dict):
    return dict([(_FIELD_MAPS.get(key, key), value) for key, value in raw_dict.items()])


class NotificationType(Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"


class NotificationSubType(Enum):
    DEFAULT = "DEFAULT"
    DISCONNECTED = "DISCONNECTED"
    DROPPED = "DROPPED"
    LAGGED = "LAGGED"
    SKIPPED = "SKIPPED"


INotificationModel = namedtuple(
    "INotificationModel",
    "action code data date id lifetime message play_sound "
    "show_time  subtype  type  unread",
)
INOTIFICATIONOPTIONS_MANDATORY_FIELDS = {"message"}
INOTIFICATIONOPTIONS_OPTIONAL_FIELDS = {
    "action",
    "code",
    "data",
    "lifeTime",
    "playSound",
    "showTime",
    "subType",
    "type",
    "unread",
}
INOTIFICATIONOPTIONS_FIELDS = (
    INOTIFICATIONOPTIONS_MANDATORY_FIELDS | INOTIFICATIONOPTIONS_OPTIONAL_FIELDS
)
INOTIFICATIONSETTINGS_FIELDS = ["enabled", "playSound"]
INotificationSettings = namedtuple("INotificationSettings", ["enabled", "play_sound"])
IPerformanceState = namedtuple(
    "IPerformanceState",
    "cpu bandwidth frame_rate number_dropped_frames percentage_dropped_frames",
)
ISceneModel = namedtuple("ISceneModel", "id name nodes")
IStreamingState = namedtuple(
    "IStreamingState",
    "recording_status recording_status_time replay_buffer_status "
    "replay_buffer_status_time streaming_status streaming_status_time",
)


def _convert_time(datestr):
    return datetime.strptime(datestr[:-1] + "000Z", "%Y-%m-%dT%H:%M:%S.%f%z")


ITransitionsServiceState = namedtuple("ITransitionsServiceState", "studio_mode")


class MonitoringType(Enum):
    NONE = 0
    MONITORING_ONLY = 1
    MONITORING_AND_OUTPUT = 2


IFader = namedtuple("IFader", "db deflection mul")
IAudioSourceModel = namedtuple(
    "IAudioSourceModel",
    "audio_mixers fader force_mono mixer_hidden monitoring_type muted name "
    "source_id sync_offset",
)


IRectangle = namedtuple("IRectangle", "x y width height")


class TSceneNodeType(Enum):
    FOLDER = "folder"
    ITEM = "item"


ISceneNodeModel = namedtuple(
    "ISceneNodeModel", "children_ids id parent_id scene_id scene_node_type"
)

ISceneNodeAddOptions = namedtuple("ISceneNodeAddOptions", "id source_add_options")

ISourceAddOptions = namedtuple("ISourceAddOptions", "channel is_temporary")

ITransform = namedtuple("ITransform", "crop position rotation scale")

IObsListOption = namedtuple("IObsListOptions", "value description")

# These is unclearly defined.
TObsFormData = str

# This is one of the source types, like browser_source.
# The master list is returned by SourcesServices.getAvailableSourcesTypesList()
TSourceType = str

ISourceModel = namedtuple(
    "ISourceModel",
    [
        "async_",
        "audio",
        "channel",
        "do_not_duplicate",
        "height",
        "id",
        "muted",
        "name",
        "source_id",
        "type_",
        "video",
        "width",
    ],
)

ISceneCollectionsManifestEntry = namedtuple("ISceneCollectionsManifestEntry", "id name")

ISceneCollectionSchema = namedtuple("ISceneCollectionSchema", "id name scenes sources")

ISceneCollectionCreateOptions = namedtuple("ISceneCollectionCreateOptions", "name")

ISelectionModel = namedtuple("ISelectionModel", "last_selected_id selected_ids")
