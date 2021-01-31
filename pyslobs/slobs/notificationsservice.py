from datetime import datetime
from typing import Dict

from ..apibase import SlobsService
from .typedefs import (
    INotificationModel,
    NotificationType,
    INotificationSettings,
    _translate_dict,
    INOTIFICATIONOPTIONS_FIELDS,
    INOTIFICATIONOPTIONS_MANDATORY_FIELDS,
    INOTIFICATIONSETTINGS_FIELDS,
    NotificationSubType,
)


class NotificationsService(SlobsService):
    @staticmethod
    def _inotification_model_factory(json_dict):
        return INotificationModel(
            action=json_dict.get("action", None),
            code=json_dict.get("code", None),
            data=json_dict.get("data", None),
            date=datetime.fromtimestamp(json_dict["date"] / 1000),
            id=json_dict["id"],
            lifetime=json_dict["lifeTime"],
            message=json_dict["message"],
            play_sound=json_dict["playSound"],
            show_time=json_dict["showTime"],
            subtype=NotificationSubType(json_dict["subType"]),
            type=NotificationType(json_dict["type"]),
            unread=json_dict["unread"],
        )

    async def apply_action(self, notification_id):
        response = await self._connection.command(
            "applyAction", self._prepared_params([notification_id])
        )
        self._check_empty(response)

    async def get_all(self, type_: NotificationType):
        response = await self._connection.command(
            "getAll", self._prepared_params([type_.value])
        )
        return [
            self._inotification_model_factory(subitem) for subitem in response
        ]

    async def get_notification(self, id_):
        response = await self._connection.command(
            "getNotification", self._prepared_params([id_])
        )
        return self._inotification_model_factory(response)

    async def get_read(self, type_: NotificationType):
        response = await self._connection.command(
            "getRead", self._prepared_params([type_.value])
        )
        return [
            self._inotification_model_factory(subitem) for subitem in response
        ]

    async def get_settings(self) -> INotificationSettings:
        response = await self._connection.command(
            "getSettings", self._prepared_params()
        )
        return INotificationSettings(
            enabled=response["enabled"], play_sound=response["playSound"]
        )

    async def get_unread(self, type_: NotificationType):
        response = await self._connection.command(
            "getUnread", self._prepared_params([type_.value])
        )
        return [
            self._inotification_model_factory(subitem) for subitem in response
        ]

    async def mark_all_as_read(self):
        response = await self._connection.command(
            "markAllAsRead", self._prepared_params()
        )
        self._check_empty(response)

    async def mark_as_read(self, id_):
        response = await self._connection.command(
            "markAllAsRead", self._prepared_params([id_])
        )
        self._check_empty(response)

    async def push(self, notify_info: Dict):
        translated_dict = _translate_dict(notify_info)
        # notify_info may only contain fields in the INotificationOptions list
        assert set(translated_dict.keys()).issubset(INOTIFICATIONOPTIONS_FIELDS)
        # notify_info must contain mandatory fields
        assert INOTIFICATIONOPTIONS_MANDATORY_FIELDS.issubset(
            set(translated_dict.keys())
        )

        response = await self._connection.command(
            "push", self._prepared_params([translated_dict])
        )
        return self._inotification_model_factory(response)

    async def restore_default_settings(self):
        response = await self._connection.command(
            "restoreDefaultSettings", self._prepared_params()
        )
        self._check_empty(response)

    async def set_settings(self, patch: Dict):
        # patch should be a dictionary containing any subset of the available
        # fields as keys.
        _translated_dict = _translate_dict(patch)
        assert set(_translated_dict.keys()).issubset(set(INOTIFICATIONSETTINGS_FIELDS))
        response = await self._connection.command(
            "setSettings", self._prepared_params([_translated_dict])
        )
        self._check_empty(response)

    async def show_notifications(self):
        response = await self._connection.command(
            "showNotifications", self._prepared_params()
        )
        self._check_empty(response)
