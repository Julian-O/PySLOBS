from pyslobs import PerformanceService
import formatters as pp

async def show_performance(conn):
    ps = PerformanceService(conn)
    state = await ps.get_model()
    print("Current performance statistics")
    print(pp.str_iperformancestate(state))

async def exercise_performanceservice_ro(conn):
    await show_performance(conn)

if __name__ == "__main__":
    from tests.runexercise import run_exercise

    run_exercise(exercise_performanceservice_ro)
