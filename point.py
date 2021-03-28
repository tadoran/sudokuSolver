from misc.errors import UnsolvableError
from misc.static_method import calculated_once_dict


class Point:
    valid_values = set(range(1, 10))
    parent = None

    def __init__(self, row, column, value=0, parent=None):
        self.row = row
        self.column = column
        self._value = value
        self.restricted_values = set()
        self.parent = parent
        self.has_value = False

    @property
    def value(self) -> int:
        """
        Returns value of particular Point
        :return: Value of the Point, 0 if not set
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, val: int = 0):
        """
        Sets Point's value. If value is not possible due to restrictions - UnsolvableError is thrown
        :param val: Value to be set. Allowed integers are in range(10)
        :type val: int
        """
        self._value = val
        if val not in self.possible_values + [0]:
            raise UnsolvableError(f"Value can be one of following: {self.possible_values + [0]}, {val} was provided.")
        if val > 0:
            self.restricted_values.update({n for n in range(9) if n != val})
            self.has_value = True
        else:
            self.has_value = False

        self.calculate()

    @property
    def possible_values(self) -> list:
        """
        Returns values that are possible for the Point, according to given restrictions from related Points
        :return: Possible values for the Point
        :rtype: list[int]
        """
        possible_values = list(Point.valid_values - self.impossible_values)
        return possible_values

    @property
    def impossible_values(self) -> set:
        """
        Returns set of values that are restricted for the Point according to it's related Points values
        :return: Set of impossible values for the Point
        :rtype: set[int]
        """
        neighbors_values = {point.value for point in self.get_all_related_points() if point.has_value}
        return neighbors_values.union(self.restricted_values)

    @calculated_once_dict
    def get_all_related_points(self) -> set:
        """
        Returns set of all related to the Point Points (same row, same column, same square)
        :return: Set of all related Points
        :rtype: set
        """
        all_related = set(self.get_row() + self.get_column() + self.get_square())
        return {point for point in all_related if point != self}

    @calculated_once_dict
    def get_row(self) -> list:
        """
        Returns list of all Points from the Field in same row
        :return: list of Points at the same row as the Point
        :rtype: list[*Point]
        """
        return self.parent.get_row(self)

    @calculated_once_dict
    def get_column(self) -> list:
        """
        Returns list of all Points from the Field in same column
        :return: list of Points at the same column as the Point
        :rtype: list[*Point]
        """
        return self.parent.get_column(self)

    @calculated_once_dict
    def get_square(self) -> list:
        """
        Returns list of all related Points from the Field in same square
        :return: list of Points at the same square as the Point
        :rtype: list[*Point]
        """
        return self.parent.get_square(self)

    # Calculation euristics

    def calculate_by_restrictions(self) -> None:
        """
        Calculates value of the Point if only one is possible.
        """
        if len(self.possible_values) == 0:
            raise UnsolvableError()

        elif len(self.possible_values) == 1:
            self.value = self.possible_values[0]

    def calculate_single_pos_possible(self) -> None:
        """
        Calculates value of the Point if a value is possible only in the Point (the only place for value in row/column/square)
        """
        if self.has_value:
            return
        for pts in (_ for _ in (self.get_square(), self.get_row(), self.get_column())):
            for val in Point.valid_values:
                # If there is only one possible position for element - it should be selected
                val_possible_in_iter = (pt for pt in pts if val in pt.possible_values)
                val_possible_in_first = None
                try:
                    val_possible_in_first = next(val_possible_in_iter)
                    next(val_possible_in_iter)
                except StopIteration:
                    if val_possible_in_first:
                        val_possible_in_first.value = val

    def calculate_single_pos_possible_old(self) -> None:
        if self.has_value:
            return
        for pts in (_ for _ in (self.get_square(), self.get_row(), self.get_column())):
            # Values that already present
            solved_values = {pt.value for pt in pts if pt.has_value}
            # Values that are not yet set
            line_unsolved_values = Point.valid_values - solved_values

            self_possible_in_line = line_unsolved_values.intersection(self.possible_values)

            line_possible = [pt.possible_values for pt in pts if not pt.has_value and pt != self]
            try:
                for val in self_possible_in_line:
                    if len([_ for _ in line_possible if val in _]) == 0:
                        self.value = val
                        break
            except Exception as e:
                print(e)

            if self.has_value:
                break

    def calculate_naked_pairs(self) -> None:
        """
        Calculates additional restrictions for the Point, using Naked Pair technique
        See https://www.learn-sudoku.com/naked-pairs.html for additional details
        If after calculation of applied restrictions only one value is possible - sets Point's value accordingly
        """
        if self.has_value:
            return
        for pts in (_ for _ in [self.get_square(), self.get_row(), self.get_column()]):
            line_possible = {pt: tuple(pt.possible_values) for pt in pts if not pt.has_value}

            possible_combinations = {}
            for key, val in line_possible.items():
                combination = possible_combinations.get(val, None)
                if not combination:
                    possible_combinations[val] = []
                possible_combinations[val] += [key]

            for key, val in possible_combinations.items():
                if len(key) == len(val):
                    for key1, value1 in line_possible.items():
                        if key1.has_value:
                            continue
                        if value1 != key:
                            key1.restricted_values.update(key)
                            if len(key1.possible_values) == 0:
                                raise UnsolvableError(f"Unsolvable - no possible values")
                            elif len(key1.possible_values) == 1:
                                key1.value = key1.possible_values[0]

    def calculate_square_only_possible_row_or_col(self) -> None:
        """
        Applies additional restrictions for column or row out of Point's square if a value is possible only in
        one row/column inside of a Point's square
        """
        if self.has_value:
            return

        square = self.get_square()
        for possible_value in self.possible_values:
            possible_rows = set(el.row for el in square if possible_value in el.possible_values)
            if len(possible_rows) == 1:
                other_cells_in_line = (el for el in self.get_row() if el not in square)
                for el in other_cells_in_line:
                    el.restricted_values.add(possible_value)

            possible_columns = set(el.column for el in square if possible_value in el.possible_values)
            if len(possible_columns) == 1:
                other_cells_in_line = [el for el in self.get_column() if el not in square]
                for el in other_cells_in_line:
                    el.restricted_values.add(possible_value)

    def calculate(self) -> None:
        """
        Applies all euristics to the Point to calculate its value or additional restrictions.
        If value was set during calculations, all related empty Points are triggered for a recalculation too.
        """
        if not self.parent.ready:
            return
        if self.has_value:
            return

        self.calculate_single_pos_possible()
        self.calculate_single_pos_possible_old()
        self.calculate_naked_pairs()
        self.calculate_square_only_possible_row_or_col()
        self.calculate_by_restrictions()

        if self.has_value:
            try:
                for point in self.get_all_related_points():
                    if point != self and not point.has_value:
                        point.calculate()
            except Exception as e:
                raise Exception(e)
        else:
            pass

    def flush(self) -> None:
        """
        Clears cache for the Point in a way that it is possible to insert new value for it without error.
        Used for mutation from a Field().
        """
        self.restricted_values = set()
