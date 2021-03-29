from copy import deepcopy

from misc.errors import UnsolvableError
from point import Point


class Field:

    def __init__(self):
        self.ready = False
        self.field = tuple(tuple(Point(y, x, value=0, parent=self) for x in range(9)) for y in range(9))
        self.initial_field = None

        self.solved = False
        self.unsolvable = False
        self.possible_branches = []

    def enter_values(self, matrix: list, solve: bool = True) -> None:
        """
        Puts values from a given array to field. Matrix length is 9 * 9
        :param matrix: List 9 * 9
        :type matrix: list
        :param solve: Indicates if solution has to be found once it is set
        :type solve: bool
        :rtype: None
        """
        self.ready = False
        try:
            for y, row in enumerate(matrix):
                for x, column in enumerate(row):
                    self.field[y][x].value = int(matrix[y][x])
            self.initial_field = deepcopy(self.field)

        except UnsolvableError:
            self.unsolvable = True
            return

        self.ready = True
        if solve:
            self.solve()

    def get_values(self, field=None) -> str:
        """
        Returns string that represent Sudoku values as string 9 * 9 chars long
        E.g '436821975982567413751934682275193846643278159819645237367489521594312768128756394'
        :param field: Matrix 9*9 to analyse. If None - will analyse Field.field
        :type field: List or None
        :return: String representing Sudoku field values
        :rtype: str
        """
        if field is None:
            field = set()
        if len(field) == 0:
            field = self.field
        return "".join(str(field[y][x].value) for y in range(9) for x in range(9))

    @staticmethod
    def matrix_from_str(matrix_str: str) -> list:
        """
        Returns list representation of a Sudoku field from given string 9*9 chars long.
        E.g '436821975982567413751934682275193846643278159819645237367489521594312768128756394' will be converted to:
        [[4, 3, 6, 8, 2, 1, 9, 7, 5],
        [9, 8, 2, 5, 6, 7, 4, 1, 3],
        [7, 5, 1, 9, 3, 4, 6, 8, 2],
        [2, 7, 5, 1, 9, 3, 8, 4, 6],
        [6, 4, 3, 2, 7, 8, 1, 5, 9],
        [8, 1, 9, 6, 4, 5, 2, 3, 7],
        [3, 6, 7, 4, 8, 9, 5, 2, 1],
        [5, 9, 4, 3, 1, 2, 7, 6, 8],
        [1, 2, 8, 7, 5, 6, 3, 9, 4]]

        :param matrix_str: String to parse
        :type matrix_str: str
        :return: Sudoku field representation as a list
        :rtype: list
        """
        return [matrix_str[y * 9: y * 9 + 9] for y in range(9)]

    def enter_from_str(self, matrix_str: str) -> None:
        """
        Puts values from given string into to field. Matrix length is 9 * 9
        :param matrix_str: String of 81 character, representing values from left to right, from top to down
        :type matrix_str: str
        """
        matrix = self.matrix_from_str(matrix_str)
        self.enter_values(matrix=matrix, solve=True)

    def mutate_field(self, new_matrix: list, calculate: bool = True) -> bool:
        """
        Changes Field.field matrix to align with given new_matrix.
        Points with different values are changed accordingly - values are changed and
        related Points' restrictions are cleared.
        If calculate == True then Field will be recalculated.
        :param new_matrix: List representing new values of a Puzzle (list 9 * 9)
        :type new_matrix: List
        :param calculate: If calculate == True then Field will be recalculated.
        :type calculate: bool
        :return: Indicates if mutaton was done correctly
        :rtype: bool
        """
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

        except UnsolvableError:
            self.unsolvable = True
            return False
        except Exception as e:
            print(e)
            return False

        self.unsolvable = False
        return True

    def solve(self) -> bool:
        """
        Calculates all possible values for Field.
        If error occurs based on Points restrictions - will mark Field as unsolvable and return False.
        If there are points with no values - will generate guesses about their values and put them into
            Field.possible_branches (as str of len(81)).
        If all Points are filled with values - will mark Field as solved.
        If no errors occur during calculation - will return True.
        :return: False if Field is unsolvable ot True otherwise.
        :rtype: bool
        """
        if self.unsolvable:
            return False

        points = self.get_all_points()
        self.ready = True
        try:
            for point in points:
                point.calculate()
        except UnsolvableError:
            self.unsolvable = True
            return False

        if len([point.value for point in points if not point.has_value]) > 0:
            most_restricted_points = sorted((point for point in points if not point.has_value),
                                            key=lambda x: len(x.impossible_values), reverse=True)

            self_str = self.get_values(self.field)
            for restricted_point in most_restricted_points:
                change_pos = restricted_point.row * 9 + restricted_point.column
                for possible_val in restricted_point.possible_values:
                    new_str = self_str[:change_pos] + str(possible_val) + self_str[change_pos + 1:]
                    self.possible_branches.append(new_str)

        else:
            self.solved = True
        return True

    def get_all_points(self) -> list:
        """
        Returns list of all 81 Points from the Field
        :return: All Points from the Field
        :rtype: list[Point]
        """
        return [self.field[y][x] for y in range(9) for x in range(9)]

    def get_point(self, row: int, column: int) -> Point:
        """
        Returns Point from the Field at given row and column
        :return: Point at position Field[row][column]
        :rtype: Point
        """
        return self.field[row][column]

    def get_square(self, point: Point) -> list:
        """
        Returns list of all related Points from the Field in same square
        :return: list of Points at the same square as provided Point
        :rtype: list[*Point]
        """
        row, col = point.row, point.column
        return [self.field[y][x] for x in range(3 * (col // 3), 3 * (col // 3) + 3) for y in
                range(3 * (row // 3), 3 * (row // 3) + 3)]

    def get_column(self, point) -> list:
        """
        Returns list of all Points from the Field in same column
        :return: list of Points at the same column as provided Point
        :rtype: list[*Point]
        """
        return [self.field[y][point.column] for y in range(len(self.field))]

    def get_row(self, point) -> list:
        """
        Returns list of all Points from the Field in same row
        :return: list of Points at the same row as provided Point
        :rtype: list[*Point]
        """

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
