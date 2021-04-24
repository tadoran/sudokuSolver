import numpy as np

from fieldMap import FieldMap


def array_to_clipboard(x: np.array) -> None:
    import pandas as pd
    df = pd.DataFrame(x)
    df.to_clipboard(index=False, header=False)


if __name__ == '__main__':
    field_str = "000801005900000010700000002070000000003000100010040200007400000000000068008706000"

    fld = np.array([ch for ch in field_str], dtype='int8')
    fld_vals = fld
    fld = np.vstack([fld, np.tile(np.ones_like(fld_vals), (9, 1))])
    fld[1:, :][0:, fld[0, :] > 0] = 0

    # twoDfld = fld_vals.reshape(9, 9)
    # twoDfld2 = np.arange(81).reshape(9, 9)

    # aa = np.where(twoDfld == 0)
    # print(fld)

    fld_map = FieldMap()

    print(fld_map.squares_h_excl(61))
    # print(fld_map.row_excl[1])
    print(fld_map)
    # all_rows = {k: row(k) for k in range(9)}
    # all_cols = {k: column(k) for k in range(9)}
    # all_squares = {(y, x): square(y * 3, x * 3) for y in range(3) for x in range(3)}
    #
    # point_mappings = {k: point_mapping(k) for k in range(81)}
    #
    # pointer = 0
    # for key, val in point_mappings[0].items():
    #     print(key, range(pointer, pointer + len(val)))
    #     pointer += len(val)
    #
    # point_mappings_np = np.vstack(
    #     [np.array(tuple(chain(*pt_items.values())), dtype='int8') for pt_items in point_mappings.values()])
    # # print(point_mappings)
