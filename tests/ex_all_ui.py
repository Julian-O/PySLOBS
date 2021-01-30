"""
    These exercises should (all going well) have no impact on the SLOBS configuration,
    but they should cause dialog boxes to pop up. They should be cancelled to avoid
    changing anything.
"""
import asyncio

from pyslobs import NotificationsService, SourcesService


async def show_notification_dialog(conn):
    ns = NotificationsService(conn)
    print("Please note the 'Notifications' dialogue.")
    await ns.show_notifications()
    await asyncio.sleep(5)


async def show_add_source_dialog(conn):
    ss = SourcesService(conn)
    print("Please note the 'Name source' dialogue.")
    await ss.show_add_source("This doesn't matter?")
    await asyncio.sleep(5)


async def show_add_showcase_dialog(conn):
    ss = SourcesService(conn)
    print("Please note the 'Select source type' dialogue.")
    await ss.show_showcase()
    await asyncio.sleep(5)


async def show_source_properties_dialog(conn):
    ss = SourcesService(conn)
    sources = await ss.get_sources()
    first_source = sources[0]
    first_source_id = first_source.source_id
    print("Please cancel the 'properties' dialogue for:")
    # TODO: When str_source_multiline is available, print it here.
    await ss.show_source_properties(first_source_id)


async def show_all_dialogs(conn):
    await show_notification_dialog(conn)
    await show_add_source_dialog(conn)
    await show_add_showcase_dialog(conn)
    await show_source_properties_dialog(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(show_all_dialogs)
