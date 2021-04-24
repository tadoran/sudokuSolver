from itertools import chain

import numpy as np


class FieldMap:
    def row(self, row_num: int) -> tuple:
        assert 0 <= row_num < 9
        return tuple(range(row_num * 9, row_num * 9 + 9))

    def column(self, col_num: int) -> tuple:
        assert 0 <= col_num < 9
        return tuple(range(0 + col_num, 9 * 9 + col_num, 9))

    def square(self, row_num: int, col_num: int) -> tuple:
        assert 0 <= row_num < 9
        assert 0 <= col_num < 9

        return tuple(y * 9 + x
                     for y in range(3 * (row_num // 3), 3 * (row_num // 3) + 3)
                     for x in range(3 * (col_num // 3), 3 * (col_num // 3) + 3)
                     )

    def pos_by_row_column(self, row: int, column: int) -> int:
        return row * 9 + column

    def row_column_by_pos(self, index) -> tuple:
        return index // 9, index % 9

    def point_mapping(self, index: int) -> dict:
        self.all_rows = {k: self.row(k) for k in range(9)}
        self.all_cols = {k: self.column(k) for k in range(9)}
        self.all_squares = {(y, x): self.square(y * 3, x * 3) for y in range(3) for x in range(3)}

        d = {}

        d['row_all'] = self.all_rows[index // 9]
        d['row_excl'] = tuple(filter(lambda x: x != index, d['row_all']))

        d['column_all'] = self.all_cols[index % 9]
        d['column_excl'] = tuple(filter(lambda x: x != index, d['column_all']))

        d['square_all'] = self.all_squares[(index // 9) // 3, (index % 9) // 3]
        d['square_excl'] = tuple(filter(lambda x: x != index, d['square_all']))

        d['related_all'] = list(set(chain(d['row_all'], d['column_all'], d['square_all'])))
        d['related_excl'] = tuple(filter(lambda x: x != index, d['related_all']))

        d['squares_v_all'] = tuple(sorted(r * 9 + el + (index % 9) // 3 * 3 for el in range(3) for r in range(9)))
        d['squares_v_excl'] = tuple(filter(lambda x: x != index, d['squares_v_all']))

        d['squares_h_all'] = tuple(range(27 * (index // 27), 27 * (index // 27) + 27))
        d['squares_h_excl'] = tuple(filter(lambda x: x != index, d['squares_h_all']))

        return d

    def __init__(self):
        # print(f"FieldMap():")
        point_mappings = {k: self.point_mapping(k) for k in range(81)}

        pointer = 0
        for key, val in point_mappings[0].items():
            # print(f"\t{key}: {range(pointer, pointer + len(val))}")
            self.__dict__["_" + key + "_range"] = range(pointer, pointer + len(val))
            pointer += len(val)

        self._point_mappings_np = np.vstack(
            [np.array(tuple(chain(*pt_items.values())), dtype='int8') for pt_items in point_mappings.values()])

    def __getattr__(self, name):
        attr_range = self.__dict__.get("_" + name + "_range", None)
        if attr_range:
            # return self._point_mappings_np[:, attr_range]
            return lambda n: self._point_mappings_np[n, attr_range]
        else:
            raise AttributeError(f"No attribute named {name}")


if __name__ == '__main__':
    fld_map = FieldMap()
    pt_pos = 72

    print()
    print(f"pt_pos: {pt_pos}")
    row, column = fld_map.row_column_by_pos(pt_pos)
    print(f"row_column_by_pos: {(row, column)}")
    print(f"pos_by_row_column: {fld_map.pos_by_row_column(row, column)}")
    print(f"row_all: {fld_map.row_all(pt_pos)}")
    print(f"column_all: {fld_map.column_all(pt_pos)}")
    print(f"square_all: {fld_map.square_all(pt_pos)}")

    print(f"square_excl: {fld_map.square_excl(pt_pos)}")
    print(f"related_all: {fld_map.related_excl(pt_pos)}")
