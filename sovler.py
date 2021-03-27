from collections import OrderedDict
from itertools import count

from field import Field
from misc.timeKeeper import timeit


class Solver:
    snapshots = OrderedDict()
    tested = set()
    solution = None

    def __init__(self, print_start_matrix: bool = True, print_solution_matrix: bool = True):
        self.counter = count()
        self.field = Field()
        self.print_start_matrix = print_start_matrix
        self.print_solution_matrix = print_solution_matrix

    def enter_values(self, matrix):
        matrix_str = "".join("".join(str(x) for x in y) for y in matrix)
        self.snapshots.clear()
        for point in self.field.get_all_points():
            point.flush()
        self.snapshots.update({matrix_str: None})

    @timeit
    def solve(self):
        field = self.field
        while len(self.snapshots) > 0:
            iteration = next(self.counter)
            try:
                current_field_str, _ = self.snapshots.popitem(last=True)
                self.tested.add(current_field_str)
                field.mutate_field(field.matrix_from_str(current_field_str), iteration != 0)
                if iteration == 0:
                    if self.print_start_matrix:
                        print(field)
                    pass
                field.solve()
            except Exception as e:
                # print(e)
                continue

            # print(current_field_str)
            # print(field)
            # field.enter_from_str(current_field_str)

            if field.solved:
                print(f"Solution was found on step #{iteration}")
                if self.print_solution_matrix:
                    print(field)
                return field

            elif field.unsolvable:
                # print(f"{iteration} - Solution is unsolvable")
                self.tested.add(current_field_str)
                pass

            elif len(field.possible_branches) > 0:
                possible_branches = [f for f in field.possible_branches if f not in self.tested]
                # print(f"{iteration} - {len(possible_branches)} branches added, {len(self.snapshots)} total")
                self.snapshots.update(dict.fromkeys(possible_branches))
        if not field.solved:
            print("Solution was NOT found")
