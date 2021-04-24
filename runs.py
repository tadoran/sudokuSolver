from misc.timeKeeper import timeit
# from sovler import Solver
from sovler_np import Solver


def web_single():
    from from_web import get_from_web, matrix_from_web

    f = Solver()
    req = get_from_web(3)
    matrix = matrix_from_web(req)
    f.enter_values(matrix)
    f.solve()


def random_single_test():
    import test_tasks

    f = Solver()
    vals = test_tasks.fv.get_one_random(tag="Currently unsolvable")
    f.enter_values(vals)
    f.solve()


def tests_last():
    import test_tasks

    f = Solver()
    vals = test_tasks.fv.get_all()[-1]
    f.enter_values(vals)
    f.solve()


def tests_all():
    import test_tasks

    vals = test_tasks.fv.get_all()
    for i, puzzle in enumerate(vals):
        print(f"Puzzle #{i}")
        f = Solver()
        f.enter_values(puzzle)
        # f.solve()
        print("-" * 40)


def tests_w_tag_error():
    import test_tasks

    # vals = test_tasks.fv.get_all("Empty")
    vals = test_tasks.fv.get_all("Wrong")
    for i, puzzle in enumerate(vals):
        print(f"Puzzle #{i}")
        f = Solver()
        f.enter_values(puzzle)
        # f.solve()


def web_n_times(k: int = 10):
    from from_web import get_from_web, matrix_from_web

    for i in range(k + 1):
        print(f"Puzzle #{i}")
        f = Solver()
        req = get_from_web(3)
        matrix = matrix_from_web(req)
        f.enter_values(matrix)
        # f.solve()
        print("-" * 40)


def save_fields_from_web():
    from from_web import get_from_web, matrix_from_web
    from unsync import unsync
    import pickle
    import os

    @unsync
    def get_from_web_async():
        req = get_from_web(3)
        matrix = matrix_from_web(req)
        return matrix

    @timeit
    def import_unsynced(count: int):
        matrices = [get_from_web_async() for _ in range(count)]
        results = [task.result() for task in matrices]
        return results

    matrices = import_unsynced(10)
    print(matrices)

    self_path = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(self_path, "misc", "matrices")
    with open(save_path, "wb") as f:
        pickle.dump(matrices, f)


def get_saved_fields_from_web():
    import pickle
    import os

    self_path = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(self_path, "misc", "matrices")
    with open(save_path, "rb") as f:
        matrices = pickle.load(f)

    @timeit
    def run_all():
        for i, matrix in enumerate(matrices):
            print(f"Puzzle #{i}")
            # solver = Solver(print_start_matrix=False, print_solution_matrix=False)
            solver = Solver()
            solver.enter_values(matrix)
            # solver.solve()
            # print(solver.initial_field)
            # print(solver.field)
            print("-" * 40)

    run_all()


def get_norvig_random():
    import random
    import os

    def random_line(afile):
        line = next(afile)
        for num, aline in enumerate(afile, 2):
            if random.randrange(num):
                continue
            line = aline
        return line

    self_path = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(self_path, "misc", "norvig_hard")
    with open(save_path, "r") as f:
        line = random_line(f)

    # print(line)
    solver = Solver()
    solver.enter_from_str(line)
    solver.solve()
    print("-" * 40)


def get_norvig_all():
    import os

    self_path = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(self_path, "misc", "norvig_hard")
    with open(save_path, "r") as f:
        matrices = list(map(str.strip, f.readlines()))

    @timeit
    def run_all():
        for i, matrix in enumerate(matrices):
            print(f"Norvig Puzzle #{i}")
            solver = Solver()
            solver.enter_from_str(matrix)
            solver.solve()
            print("-" * 40)

    run_all()
