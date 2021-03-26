def simple_tab_delimited(matrix: list):
    vals = [
        [6, 0, 0, 0, 9, 7, 0, 4, 0],
        [7, 0, 8, 0, 0, 0, 9, 6, 3],
        [0, 1, 9, 0, 3, 0, 7, 0, 5],
        [5, 8, 0, 4, 0, 0, 2, 9, 6],
        [0, 0, 4, 0, 7, 0, 8, 0, 1],
        [0, 6, 1, 0, 0, 0, 0, 3, 0],
        [9, 0, 3, 1, 6, 0, 5, 7, 0],
        [1, 5, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 5, 4, 6, 1, 9]
    ]
    return "\n".join("\t".join(map(str, row)) for row in vals).replace("0", "")


if __name__ == '__main__':
    simple_tab_delimited([])
