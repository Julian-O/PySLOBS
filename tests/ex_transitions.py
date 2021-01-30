from pyslobs import TransitionsService
import formatters as pp

async def show_studio_mode(conn) -> None:
    ts = TransitionsService(conn)
    state = await ts.get_model()

    print("Current studio mode: ", pp.str_itransitionsservicestate(state))

async def exercise_transitionservice_ro(conn):
    await show_studio_mode(conn)

if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_transitionservice_ro)
