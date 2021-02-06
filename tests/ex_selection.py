import asyncio
from pyslobs import SelectionService
#import formatters as pp
#from preservers import StudioModeDisabled, NotStreamingPreserver, TestScene


async def display_status(conn) -> None:
    sts = SelectionService(conn)
    model = await sts.get_model()
    print(model)

async def exercise_selection_ro(conn):
    await display_status(conn)




if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_selection_ro)
