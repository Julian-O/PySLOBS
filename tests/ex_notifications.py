from pyslobs import NotificationsService, NotificationType
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


async def exercise_notifications_services_ro(conn):
    await show_settings(conn)
    await show_single_notification(conn)
    await list_notifications(conn)

if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_notifications_services_ro)

