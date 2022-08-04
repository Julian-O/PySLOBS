"""
    These exercises should (all going well) have no impact on the SLOBS configuration,
    but they should cause dialog boxes to pop up. They should be cancelled to avoid
    changing anything.
"""
import asyncio

from pyslobs import NotificationsService, SourcesService

from ex_notifications import exercise_notifications_services_ui
import formatters as pp


async def show_notification_dialog(conn, delay):
    ns = NotificationsService(conn)
    print("Please note the 'Notifications' dialogue.")
    await ns.show_notifications()
    await asyncio.sleep(delay)


async def show_add_source_dialog(conn, delay):
    ss = SourcesService(conn)
    print("Please note the 'Name source' dialogue.")
    await ss.show_add_source("This doesn't matter?")
    await asyncio.sleep(delay)


async def show_add_showcase_dialog(conn, delay):
    ss = SourcesService(conn)
    print("Please note the 'Select source type' dialogue.")
    await ss.show_showcase()
    await asyncio.sleep(delay)


async def show_source_properties_dialog(conn, delay):
    ss = SourcesService(conn)
    sources = await ss.get_sources()
    first_source = sources[0]
    first_source_id = first_source.source_id
    print("Please cancel the 'properties' dialogue for:")
    print(await pp.str_source_multiline(first_source, ""))
    await ss.show_source_properties(first_source_id)
    await asyncio.sleep(delay)


async def exercise_all_ui(conn, delay=3):
    await show_notification_dialog(conn, delay)
    await show_add_source_dialog(conn, delay)
    await show_add_showcase_dialog(conn, delay)
    await show_source_properties_dialog(conn, delay)
    await exercise_notifications_services_ui(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_all_ui)
