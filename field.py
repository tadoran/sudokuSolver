from misc import looping_char
from point import Point

gen = looping_char.gen


class Field:

    def __init__(self):
        self.ready = False
        self.field = tuple(tuple(Point(y, x, value=0, parent=self) for x in range(9)) for y in range(9))

        self.solved = False
        self.unsolvable = False
        self.possible_branches = []

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

    @staticmethod
    def matrix_from_str(matrix_str):
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
                        for related_point in point.get_all_related_points():
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

    def __str__(self):
        txt = ""
        for y, line in enumerate(self.field):

            if y % 3 == 0:
                txt += "-" * (9 + 1) * 3 + "-\n"
            txt += "|"
            for x, point in enumerate(line):
                txt += str(point.value).center(3)
                if (x + 1) % 3 == 0:
                    txt += "|"
            txt += "\n"
        txt += "-" * (9 + 1) * 3 + "-\n"
        return txt.replace("0", ".")
