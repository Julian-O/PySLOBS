import time

from pyslobs import NotificationsService, NotificationType, NotificationSubType
import formatters as pp


async def list_notifications(conn):
    ns = NotificationsService(conn)
    for notif_type in NotificationType:
        print(f"All {notif_type.name} Notifications:")
        notifications = await ns.get_all(notif_type)
        print(pp.str_notificationmodels_multiline(notifications, ""))

        print(f"  Read {notif_type.name} Notifications:")
        notifications = await ns.get_read(notif_type)
        print(pp.str_notificationmodels_multiline(notifications, "  "))

        print(f"  Unread {notif_type.name} Notifications:")
        notifications = await ns.get_unread(notif_type)
        print(pp.str_notificationmodels_multiline(notifications, "  "))


async def show_settings(conn):
    ns = NotificationsService(conn)
    settings = await ns.get_settings()
    print(pp.str_inotificationsettings(settings))


async def change_settings(conn):
    ns = NotificationsService(conn)
    settings_as_found = await ns.get_settings()
    await ns.set_settings(dict(play_sound=False, enabled=False))
    updated_settings = await ns.get_settings()
    assert not updated_settings.play_sound
    assert not updated_settings.enabled
    await ns.set_settings(dict(play_sound=True))
    updated_settings = await ns.get_settings()
    assert updated_settings.play_sound
    assert not updated_settings.enabled

    await ns.restore_default_settings()
    updated_settings = await ns.get_settings()
    print("Default settings: ", pp.str_inotificationsettings(updated_settings))

    await ns.set_settings(settings_as_found._asdict())


async def show_single_notification(conn):
    # Assumes there is at least one WARNING.
    ns = NotificationsService(conn)
    notif_type = NotificationType.WARNING
    notifications = await ns.get_all(notif_type)
    if not notifications:
        print(f"Unable to find a {notif_type.name} notification to display.")
    else:
        first_notification_id = notifications[0].id
        # Fetch it again
        notification = await ns.get_notification(first_notification_id)
        print(f"Single Notification:")

        print(pp.str_notificationmodel_multiline(notification, ""))


async def push_notification_and_mark_read(conn):
    ns = NotificationsService(conn)

    message_text = f"Pushed notification from test code {time.asctime()}"

    print(
        "Expect beep and message text to display at bottom of StreamLabs OBS"
        " with an (i)"
    )

    # Send most basic message
    notify_info = dict(message=message_text)
    sent_notification_details = await ns.push(notify_info)
    print("Response", sent_notification_details)

    notifications = await ns.get_all(sent_notification_details.type)
    assert notifications
    last_notification = notifications[0]
    print("Notifications from search:")
    for notification in notifications:
        print(pp.str_notificationmodel_multiline(notification, ""))

    assert last_notification.message == message_text, (
        last_notification.message,
        message_text,
    )
    print(pp.str_notificationmodel_multiline(last_notification, ""))

    # Send elaborate message

    print(
        "Expect two more messages - no beep and no message text to display at bottom."
        " However they will appear in the Notifications window log"
    )

    notify_info = dict(
        message=message_text,
        action="Take some action!",
        code="This is a code.",
        data="Any data you like.",
        play_sound=False,  # Shhh!
        show_time=False,  # Can't see what difference changing this makes.
        lifetime=10000,  # Can't see what difference changing this makes.
        sub_type=NotificationSubType.DROPPED.name,
        type=NotificationType.WARNING.name,
        unread=False,
    )
    sent_notification_details = await ns.push(notify_info)
    print("Response", sent_notification_details)

    notifications = await ns.get_all(sent_notification_details.type)
    assert notifications
    last_notification = notifications[0]
    assert last_notification.message == message_text, (
        last_notification.message,
        message_text,
    )
    assert not last_notification.play_sound
    assert not last_notification.show_time
    assert last_notification.lifetime == 10000, last_notification.lifetime
    assert last_notification.subtype == NotificationSubType.DROPPED
    assert last_notification.type == NotificationType.WARNING
    assert not last_notification.unread
    assert last_notification.action == "Take some action!"
    assert last_notification.code == "This is a code."
    assert last_notification.data == "Any data you like."

    # Apply the action (which is gibberish text)
    # See no response. Not sure what is supposed to happen here.
    await ns.apply_action(last_notification.id)

    notify_info = dict(message=message_text, play_sound=False)
    sent_notification_details = await ns.push(notify_info)

    # Mark one as read.
    notifications = await ns.get_unread(sent_notification_details.type)
    unread_count = len(notifications)
    await ns.mark_as_read(notifications[0].id)
    notifications = await ns.get_unread(sent_notification_details.type)
    assert len(notifications) == unread_count - 1, (len(notifications), unread_count)

    # Mark all as read.
    await ns.mark_all_as_read()
    notifications = await ns.get_unread(sent_notification_details.type)
    assert len(notifications) == 0


async def exercise_notifications_services_ro(conn):
    await show_settings(conn)
    await show_single_notification(conn)
    await list_notifications(conn)


async def exercise_notifications_services_ui(conn):
    await push_notification_and_mark_read(conn)


async def exercise_notifications_services_rw(conn):
    await change_settings(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_notifications_services_ui)
