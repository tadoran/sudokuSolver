from itertools import chain
from queue import Queue

import numpy as np

from fieldMap import FieldMap
from misc.errors import UnsolvableError
from point_np import Point_np as Point


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
        # self.fld.dtype.names = tuple(range(self.fld.shape[0]+1))
        fld_vals = self.fld
        self.fld = np.vstack([self.fld, np.tile(np.ones_like(fld_vals), (9, 1))])
        self.fld[1:, :][0:, self.fld[0, :] > 0] = 0
        self.ready = True

    def mutate_field(self, new_matrix: str, calculate: bool = True) -> bool:
        # TODO
        # new_fld_vals = np.array([ch for ch in self.possible_branches[-1]], dtype='int8')
        # return
        # old_matrix_str = np.array2string(self.fld[0], separator='', max_line_width=90)[1:-1]
        old_matrix = np.copy(self.fld)
        new_fld_vals = np.array([ch for ch in new_matrix], dtype='int8')
        diff_arr = new_fld_vals - self.fld[0, :]
        diff_positions = np.flatnonzero(diff_arr)
        diff_difference_vals = diff_arr[diff_positions]
        # print(diff_arr[diff_positions])
        # print(*[f"{str(self.points[pos])} -> {new_fld_vals[pos]}" for pos in diff_positions], sep="\n")
        # if np.sum(diff_arr < 0) > 0:
        #     print("")

        # print("")
        for i in diff_positions:
            self.fld[0, i] = new_fld_vals[i]
            self.fld[1:, i] = 0
            if new_fld_vals[i] > 0:
                # for pt_num in self.fld_map.related_all(i):
                #     self.points[pt_num].flush()
                self.fld[new_fld_vals[i], self.fld_map.related_all(i)] = 0
            # elif:
            #     self.fld[new_fld_vals[i], self.fld_map.related_all(i)] = 1
        self.ready = True
        try:
            self.validate()
        except UnsolvableError:
            # print(old_matrix_str)
            # print(new_matrix)
            # print("")
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
        calculate_again = True

        # TODO
        empty_points = np.flatnonzero(self.fld[0, :] == 0, )
        points_calculated = len(empty_points)
        # print(f"Start solving, there are {len(empty_points)} unsolved points.")
        while calculate_again:
            [pnt.restrict_by_neighbours() for pnt in self.points]
            non_empty_points = np.flatnonzero(self.fld[0, :] > 0, )
            self.fld[1:, non_empty_points] = 0
            single_possible_points = self.points[np.sum(self.fld[1:, :], axis=0) == 1]
            if len(single_possible_points) > 0:
                [pnt.calculate_by_restrictions() for pnt in single_possible_points]

            [self.solve_queue.put(empty_point) for empty_point in empty_points]

            while not self.solve_queue.empty():
                # point_num = int(self.solve_queue.get())
                point_num = self.solve_queue.get()
                cur_point = self.points[point_num]
                # print(cur_point.value)
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
                # print(f"Done solving iteration, there are {len(empty_points)} unsolved points left.")
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
                # print(f"Done solving, there are {len(empty_points)} unsolved points left.")
                if len(empty_points) > 0:
                    self.propose_most_restricted_point_fill()
                else:
                    self.solved = True
                break
            # [pnt.restrict_by_neighbours() for pnt in self.points]
        # print("done calculations for now")
        # print(self)

    def get_all_points(self):
        return self.points

    def get_point(self, row: int, column: int) -> Point:
        # OK
        # return Point(self.fld_map.pos_by_row_column(row, column), self)
        return self.points[self.fld_map.pos_by_row_column(row, column)]

    def get_square(self, point: Point) -> tuple:
        # OK
        return self.fld_map.square_all(point.position)

    def get_column(self, point) -> tuple:
        # OK
        return self.fld_map.column_all(point.position)

    def get_row(self, point) -> tuple:
        # OK
        return self.fld_map.row_all(point.position)

    def __str__(self):
        # TODO
        pass

    def propose_most_restricted_point_fill(self):
        try:
            # TODO - Запутулся к хуям :-)
            pass

            [pnt.restrict_by_neighbours() for pnt in self.points]

            self.possible_branches = []
            pt_possible_count = np.sum(self.fld[1:], axis=0)
            # fld_w_zero_val = np.arange(self.fld.shape[1])[self.fld[0, :] == 0]
            # pts_wo_vals = self.fld[0, :] == 0
            most_restr_pts = np.argsort(pt_possible_count)
            # ssa = np.vstack([np.arange(self.fld.shape[1]), most_restr_pts])[:, pts_wo_vals]
            # most_restr_pts2 = ssa[:, np.argsort(ssa[1,:])][0]

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
            # branches = np.flip(branches, axis=0)
            for i in range(len(branches)):
                self.possible_branches.append(np.array2string(branches[i], separator='', max_line_width=90)[1:-1])

            return

            # most_restr_pts_possibilities = self.fld[1:, most_restr_pts][:, self.fld[0, most_restr_pts] == 0]

            # Номера столбцов с наименьшим кол-вом вариантов
            # most_restricted_points = np.flip(np.argsort(np.sum(self.fld[1:], axis=0)))

            # most_restricted_points2 = np.arange(self.fld.shape[1])[np.flip(most_restricted_points[fld_w_zero_val])]

            # Возможные значения для каждой точки  [0, № точки] - точка, [1, № точки] - возможное значение
            ######## TODO - группировать и использовать
            ######## TODO   ВАЖНО! Номера точек тут - отсортированы не как в изначльном массиве, нужно сконвертировать обратно
            #######probable_vals = np.vstack([
            #######    np.flatnonzero(most_restr_pts_possibilities == 1) % most_restr_pts_possibilities.shape[1],
            #######    (np.flatnonzero(most_restr_pts_possibilities == 1) // most_restr_pts_possibilities.shape[1]) + 1
            #######])
            ######## Сортируем по номеру точки, затем по значениям
            #######probable_vals = probable_vals[:, np.lexsort([probable_vals[1, :], probable_vals[0, :]])]

            # Генерируем стоки с мутированным значением ver.2
            branches = np.tile(self.fld[0], [probable_vals.shape[1], 1])
            for i in reversed(range(len(branches))):
                mutated_pos = probable_vals[0, i]
                fld_pos = most_restr_pts[mutated_pos]
                if branches[i, fld_pos] == 0:
                    branches[i, fld_pos] = probable_vals[1, i]
                else:
                    branches[i, :] = 0
            branches = branches[np.sum(branches, axis=1) > 0, :]
            branches = np.flip(branches, axis=0)
            for i in range(len(branches)):
                self.possible_branches.append(np.array2string(branches[i], separator='', max_line_width=90)[1:-1])

            return
            # Генерируем стоки с мутированным значением ver. 1 (old)
            for i in range(probable_vals.shape[1] - 1, -1, -1):
                start_arr = self.fld[0].copy()
                mutated_pos = probable_vals[0, i]
                fld_pos = most_restr_pts[mutated_pos]
                if start_arr[fld_pos] == 0:
                    start_arr[fld_pos] = probable_vals[1, i]
                    str_to_append = np.array2string(start_arr, separator='', max_line_width=90)[1:-1]
                    # print("-" * (fld_pos) + "V")
                    # print(str_to_append)
                    self.possible_branches.append(str_to_append)
                else:
                    # print("Just passing")
                    pass



        except Exception as e:
            print(e)
        # print('Hi')

    def __str__(self):
        # TODO - сделал на отъебись, переделать
        txt = ""
        txt += ("-" * (32)) + "\n"
        for row, ln in enumerate(self.cast_to_99_shape()):
            line = np.array2string(ln, separator="  ")[1:-1]
            txt += "| " + line[:9] + "| " + line[9:17] + "| " + line[18:] + " |" + "\n"
            if row + 1 in [3, 6, 9]:
                txt += ("-" * (32)) + "\n"
        txt = txt.replace('0', '.')
        return txt
        # print(np.array2string(self.cast_to_99_shape(), separator="")[1:-1])


if __name__ == '__main__':
    # Solved on first iteration
    field_str = "060803590100502067000090100090000720800609003056000010005020000940305001012407030"

    # field_str = "000801005900000010700000002070000000003000100010040200007400000000000068008706000"
    # field_str = '000061050008000210000250003700000030003815900020000005200087000034000800070390000'
    # field_str = '000097006500200104300001070093805007000010000400706590040100009802009001900640000'

    # With naked pair
    # field_str = "530007108100580004080000509803915007657000981000670005000800750000409810200700490"

    # With restricted value on square
    field_str = "000801005900000010701000002070000000003000100010040200007400000000000068008706000"

    fld = Field_np()
    fld.enter_values(field_str)
    fld.solve()

    # from num_field import array_to_clipboard

    # array_to_clipboard(fld.cast_to_99_shape())
