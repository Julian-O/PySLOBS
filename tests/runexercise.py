import asyncio
import logging

from pyslobs import SlobsConnection

from .config import token


async def closing_exercise(conn, exercise):
    await exercise(conn)
    await conn.close()


async def connect_and_wait(exercise) -> None:
    conn = SlobsConnection(token())
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
