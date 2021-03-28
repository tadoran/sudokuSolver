from collections import OrderedDict
from copy import deepcopy
from itertools import count

from field import Field
from misc.errors import UnsolvableError
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

    def enter_from_str(self, matrix_str: str) -> None:
        """
        Fill the Field from a given string that represents Sudoku field values
        :param matrix_str: String with 81 char, representing Sudoku field. Empty points are declared as 0
        :type matrix_str: str
        """
        self.snapshots.clear()
        for point in self.field.get_all_points():
            point.flush()
        self.snapshots.update({matrix_str: None})

    def enter_values(self, matrix) -> None:
        """
        Fill the Field from a given iterable that represents Sudoku field values
        :param matrix: List of 9*9 integers or list of 9*9 Points
        :type matrix: list
        """
        if isinstance(matrix, Field):
            matrix_str = self.field.get_values()
        else:
            matrix_str = "".join("".join(str(x) for x in y) for y in matrix)

        self.snapshots.clear()
        for point in self.field.get_all_points():
            point.flush()
        self.snapshots.update({matrix_str: None})

    @property
    def initial_field(self) -> tuple:
        """
        Returns Field object that was initially set
        :return: Field object, representing values that were set before Sudoku was processed
        :rtype: tuple
        """
        return self.field.initial_field

    @timeit
    def solve(self) -> Field:
        """
        Applies calculations to solve given Sudoku.
        Solution calculation process is following:
        1. For a given field - try to calculate all possible Points' values
        2. If there are empty Points:
            a. Sort Points with no value according to their minimum possible values count
            b. Put all guesses about their possible values to Field.possible_branches
            c. Add all guesses to the end of OrderedDict (Solver.snapshots)
            d. Mutate current field status according to the last guess
            e. Try to calculate Field's Point values with new information
            f. Repeat the cycle until solution is found or no more guesses available
        :return: Filled Field if solution was found or None otherwise
        :rtype: Field
        """
        field = self.field
        while len(self.snapshots) > 0:
            iteration = next(self.counter)
            try:
                current_field_str, _ = self.snapshots.popitem(last=True)
                self.tested.add(current_field_str)
                field.mutate_field(field.matrix_from_str(current_field_str), iteration != 0)
                if iteration == 0:
                    if self.print_start_matrix:
                        self.field.initial_field = deepcopy(self.field)
                        print(field)
                    pass
                field.solve()
            except UnsolvableError:
                continue
            except Exception as e:
                print(e)
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
