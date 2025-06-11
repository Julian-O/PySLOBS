"""
    Issue #20 reports an intermittent warning message that appears when
    the connection is closed.
    This attempt attempts to reproduce it.
"""

import asyncio
import logging
import unittest

from pyslobs import SlobsConnection, config_from_ini_else_stdin, ScenesService


async def repeated_connections():
    print("Starting")
    logging.basicConfig(level=logging.INFO)

    connection_config = config_from_ini_else_stdin()

    for _ in range(40):
        print("Connection...")
        conn = SlobsConnection(connection_config)
        print("   ... opened")
        background_task = asyncio.create_task(conn.background_processing())
        print("   ... active")
        ss = ScenesService(conn)
        await ss.get_scenes()
        print("   ... closing")
        conn.close()
        print("   ... closed")


class StressTestCase(unittest.TestCase):
    def test_repeated_connections(self):
        with self.assertNoLogs("slobsapi._SlobsWebSocket", level="WARNING") as lc:
            asyncio.run(repeated_connections())


def main():
    unittest.main()


if __name__ == "__main__":
    main()
