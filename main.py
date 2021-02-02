import from_web


class Field(object):
    snapshots = []
    solution = None

    def __init__(self):
        self.ready = False
        self.field = [[Point(y, x, value=0, parent=self) for x in range(9)] for y in range(9)]
        self.solved = False
        self.unsolvable = False

    def enter_values(self, matrix, solve: bool = True):
        self.ready = False
        for y, row in enumerate(matrix):
            for x, column in enumerate(row):
                self.field[y][x].value = matrix[y][x]
        print(self)
        self.ready = True
        if solve:
            self.solve()

    def get_values(self):
        return "".join(str(self.field[y][x].value) for y in range(9) for x in range(9))

    def solve(self):
        points = self.get_all_points()
        Field.snapshots.append(self.get_values())
        [point.calculate_possible() for point in points]
        if len([point.value for point in points if point.value == 0]) > 0:
            # print("No solution was found")
            # print("...")
            most_restricted_points = list(
                sorted([point for point in points if point.value == 0], key=lambda x: len(x.impossible_values),
                       reverse=True))
            # print(self)

            exit_for = False
            for restr_pt in most_restricted_points:
                if exit_for or self.unsolvable or not Field.solution is None:
                    break

                for possible_val in restr_pt.get_possible_values():
                    if exit_for or self.unsolvable or not Field.solution is None:
                        break
                    branch_field = Field()
                    for pt in self.get_all_points():
                        try:
                            branch_field.field[pt.row][pt.column].value = pt.value
                        except Exception as e:
                            print(e)

                    branch_field.field[restr_pt.row][restr_pt.column].value = possible_val
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
                        return
                    elif branch_field.unsolvable:
                        print("This variant is unsolvable. Skip it")
                        del branch_field
                        break

            # self.snapshots += [self.get_snapshot()]
            #
            # if len(self.snapshots) > 0:
            #     for restr_pt in most_restricted_points:
            #         for possible_val in restr_pt.get_possible_values():
            #             restr_pt.value = possible_val
            #             # restr_pt.calculate_possible(forced_calculation=True)
            #             [point.calculate_possible(forced_calculation=True) for point in points]
            #             print(f"hey there, {len([point.value for point in points if point.value == 0])} points were not solved")
            #             print(self)
            #
            #         self.enter_values(self.snapshots.pop(0))
        else:
            print("Sudoku is solved!")
            self.solved = True
            print(self)
            print("")

    def get_all_points(self):
        return [self.field[y][x] for y in range(9) for x in range(9)]

    def get_point(self, row: int, column: int):
        return self.field[row][column]

    def get_square(self, point):
        row, col = point.row, point.column
        return [self.field[y][x] for x in range(3 * (col // 3), 3 * (col // 3) + 3) for y in
                range(3 * (row // 3), 3 * (row // 3) + 3)]

    def get_row(self, point):
        return [self.field[y][point.column] for y in range(len(self.field))]

    def get_column(self, point):
        return [self.field[point.row][x] for x in range(len(self.field[point.row]))]

    def get_snapshot(self):
        return [[self.field[y][x].value for x, column in enumerate(row)] for y, row in enumerate(self.field)]

    def __str__(self):
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
        # return txt.replace("0", " ")
        return txt.replace("0", ".")


class Point(object):
    possible_values = list(range(10))
    impossible_values = []
    parent: Field = None

    def __init__(self, row, column, value=0, parent: Field = None):
        self.row = row
        self.column = column
        self._value = value
        self.parent = parent

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: int = 0):
        self._value = val
        if val not in self.possible_values + [0]:
            raise ValueError(f"Value can be one of following: {self.possible_values + [0]}, {val} was provided.")
        self.calculate_possible()

    @property
    def possible_values(self):
        return list(set(range(1, 10)) - self.impossible_values)

    @property
    def all_related(self):
        _all_related = self.__dict__.get("_all_related", None)
        if _all_related:
            return _all_related
        else:
            _all_related = set(self.get_row() + self.get_column() + self.get_square())
            self._all_related = {point for point in _all_related if point != self}
            return self._all_related

    def get_row(self):
        return self.parent.get_row(self)

    def get_column(self):
        return self.parent.get_column(self)

    def get_square(self):
        return self.parent.get_square(self)

    def get_possible_values(self):
        if len(self.impossible_values) == 9:
            self.parent.unsolvable = True
            return {}

        try:
            return sorted(set(self.possible_values) - self.impossible_values)[1:]
        except Exception as e:
            self.parent.unsolvable = True
            raise Exception("Unsolvable")
            return {}

    def calculate_square(self):
        if self.value == 0:
            # Neighbours
            square_pts = [pt for pt in self.get_square() if pt.value != self]
            # Values that already present
            solved_vals = [pt.value for pt in square_pts if pt.value != 0]
            # Values that are not yet set
            square_unsolved_vals = set(range(1, 10)) - set(solved_vals)

            self_possible_in_square = square_unsolved_vals.intersection(self.possible_values)

            square_possible = [set(range(1, 10)) - pt.impossible_values for pt in square_pts if
                               pt.value == 0 and pt != self]
            for val in self_possible_in_square:
                if len([_ for _ in square_possible if val in _]) == 0:
                    self.value = val
                    break

    def calculate_by_restrictions(self):
        if len(self.possible_values) == 0:
            self.parent.unsolvable = True
            raise Exception("Unsolvable")

        elif len(self.possible_values) == 1:
            self.value = self.possible_values[0]

    @property
    def impossible_values(self):
        return {point.value for point in self.all_related if point.value != 0 and point != self}

    def calculate_possible(self):
        if not self.parent.ready or self.value != 0:
            return

        self.calculate_by_restrictions()
        self.calculate_square()

        if self.value != 0:
            try:
                [point.calculate_possible() for point in self.all_related if
                 point != self and point.value == 0]
            except Exception as e:
                raise Exception(e)

    def __str__(self):
        return f"({self.row}-{self.column})-{self.value}"

    def __repr__(self):
        return f"({self.row}-{self.column})-{self.value}"


if __name__ == '__main__':
    f = Field()
    # vals = [
    #     [0, 6, 0, 8, 0, 3, 5, 9, 0],
    #     [1, 0, 0, 5, 0, 2, 0, 6, 7],
    #     [0, 0, 0, 0, 9, 0, 1, 0, 0],
    #     [0, 9, 0, 0, 0, 0, 7, 2, 0],
    #     [8, 0, 0, 6, 0, 9, 0, 0, 3],
    #     [0, 5, 6, 0, 0, 0, 0, 1, 0],
    #     [0, 0, 5, 0, 2, 0, 0, 0, 0],
    #     [9, 4, 0, 3, 0, 5, 0, 0, 1],
    #     [0, 1, 2, 4, 0, 7, 0, 3, 0]
    # ]
    # vals = [
    #     [0, 0, 0, 0, 9, 7, 0, 0, 6],
    #     [5, 0, 0, 2, 0, 0, 1, 0, 4],
    #     [3, 0, 0, 0, 0, 1, 0, 7, 0],
    #     [0, 9, 3, 8, 0, 5, 0, 0, 7],
    #     [0, 0, 0, 0, 1, 0, 0, 0, 0],
    #     [4, 0, 0, 7, 0, 6, 5, 9, 0],
    #     [0, 4, 0, 1, 0, 0, 0, 0, 9],
    #     [8, 0, 2, 0, 0, 9, 0, 0, 1],
    #     [9, 0, 0, 6, 4, 0, 0, 0, 0]
    # ]
    #
    # vals = [
    #     [0, 0, 0, 0, 6, 1, 0, 5, 0],
    #     [0, 0, 8, 0, 0, 0, 2, 1, 0],
    #     [0, 0, 0, 2, 5, 0, 0, 0, 3],
    #     [7, 0, 0, 0, 0, 0, 0, 3, 0],
    #     [0, 0, 3, 8, 1, 5, 9, 0, 0],
    #     [0, 2, 0, 0, 0, 0, 0, 0, 5],
    #     [2, 0, 0, 0, 8, 7, 0, 0, 0],
    #     [0, 3, 4, 0, 0, 0, 8, 0, 0],
    #     [0, 7, 0, 3, 9, 0, 0, 0, 0]
    # ]
    # vals = [
    #     [0, 0, 0, 0, 9, 7, 0, 0, 6],
    #     [5, 0, 0, 2, 0, 0, 1, 0, 4],
    #     [3, 0, 0, 0, 0, 1, 0, 7, 0],
    #     [0, 9, 3, 8, 0, 5, 0, 0, 7],
    #     [0, 0, 0, 0, 1, 0, 0, 0, 0],
    #     [4, 0, 0, 7, 0, 6, 5, 9, 0],
    #     [0, 4, 0, 1, 0, 0, 0, 0, 9],
    #     [8, 0, 2, 0, 0, 9, 0, 0, 1],
    #     [9, 0, 0, 6, 4, 0, 0, 0, 0]
    # ]
    # vals = [
    #     [0, 0, 0, 8, 5, 0, 0, 2, 0],
    #     [0, 0, 0, 0, 0, 7, 6, 0, 8],
    #     [8, 4, 0, 0, 0, 0, 7, 0, 0],
    #     [0, 0, 0, 0, 2, 0, 4, 6, 3],
    #     [4, 0, 0, 0, 0, 0, 0, 0, 9],
    #     [6, 1, 2, 0, 3, 0, 0, 0, 0],
    #     [0, 0, 6, 0, 0, 0, 0, 4, 2],
    #     [3, 0, 5, 7, 0, 0, 0, 0, 0],
    #     [0, 2, 0, 0, 8, 9, 0, 0, 0]
    # ]
    vals = [
        [0, 8, 0, 0, 9, 4, 0, 0, 0],
        [0, 0, 9, 1, 7, 0, 0, 0, 0],
        [4, 0, 1, 0, 0, 0, 0, 0, 3],
        [0, 0, 8, 0, 0, 0, 0, 2, 0],
        [5, 0, 0, 9, 1, 3, 0, 0, 8],
        [0, 9, 0, 0, 0, 0, 4, 0, 0],
        [3, 0, 0, 0, 0, 0, 8, 0, 6],
        [0, 0, 0, 0, 5, 8, 2, 0, 0],
        [0, 0, 0, 2, 3, 0, 0, 4, 0]
    ]
    # f.enter_values(vals)
    # print(f)
    req = from_web.get_from_web(3)
    f = from_web.fill_field_from_web(f, req)
    print(f)
    f.solve()
