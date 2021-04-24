import numpy as np


class Point_np:

    def __init__(self, pos: int, parent):
        self.position = pos
        self.parent = parent

    @property
    def has_value(self):
        return self.value > 0

    @property
    def value(self) -> int:
        # OK
        return int(self.parent.fld[0, self.position])

    @value.setter
    def value(self, val: int) -> None:
        # OK
        if self.parent.fld[0, self.position] == val:
            self.parent.fld[1:, self.position] = 0
            return
        if val in self.possible_values:
            self.parent.fld[0, self.position] = val
            self.parent.fld[1:, self.position] = 0
            # print(f"Point {self.parent.fld_map.row_column_by_pos(self.position)} is {val}")

            related_pts_nums_all = self.parent.fld_map.related_excl(self.position)
            [pnt.restrict_by_neighbours() for pnt in self.parent.points[related_pts_nums_all]]

        else:
            raise ValueError(f"Value cannot be {val} - possible values are: {self.possible_values}")

    @property
    def possible_values(self) -> np.array:
        return np.flatnonzero(self.parent.fld[1:, self.position]) + 1

    @property
    def impossible_values(self) -> np.array:
        return np.flatnonzero(self.parent.fld[1:, self.position] == 0) + 1

    def get_all_related_points(self, excluding=True):
        if excluding:
            return self.parent.fld[:, self.parent.fld_map.related_excl(self.position)]
        else:
            return self.parent.fld[:, self.parent.fld_map.related_all(self.position)]

    def get_row(self, excluding=True):
        if excluding:
            return self.parent.fld[:, self.parent.fld_map.row_excl(self.position)]
        else:
            return self.parent.fld[:, self.parent.fld_map.row_all(self.position)]

    def get_column(self, excluding=True):
        if excluding:
            return self.parent.fld[:, self.parent.fld_map.column_excl(self.position)]
        else:
            return self.parent.fld[:, self.parent.fld_map.column_all(self.position)]

    def get_square(self, excluding=True):
        if excluding:
            return self.parent.fld[:, self.parent.fld_map.square_excl(self.position)]
        else:
            return self.parent.fld[:, self.parent.fld_map.square_all(self.position)]

    def calculate_by_restrictions(self) -> None:
        """
        Calculates value of the Point if only one is possible.
        """
        self.restrict_by_neighbours()
        if len(self.possible_values) == 1:
            self.value = int(self.possible_values[0])

    def calculate_single_pos_possible(self) -> None:
        """
        Calculates value of the Point if a value is possible only in the Point (the only place for value in row/column/square)
        """
        if self.has_value:
            return
        for pts, positions in (_ for _ in (
                (self.get_square(False), self.parent.fld_map.square_all(self.position)),
                (self.get_row(False), self.parent.fld_map.row_all(self.position)),
                (self.get_column(False), self.parent.fld_map.column_all(self.position))
        )):
            full_pts_w_numbers = np.where(pts == 1, np.tile(np.arange(10), (pts.shape[1], 1)).T, pts)
            full_pts_w_numbers[0, :] = 0
            if np.any(np.sum(full_pts_w_numbers > 0, axis=1) == 1):
                if np.count_nonzero(full_pts_w_numbers[np.sum(full_pts_w_numbers > 0, axis=1) == 1, :],
                                    axis=0).max() > 1:
                    return
                new_vals = np.vstack([
                    np.sum(full_pts_w_numbers[np.sum(full_pts_w_numbers > 0, axis=1) == 1, :], axis=0),
                    np.zeros((pts.shape[0] - 1, 9), dtype="int8")
                ])

                for pt_pos in np.flatnonzero(new_vals[0]):
                    if self.parent.fld[0, positions[pt_pos]] == 0:
                        try:
                            self.parent.points[positions[pt_pos]].value = new_vals[0, pt_pos]
                        except Exception as e:
                            print(e)

    def calculate_naked_pairs(self) -> None:
        """
        Calculates additional restrictions for the Point, using Naked Pair technique
        See https://www.learn-sudoku.com/naked-pairs.html for additional details
        If after calculation of applied restrictions only one value is possible - sets Point's value accordingly
        """
        return
        # TODO - Hm, it seems that it is quite rare situation (double pair when other points are not fully restricted)
        # TODO      Could not find such case anyway. Still, many time needed. Won't do for now.
        pass

        if self.has_value:
            return

        for pts, positions in (_ for _ in (
                (self.get_square(False), self.parent.fld_map.square_all(self.position)),
                (self.get_row(False), self.parent.fld_map.row_all(self.position)),
                (self.get_column(False), self.parent.fld_map.column_all(self.position))
        )):
            line = np.vstack([positions, pts])
            # array_to_clipboard(line)
            # print("Hi")

    def calculate_square_only_possible_row_or_col(self) -> None:
        """
        Applies additional restrictions for column or row out of Point's square if a value is possible only in
        one row/column inside of a Point's square
        """
        if self.has_value:
            return

        square, positions = self.get_square(False), self.parent.fld_map.square_all(self.position)
        # If possible in given positions and not possible in others - value is restricted to row(v) or column(h).
        # Number ["h"][_0_] says that we should restrict value outside of square on that line (in square it will
        #   definitely be there).
        lines = {
            "h": {
                0: (0, 1, 2),
                1: (3, 4, 5),
                2: (6, 7, 8)
            },
            "v": {
                0: (0, 3, 6),
                1: (1, 4, 7),
                2: (2, 5, 8)
            }
        }

        for possible_val in range(9):
            for dir, var in lines.items():
                for line_num, search_positions in var.items():
                    if (np.sum(square[1:][possible_val, search_positions]) > 0 and
                            np.sum(
                                square[1:][possible_val, np.isin(np.arange(9), search_positions, invert=True)]) == 0):

                        # TODO - Вывести колонку\строку, выделить элементы вне квадрата, зарестриктить значение
                        # TODO       и обновить их (возможно осталось 1 значение)
                        if dir == "v":
                            restricted_line = self.parent.fld_map.column_all(positions[search_positions[0]])
                        elif dir == "h":
                            restricted_line = self.parent.fld_map.row_all(positions[search_positions[0]])
                        else:
                            raise ValueError("Direction is undefined")

                        positions_outside_of_square = restricted_line[np.isin(restricted_line, positions, invert=True)]
                        self.parent.fld[possible_val + 1, positions_outside_of_square] = 0
                        for pt in self.parent.points[positions_outside_of_square]:
                            pt.restrict_value(possible_val + 1)

    def restrict_by_neighbours(self) -> None:
        impossible_vals = np.unique(self.get_all_related_points()[0, self.get_all_related_points()[0, :] > 0])
        self.apply_restrictions(impossible_vals)

    def restrict_value(self, value):
        if self.parent.fld[value, self.position] > 0:
            self.parent.fld[value, self.position] = 0
            self.calculate_by_restrictions()

    def apply_restrictions(self, impossible_vals: np.array) -> None:
        self.parent.fld[impossible_vals, self.position] = 0

    def calculate(self) -> None:
        """
        Applies all euristics to the Point to calculate its value or additional restrictions.
        If value was set during calculations, all related empty Points are triggered for a recalculation too.
        """
        # TODO
        if not self.parent.ready:
            return
        if self.has_value:
            return

        self.calculate_single_pos_possible()
        # self.calculate_naked_pairs()
        self.calculate_by_restrictions()

        if self.has_value:
            try:
                for point_num in np.flatnonzero(self.get_all_related_points()[0, :]):
                    self.parent.solve_queue.put(point_num)

            except Exception as e:
                raise Exception(e)
        else:
            pass

    def flush(self) -> None:
        if self.parent.fld[0, self.position] == 0:
            self.parent.fld[1:, self.position] = 1

    def __repr__(self):
        return f"Point_np({self.position}, {self.parent})"

    def __str__(self):
        return f"Point({self.parent.fld_map.row_column_by_pos(self.position)}) - {self.value}"
