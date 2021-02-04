from ex_all_ui import exercise_all_ui
from ex_audio import exercise_audioservice_ro, exercise_audioservice_rw
from ex_notifications import exercise_notifications_services_ro
from ex_performance import exercise_performanceservice_ro
from ex_scenes import exercise_scenesservice_ro, exercise_scenesservice_rw
from ex_scenecollections import (
    exercise_scenecollections_ro,
    exercise_scenecollections_rw,
)
from ex_sources import exercise_sourcesservice_ro, exercise_sourcesservice_rw
from ex_streaming import exercise_streaming_ro, exercise_streaming_destructive
from ex_transitions import exercise_transitionservice_ro, exercise_transitionservice_rw
from runexercise import run_exercise


async def exercise_all_ro(conn):
    await exercise_audioservice_ro(conn)
    await exercise_notifications_services_ro(conn)
    await exercise_performanceservice_ro(conn)
    await exercise_scenesservice_ro(conn)
    await exercise_scenecollections_ro(conn)
    await exercise_sourcesservice_ro(conn)
    await exercise_transitionservice_ro(conn)
    await exercise_streaming_ro(conn)


async def exercise_all_rw(conn):
    await exercise_scenecollections_rw(conn)
    await exercise_audioservice_rw(conn)
    await exercise_scenesservice_rw(conn)
    await exercise_sourcesservice_rw(conn)
    await exercise_transitionservice_rw(conn)


async def exercise_all_destructive(conn):
    await exercise_streaming_destructive(conn)


async def exercise_all(conn):
    print("Running UI affecting tests")
    await exercise_all_ui(conn)
    print("Running read-only tests")
    await exercise_all_ro(conn)
    print("Running read-write tests")
    await exercise_all_rw(conn)
    input("Press Enter to run destructive tests. WARNING: Will stream!")
    await exercise_all_destructive(conn)


if __name__ == "__main__":
    run_exercise(exercise_all)
