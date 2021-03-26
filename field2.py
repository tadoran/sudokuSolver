from collections import OrderedDict
from itertools import count

from field import Field
from misc.timeKeeper import timeit
from point import Point2


class Solver:
    snapshots = OrderedDict()
    tested = set()
    solution = None

    def __init__(self):
        self.counter = count()
        self.field = Field2()

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


class Field2(Field):

    def __init__(self):
        self.ready = False
        self.field = [[Point2(y, x, value=0, parent=self) for x in range(9)] for y in range(9)]

        self.solved = False
        self.unsolvable = False
        self.possible_branches = []

    def matrix_from_str(self, matrix_str):
        return [matrix_str[y * 9: y * 9 + 9] for y in range(9)]

    def enter_from_str(self, matrix_str):
        matrix = self.matrix_from_str(matrix_str)
        self.enter_values(matrix=matrix, solve=True)

    def mutate_field(self, new_matrix, calculate=True):
        try:
            self.ready = False
            for y, row in enumerate(self.field):
                for x, point in enumerate(row):
                    val = int(new_matrix[y][x])
                    if point.value != val:
                        for related_point in point.all_related:
                            related_point.flush()
                        point.value = val

            self.ready = True
            if calculate:
                for y, row in enumerate(self.field):
                    for x, point in enumerate(row):
                        point.calculate()

        except ValueError:
            self.unsolvable = True
            return False
        except Exception as e:
            # print(e)
            return False
        self.unsolvable = False
        return True

    def solve(self):
        if self.unsolvable:
            return

        points = self.get_all_points()
        self.ready = True
        try:
            for point in points:
                point.calculate()
        except Exception as e:
            self.unsolvable = True
            return

        if len([point.value for point in points if point.value == 0]) > 0:
            most_restricted_points = sorted([point for point in points if point.value == 0],
                                            key=lambda x: len(x.impossible_values), reverse=True)

            self_str = self.get_values(self.field)
            for restr_pt in most_restricted_points:
                change_pos = (restr_pt.row) * 9 + (restr_pt.column)
                for possible_val in restr_pt.possible_values:
                    new_str = self_str[:change_pos] + str(possible_val) + self_str[change_pos + 1:]
                    self.possible_branches.append(new_str)

        else:
            self.solved = True
