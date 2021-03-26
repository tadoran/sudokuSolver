# from field import Field
from misc.static_method import static


class Point(object):
    # possible_values = list(range(10))
    vals_possible = set(range(1, 10))
    parent = None

    def __init__(self, row, column, value=0, parent=None, is_initial: bool = False):
        self.row = row
        self.column = column
        self._value = value
        self.restricted_values = set()
        self.parent = parent
        self.initial = is_initial

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: int = 0):
        self._value = val
        if val not in self.possible_values + [0]:
            raise ValueError(f"Value can be one of following: {self.possible_values + [0]}, {val} was provided.")
        if val > 0:
            self.restricted_values.update({n for n in range(9) if n != val})
        self.calculate()

    @property
    def possible_values(self):
        possible_values = list(Point.vals_possible - self.impossible_values)

        # if len(possible_values) == 0:
        #     self.parent.tested = True
        return possible_values

    @property
    def impossible_values(self):
        neigbors_vals = {point.value for point in self.all_related if point.value != 0}
        return neigbors_vals.union(self.restricted_values)

    @property
    @static
    def all_related(self):
        all_related = set(self.get_row() + self.get_column() + self.get_square())
        return {point for point in all_related if point != self}

    @static
    def get_row(self):
        return self.parent.get_row(self)

    @static
    def get_column(self):
        return self.parent.get_column(self)

    @static
    def get_square(self):
        return self.parent.get_square(self)

    def calculate_by_restrictions(self):
        if len(self.possible_values) == 0:
            # self.parent.tested = True
            raise Exception("Unsolvable")

        elif len(self.possible_values) == 1:
            self.value = self.possible_values[0]

    def calculate_single_pos_possible(self):
        if self.value != 0:
            return
        for pts in (_ for _ in (self.get_square(), self.get_row(), self.get_column())):
            for val in range(9):
                # If there is only one possible position for element - it should be selected
                val_possible_in_iter = (pt for pt in pts if val in pt.possible_values)
                try:
                    val_possible_in_first = None
                    val_possible_in_first = next(val_possible_in_iter)
                    next(val_possible_in_iter)
                except StopIteration:
                    if val_possible_in_first:
                        val_possible_in_first.value = val

    def calculate_single_pos_possible_old(self):
        if self.value != 0:
            return
        for pts in (_ for _ in [self.get_square(), self.get_row(), self.get_column()]):
            # Neighbours
            line_pts = pts
            # Values that already present
            solved_vals = [pt.value for pt in line_pts if pt.value != 0]
            # Values that are not yet set
            line_unsolved_vals = set(range(1, 10)) - set(solved_vals)

            self_possible_in_line = line_unsolved_vals.intersection(self.possible_values)

            line_possible = [set(range(1, 10)) - pt.impossible_values for pt in line_pts if
                             pt.value == 0 and pt != self]
            for val in self_possible_in_line:
                if len([_ for _ in line_possible if val in _]) == 0:
                    self.value = val
                    break
            if self.value != 0:
                break

    def calculate_naked_pairs(self):
        if self.value != 0:
            return
        for pts in (_ for _ in [self.get_square(), self.get_row(), self.get_column()]):
            line_possible = {pt: tuple(sorted(set(range(1, 10)) - pt.impossible_values))
                             for pt in pts if pt.value == 0}

            possible_combinations = {}
            for key, val in line_possible.items():
                combination = possible_combinations.get(val, None)
                if not combination:
                    possible_combinations[val] = []
                possible_combinations[val] += [key]

            for key, val in possible_combinations.items():
                # if len(key) == 2 and len(val) == 2:
                if len(key) == len(val):
                    # if len(key) > 2:
                    #     print(f"{len(key)} similar values")
                    for key1, value1 in line_possible.items():
                        if key1.value > 0:
                            continue
                        if value1 != key:
                            key1.restricted_values.update(key)
                            if len(key1.possible_values) == 0:
                                raise ValueError(f"Unsolvable - no possible values")
                            elif len(key1.possible_values) == 1:
                                key1.value = key1.possible_values[0]

    def calculate_square_only_possible_row_or_col(self):
        if self.value != 0:
            return

        square = self.get_square()
        for possible_value in self.possible_values:
            # print(possible_value)
            possible_rows = set(el.row for el in square if possible_value in el.possible_values)
            if len(possible_rows) == 1:
                other_cells_in_line = [el for el in self.get_row() if el not in square]
                for el in other_cells_in_line:
                    el.restricted_values.add(possible_value)
                # pass

            possible_columns = set(el.column for el in square if possible_value in el.possible_values)
            if len(possible_columns) == 1:
                other_cells_in_line = [el for el in self.get_column() if el not in square]
                for el in other_cells_in_line:
                    el.restricted_values.add(possible_value)

    def calculate(self):
        if not self.parent.ready:
            return
        if self.value != 0:
            return

        self.calculate_single_pos_possible()
        self.calculate_single_pos_possible_old()
        self.calculate_naked_pairs()
        self.calculate_square_only_possible_row_or_col()
        self.calculate_by_restrictions()

        if self.value != 0:
            try:
                self.parent.check_queue.update(
                    [point for point in self.all_related if point != self and point.value == 0])
                # [point.calculate() for point in self.all_related if point != self and point.value == 0]
            except Exception as e:
                raise Exception(e)
        else:
            pass

    def __str__(self):
        return f"({self.row}-{self.column})-{self.value}"

    def __repr__(self):
        return f"({self.row}-{self.column})-{self.value}"


class Point2(Point):
    def calculate(self):
        if not self.parent.ready:
            return
        if self.value != 0:
            return

        self.calculate_single_pos_possible()
        self.calculate_single_pos_possible_old()
        self.calculate_naked_pairs()
        self.calculate_square_only_possible_row_or_col()
        self.calculate_by_restrictions()

        if self.value != 0:
            try:
                # [point.calculate() for point in self.all_related if point != self and point.value == 0]
                for point in self.all_related:
                    if point != self and point.value == 0:
                        point.calculate()
            except Exception as e:
                raise Exception(e)
        else:
            pass

    def flush(self):
        self.restricted_values = set()
