from field2 import *
from from_web import get_from_web, fill_field_from_web

if __name__ == '__main__':
    scenarios = ["tests", "web", "tests_last", "alltests", "errorneous", "web_continious"]
    current_scenario = scenarios[5]

    f = Solver()
    if current_scenario == "tests":
        import test_tasks

        vals = test_tasks.fv.get_one_random(tag="Currently unsolvable")
        f.enter_values(vals)
        f.solve()

    elif current_scenario == "tests_last":
        import test_tasks

        vals = test_tasks.fv.get_all()[-1]
        f.enter_values(vals)
        f.solve()

    elif current_scenario == "web":
        req = get_from_web(3)
        initial_matrix = fill_field_from_web(req)
        f.enter_values(initial_matrix)
        f.solve()

    elif current_scenario == "alltests":
        import test_tasks

        vals = test_tasks.fv.get_all()
        for puzzle in vals:
            f = Solver()
            f.enter_values(puzzle)
            f.solve()
            print("-" * 20)

    elif current_scenario == "errorneous":
        import test_tasks

        # vals = test_tasks.fv.get_all("Empty")
        vals = test_tasks.fv.get_all("Wrong")
        for puzzle in vals:
            f = Solver()
            f.enter_values(puzzle)
            f.solve()

    elif current_scenario == "web_continious":
        for _ in range(10):
            f = Solver()
            req = get_from_web(3)
            initial_matrix = fill_field_from_web(req)
            f.enter_values(initial_matrix)
            f.solve()
