import asyncio
import logging

from pyslobs import SlobsConnection, config_from_ini_else_stdin


async def closing_exercise(conn, exercise):
    await exercise(conn)
    conn.close()


async def connect_and_wait(exercise) -> None:
    conn = SlobsConnection(config_from_ini_else_stdin())
    await asyncio.gather(conn.background_processing(), closing_exercise(conn, exercise))


def run_exercise(exercise):
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_and_wait(exercise))

    # Let's also finish all running tasks:
    try:
        pending = asyncio.all_tasks()
        loop.run_until_complete(asyncio.gather(*pending))
    except RuntimeError:
        # Loop has already completed.
        pass
