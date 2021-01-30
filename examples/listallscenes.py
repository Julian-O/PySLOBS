import asyncio
import logging
from pprint import pprint

from pyslobs import SlobsConnection, ScenesService
from tests.config import token

async def list_all_scenes(conn):
    print("Available scenes:")
    ss = ScenesService(conn)
    scenes = await ss.get_scenes()
    for scene in scenes:
        print(" - ", scene.name)
    await conn.close()


async def main():
    conn = SlobsConnection(token())
    await asyncio.gather(conn.background_processing(), list_all_scenes(conn))


logging.basicConfig(level=logging.INFO)
asyncio.run(main())
