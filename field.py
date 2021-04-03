from copy import deepcopy
from itertools import permutations, chain

from misc.errors import UnsolvableError
from misc.static_method import calculated_once_dict
from misc.string_manipulations import string_mutations, difference_indices
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

    def get_values_as_str(self, field=None) -> str:
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
            differences = difference_indices(self.get_values_as_str(self.field), "".join(new_matrix))
            for diff in differences:
                row, col = diff // 9, diff % 9
                cur_point = self.field[row][col]
                new_val = int(new_matrix[row][col])
                if cur_point.value != new_val:
                    for related_point in cur_point.get_all_related_points():
                        related_point.flush()
                    cur_point.value = new_val

            self.ready = True
            if calculate:
                for y, row in enumerate(self.field):
                    for x, point in enumerate(row):
                        point.calculate()

        except UnsolvableError:
            self.unsolvable = True
            return False
        except Exception as e:
            # print(e)
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
            self.propose_most_restricted_point_fill(points)

            # Shows poor result times
            # self.propose_lines_fill()

        else:
            self.solved = True
        return True

    @calculated_once_dict
    def get_all_squares(self) -> tuple:
        return tuple(self.get_square(self.get_point(y, x)) for y in range(1, 9, 3) for x in range(1, 9, 3))

    @calculated_once_dict
    def get_all_rows(self) -> tuple:
        return tuple(self.get_row(self.get_point(y, 0)) for y in range(9))

    @calculated_once_dict
    def get_all_columns(self) -> tuple:
        return tuple(self.get_column(self.get_point(0, x)) for x in range(9))

    @calculated_once_dict
    def get_all_lines(self) -> tuple:
        all = []
        all.extend(self.get_all_rows())
        all.extend(self.get_all_columns())
        all.extend(self.get_all_squares())
        return tuple(all)

    @calculated_once_dict
    def get_all_points(self) -> tuple:
        """
        Returns list of all 81 Points from the Field
        :return: All Points from the Field
        :rtype: list[Point]
        """
        return tuple(self.field[y][x] for y in range(9) for x in range(9))

    def get_point(self, row: int, column: int) -> Point:
        """
        Returns Point from the Field at given row and column
        :return: Point at position Field[row][column]
        :rtype: Point
        """
        return self.field[row][column]

    def get_square(self, point: Point) -> tuple:
        """
        Returns list of all related Points from the Field in same square
        :return: list of Points at the same square as provided Point
        :rtype: list[*Point]
        """
        row, col = point.row, point.column
        return tuple(self.field[y][x] for x in range(3 * (col // 3), 3 * (col // 3) + 3) for y in
                     range(3 * (row // 3), 3 * (row // 3) + 3))

    def get_column(self, point) -> tuple:
        """
        Returns list of all Points from the Field in same column
        :return: list of Points at the same column as provided Point
        :rtype: list[*Point]
        """
        return tuple(self.field[y][point.column] for y in range(len(self.field)))

    def get_row(self, point) -> tuple:
        """
        Returns list of all Points from the Field in same row
        :return: list of Points at the same row as provided Point
        :rtype: list[*Point]
        """

        return tuple(self.field[point.row][x] for x in range(len(self.field[point.row])))

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

    def propose_lines_fill(self):
        all_lines = self.get_all_lines()

        most_restricted_lines = {}
        for i, line in enumerate(all_lines):
            empty_points = [pt for pt in line if not pt.has_value]
            line_len = len(empty_points)
            possibles = (pt.possible_values for pt in empty_points)
            possible_values = set(chain(*possibles))
            # TODO: Should stay iterable - find a algorithm to count permutations count w\o it's run
            line_permutations = tuple(permutations(possible_values, line_len))
            permutations_count = len(line_permutations)
            try:
                most_restricted_lines[i] = {}
                most_restricted_lines[i]["len"] = line_len
                most_restricted_lines[i]["points"] = tuple((pt.row, pt.column) for pt in empty_points)
                most_restricted_lines[i]["str_pos"] = tuple(
                    coord[0] * 9 + coord[1] for coord in most_restricted_lines[i]["points"])
                most_restricted_lines[i]["possible_values"] = possible_values
                most_restricted_lines[i]["permutations"] = line_permutations
                most_restricted_lines[i]["permutations_count"] = permutations_count
            except Exception as e:
                print(e)

        most_restricted_lines = sorted(most_restricted_lines.values(), key=lambda x: x["permutations_count"])[:3]
        field_str = self.get_values_as_str()
        for line in most_restricted_lines:
            values_permutations = line["permutations"]
            mutations = string_mutations(input_str=field_str, positions_to_replace=line["str_pos"],
                                         values_to_insert=values_permutations)
            for mutation in mutations:
                self.possible_branches.append(mutation)

    def propose_most_restricted_point_fill(self, points):
        most_restricted_points = sorted((point for point in points if not point.has_value),
                                        key=lambda x: len(x.impossible_values), reverse=True)

        field_str = self.get_values_as_str(self.field)
        for restricted_point in most_restricted_points:
            change_pos = restricted_point.row * 9 + restricted_point.column

            values_permutations = restricted_point.possible_values
            mutations = string_mutations(input_str=field_str, positions_to_replace=change_pos,
                                         values_to_insert=values_permutations)
            for mutation in mutations:
                self.possible_branches.append(mutation)
