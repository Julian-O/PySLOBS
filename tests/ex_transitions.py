import asyncio
from pyslobs import TransitionsService, ProtocolError
import formatters as pp
from preservers import StudioModeDisabled


async def show_studio_mode(conn) -> None:
    ts = TransitionsService(conn)
    state = await ts.get_model()

    print("Current studio mode: ", pp.str_itransitionsservicestate(state))


async def change_studio_mode(conn) -> None:
    async def callback(key, message):
        print("Notification of transition. Studio_mode is now:", message)

    async with StudioModeDisabled(conn):
        ts = TransitionsService(conn)

        async with await ts.studio_mode_changed.subscribe(callback):
            while True:
                try:
                    await ts.enable_studio_mode()
                    break
                except ProtocolError:
                    print("Failed. Will retry")
                    await asyncio.sleep(3)

            print("Mode is now:", await ts.get_model())
            print("---")

            while True:
                try:
                    await ts.disable_studio_mode()
                    break
                except ProtocolError:
                    print("Failed. Will retry")
                    await asyncio.sleep(3)
            print("Mode is now:", await ts.get_model())
            await asyncio.sleep(3)

            print("---")

            await ts.execute_studio_mode_transition()
            print("Transitioned!")
            await asyncio.sleep(2)


async def exercise_transitionservice_ro(conn):
    await show_studio_mode(conn)


async def exercise_transitionservice_rw(conn):
    await change_studio_mode(conn)


if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_transitionservice_rw)
