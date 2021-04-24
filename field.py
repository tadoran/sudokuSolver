from itertools import chain
from queue import Queue

import numpy as np

from fieldMap import FieldMap
from misc.errors import UnsolvableError
from point import Point_np as Point


class Field_np:

    def __init__(self):
        self.fld_map = FieldMap()
        self.points = np.array([Point(i, self) for i in range(81)])
        self.fld = np.zeros((10, 81), dtype='int8')
        self.solve_queue = Queue()
        self.ready = False
        self.possible_branches = []
        self.solved = False
        self.unsolvable = False

    def cast_to_99_shape(self):
        return self.fld[0].reshape((9, 9))

    def to_clipboard(self):
        from num_field import array_to_clipboard
        array_to_clipboard(self.cast_to_99_shape())

    def enter_values(self, matrix_str: str, solve: bool = True) -> None:
        # TODO - solve param
        self.ready = False
        self.fld = np.array([ch for ch in matrix_str], dtype='int8')
        fld_vals = self.fld
        self.fld = np.vstack([self.fld, np.tile(np.ones_like(fld_vals), (9, 1))])
        self.fld[1:, :][0:, self.fld[0, :] > 0] = 0
        self.ready = True

    def mutate_field(self, new_matrix: str, calculate: bool = True) -> bool:
        old_matrix = np.copy(self.fld)
        new_fld_vals = np.array([ch for ch in new_matrix], dtype='int8')
        diff_arr = new_fld_vals - self.fld[0, :]
        diff_positions = np.flatnonzero(diff_arr)
        # print(*[f"{str(self.points[pos])} -> {new_fld_vals[pos]}" for pos in diff_positions], sep="\n")

        for i in diff_positions:
            self.fld[0, i] = new_fld_vals[i]
            self.fld[1:, i] = 0
            if new_fld_vals[i] > 0:
                self.fld[new_fld_vals[i], self.fld_map.related_all(i)] = 0
        self.ready = True
        try:
            self.validate()
        except UnsolvableError:
            self.fld = old_matrix
            raise UnsolvableError

    def validate(self):
        # TODO: vectorize it
        # Validate that mutated field is still valid
        for seq in chain(self.fld_map.all_cols.values(), self.fld_map.all_rows.values(),
                         self.fld_map.all_squares.values()):
            seq_vals = self.fld[0, seq]
            seq_vals_counts = np.unique(seq_vals[seq_vals > 0], return_counts=True)
            duplicates = np.sum(seq_vals_counts[1] > 1)
            if duplicates > 0:
                # print("Unsolvable", seq_vals, seq_vals_counts, duplicates)
                self.unsolvable = True
                raise UnsolvableError

    def solve(self) -> bool:
        try:
            self.validate()
        except UnsolvableError:
            self.unsolvable = True
            self.solved = False
            return
        calculate_again = True

        empty_points = np.flatnonzero(self.fld[0, :] == 0, )
        points_calculated = len(empty_points)
        while calculate_again:
            [pnt.restrict_by_neighbours() for pnt in self.points]
            non_empty_points = np.flatnonzero(self.fld[0, :] > 0, )
            self.fld[1:, non_empty_points] = 0
            single_possible_points = self.points[np.sum(self.fld[1:, :], axis=0) == 1]
            if len(single_possible_points) > 0:
                [pnt.calculate_by_restrictions() for pnt in single_possible_points]

            [self.solve_queue.put(empty_point) for empty_point in empty_points]

            while not self.solve_queue.empty():
                point_num = self.solve_queue.get()
                cur_point = self.points[point_num]
                if cur_point.value != 0:
                    continue
                else:
                    try:
                        cur_point.calculate()
                    except Exception as e:
                        print(e)
                        self.unsolvable = True
                        raise UnsolvableError

            empty_points = np.flatnonzero(self.fld[0, :] == 0, )
            if len(empty_points) < points_calculated:
                points_calculated = len(empty_points)
                calculate_again = True

                # Calculate square restrictions
                for pt in self.points[[0, 3, 6, 27, 30, 33, 54, 57, 60]]:
                    pt.calculate_square_only_possible_row_or_col()
            elif self.solve_queue.empty():
                calculate_again = False
                if len(empty_points) > 0:
                    self.propose_most_restricted_point_fill()
                else:
                    self.solved = True
                # break
            else:
                if len(empty_points) > 0:
                    self.propose_most_restricted_point_fill()
                else:
                    self.solved = True
                break

    def get_all_points(self):
        return self.points

    def get_point(self, row: int, column: int) -> Point:
        return self.points[self.fld_map.pos_by_row_column(row, column)]

    def get_square(self, point: Point) -> tuple:
        return self.fld_map.square_all(point.position)

    def get_column(self, point) -> tuple:
        return self.fld_map.column_all(point.position)

    def get_row(self, point) -> tuple:
        return self.fld_map.row_all(point.position)

    def propose_most_restricted_point_fill(self):
        try:
            [pnt.restrict_by_neighbours() for pnt in self.points]

            self.possible_branches = []
            pt_possible_count = np.sum(self.fld[1:], axis=0)
            if np.sum(pt_possible_count) == 0:
                return
            most_restr_pts = np.argsort(pt_possible_count)
            # TODO: Нормальные названия переменных
            dsd = np.vstack([
                np.arange(self.fld.shape[1]),
                self.fld
            ])[:, np.flip(most_restr_pts, axis=0)]

            dsd2 = dsd[0, dsd[1] == 0]
            dsd3 = np.vstack([dsd2, self.fld[1:, dsd2] * np.arange(1, 10).reshape(9, 1)])

            chunks = []
            for i in range(dsd3.shape[1]):
                cur_pt_possible = dsd3[dsd3[:, i] > 0, i]
                chunks.append(
                    np.vstack([
                        np.tile(cur_pt_possible[0], len(cur_pt_possible) - 1),
                        cur_pt_possible[1:]
                    ]))
            probable_vals = np.hstack(chunks)

            # Генерируем стоки с мутированным значением ver.2
            branches = np.tile(self.fld[0], [probable_vals.shape[1], 1])
            for i in range(len(branches)):
                mutated_pos = probable_vals[0, i]
                if branches[i, mutated_pos] == 0:
                    branches[i, mutated_pos] = probable_vals[1, i]
                else:
                    branches[i, :] = 0

            branches = branches[np.sum(branches, axis=1) > 0, :]
            for i in range(len(branches)):
                self.possible_branches.append(np.array2string(branches[i], separator='', max_line_width=90)[1:-1])

        except Exception as e:
            print(e)

    def __str__(self):
        # TODO - сделал на отъебись, переделать
        txt = ""
        txt += ("-" * 32) + "\n"
        for row, ln in enumerate(self.cast_to_99_shape()):
            line = np.array2string(ln, separator="  ")[1:-1]
            txt += "| " + line[:9] + "| " + line[9:17] + "| " + line[18:] + " |" + "\n"
            if row + 1 in [3, 6, 9]:
                txt += ("-" * (32)) + "\n"
        txt = txt.replace('0', '.')
        return txt
