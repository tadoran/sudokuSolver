import time

from field import gen
from old.point_old import PointOld


class FieldOld():
    snapshots = []
    solution = None

    def __init__(self):
        self.ready = False
        self.field = [[PointOld(y, x, value=0, parent=self) for x in range(9)] for y in range(9)]
        self.solved = False
        self.unsolvable = False
        self.check_queue = set()

    def enter_values(self, matrix, solve: bool = True):
        self.ready = False
        try:
            for y, row in enumerate(matrix):
                for x, column in enumerate(row):
                    self.field[y][x].value = int(matrix[y][x])
        except ValueError:
            self.unsolvable = True
            return

        self.ready = True
        if solve:
            self.solve()

    def get_values(self, field=[]):
        if len(field) == 0:
            field = self.field
        return "".join(str(field[y][x].value) for y in range(9) for x in range(9))

    def solve(self):
        points = self.get_all_points()
        self.check_queue.update(points)
        Field.snapshots.append(self.get_values())
        try:
            while len(self.check_queue) > 0:
                point = self.check_queue.pop()
                point.calculate()
            # [point.calculate() for point in points]
        except Exception as e:
            # print(e)
            raise Exception("Could not solve this variant")

        if len([point.value for point in points if point.value == 0]) > 0:

            print(f"No solution yet - {time.ctime()} {next(gen)}", end="\r", flush=True)
            # print(f"No solution yet - {time.ctime()}")
            # print(self)
            # excel3.reprFieldInXl(self)
            # print("...")
            most_restricted_points = list(
                sorted([point for point in points if point.value == 0], key=lambda x: len(x.impossible_values),
                       reverse=True))
            # print(self)
            exit_for = False
            for restr_pt in most_restricted_points:
                if exit_for or self.unsolvable or Field.solution is not None:
                    break

                for possible_val in restr_pt.possible_values:
                    if exit_for or self.unsolvable or Field.solution is not None:
                        break
                    # print(f"Assume that Point's {restr_pt} value is {possible_val}")
                    branch_field = Field()
                    for pt in self.get_all_points():
                        try:
                            branch_field.field[pt.row][pt.column].value = pt.value
                            branch_field.field[pt.row][pt.column].initial = True
                        except Exception as e:
                            # print(e)
                            pass

                    branch_field.field[restr_pt.row][restr_pt.column].value = possible_val
                    branch_field.field[restr_pt.row][restr_pt.column].initial = True
                    if branch_field.get_values() in Field.snapshots:
                        continue

                    branch_field.ready = True
                    try:
                        branch_field.solve()
                    except Exception:
                        continue

                    if branch_field.solved:
                        exit_for = True
                        Field.solution = branch_field
                        self = branch_field
                        return True

                    elif branch_field.unsolvable:
                        # print("This variant is unsolvable. Skip it")
                        del branch_field
                        break
        else:
            print("Sudoku is solved!")
            self.solved = True
            print(self)
            print("")
            return True

    def get_all_points(self):
        return [self.field[y][x] for y in range(9) for x in range(9)]

    def get_point(self, row: int, column: int):
        return self.field[row][column]

    def get_square(self, point):
        row, col = point.row, point.column
        return [self.field[y][x] for x in range(3 * (col // 3), 3 * (col // 3) + 3) for y in
                range(3 * (row // 3), 3 * (row // 3) + 3)]

    def get_column(self, point):
        return [self.field[y][point.column] for y in range(len(self.field))]

    def get_row(self, point):
        return [self.field[point.row][x] for x in range(len(self.field[point.row]))]

    def get_snapshot(self):
        return [[self.field[y][x].value for x, column in enumerate(row)] for y, row in enumerate(self.field)]

    def __str__(self):
        # if excel3.useExcel:
        #     excel3.reprFieldInXl(self)

        txt = ""
        for y, line in enumerate(self.field):

            if (y) % 3 == 0:
                txt += "-" * (9 + 1) * 3 + "-\n"
            txt += "|"
            for x, point in enumerate(line):
                txt += str(point.value).center(3)
                if (x + 1) % 3 == 0:
                    txt += "|"
            txt += "\n"
        txt += "-" * (9 + 1) * 3 + "-\n"
        # excel.reprFieldInXl(self)
        return txt.replace("0", ".")
