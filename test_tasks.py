from random import randint


class FieldVals:
    def __init__(self):
        self.vals = {}

    def add(self, vals: list, comment: str = "Default"):
        container = self.vals.get(comment, [])
        container.append(vals)
        self.vals[comment] = container

    def get_all(self, tag: str = ""):
        if tag == "":
            all_list = []
            for key, el in self.vals.items():
                all_list.extend(el)
            return all_list
        else:
            container = self.vals.get(tag, [])
            return container

    def get_one_random(self, tag: str = ""):
        all = self.get_all(tag)
        return all[randint(0, len(all) - 1)]


def load_FieldVals():
    fv = FieldVals()

    fv.add([[0, 6, 0, 8, 0, 3, 5, 9, 0],
            [1, 0, 0, 5, 0, 2, 0, 6, 7],
            [0, 0, 0, 0, 9, 0, 1, 0, 0],
            [0, 9, 0, 0, 0, 0, 7, 2, 0],
            [8, 0, 0, 6, 0, 9, 0, 0, 3],
            [0, 5, 6, 0, 0, 0, 0, 1, 0],
            [0, 0, 5, 0, 2, 0, 0, 0, 0],
            [9, 4, 0, 3, 0, 5, 0, 0, 1],
            [0, 1, 2, 4, 0, 7, 0, 3, 0]
            ])

    fv.add([[0, 0, 0, 0, 6, 1, 0, 5, 0],
            [0, 0, 8, 0, 0, 0, 2, 1, 0],
            [0, 0, 0, 2, 5, 0, 0, 0, 3],
            [7, 0, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 3, 8, 1, 5, 9, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 5],
            [2, 0, 0, 0, 8, 7, 0, 0, 0],
            [0, 3, 4, 0, 0, 0, 8, 0, 0],
            [0, 7, 0, 3, 9, 0, 0, 0, 0]
            ])

    fv.add([[0, 0, 0, 0, 9, 7, 0, 0, 6],
            [5, 0, 0, 2, 0, 0, 1, 0, 4],
            [3, 0, 0, 0, 0, 1, 0, 7, 0],
            [0, 9, 3, 8, 0, 5, 0, 0, 7],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [4, 0, 0, 7, 0, 6, 5, 9, 0],
            [0, 4, 0, 1, 0, 0, 0, 0, 9],
            [8, 0, 2, 0, 0, 9, 0, 0, 1],
            [9, 0, 0, 6, 4, 0, 0, 0, 0]
            ])

    fv.add([[0, 0, 0, 8, 5, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 7, 6, 0, 8],
            [8, 4, 0, 0, 0, 0, 7, 0, 0],
            [0, 0, 0, 0, 2, 0, 4, 6, 3],
            [4, 0, 0, 0, 0, 0, 0, 0, 9],
            [6, 1, 2, 0, 3, 0, 0, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 4, 2],
            [3, 0, 5, 7, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 8, 9, 0, 0, 0]
            ])

    fv.add([[0, 8, 0, 0, 9, 4, 0, 0, 0],
            [0, 0, 9, 1, 7, 0, 0, 0, 0],
            [4, 0, 1, 0, 0, 0, 0, 0, 3],
            [0, 0, 8, 0, 0, 0, 0, 2, 0],
            [5, 0, 0, 9, 1, 3, 0, 0, 8],
            [0, 9, 0, 0, 0, 0, 4, 0, 0],
            [3, 0, 0, 0, 0, 0, 8, 0, 6],
            [0, 0, 0, 0, 5, 8, 2, 0, 0],
            [0, 0, 0, 2, 3, 0, 0, 4, 0]
            ])

    fv.add([[0, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 6, 2, 7, 0],
            [0, 0, 4, 0, 0, 0, 1, 0, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 8, 0, 0, 0],
            [0, 0, 7, 5, 0, 0, 0, 0, 9],
            [5, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 9, 6, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 8, 1, 0, 2, 0]
            ])

    fv.add([[0, 0, 3, 0, 0, 6, 7, 0, 0],
            [0, 0, 0, 0, 7, 0, 3, 0, 6],
            [0, 9, 7, 0, 2, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 5, 0],
            [1, 2, 0, 0, 6, 0, 0, 0, 7],
            [0, 7, 0, 4, 0, 2, 0, 0, 3],
            [0, 8, 2, 6, 0, 1, 0, 0, 0],
            [0, 0, 0, 2, 3, 0, 8, 0, 1],
            [4, 0, 0, 0, 0, 7, 0, 6, 0]
            ])

    fv.add([[0, 0, 0, 8, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 1, 0, 0, 4, 0, 0, 0, 0],
            [8, 0, 0, 0, 0, 0, 0, 0, 7],
            [0, 0, 0, 6, 0, 8, 0, 0, 0],
            [0, 0, 4, 0, 0, 9, 2, 3, 0],
            [4, 0, 0, 0, 3, 0, 0, 0, 0],
            [0, 7, 0, 9, 0, 6, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 2, 0]
            ])

    fv.add([[0, 0, 0, 4, 0, 0, 0, 9, 0],
            [0, 0, 0, 0, 7, 8, 0, 0, 5],
            [0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 9, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 9, 2, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 0, 8, 0],
            [0, 7, 0, 0, 0, 0, 8, 0, 0],
            [6, 0, 0, 0, 4, 0, 9, 0, 0],
            [0, 1, 0, 0, 0, 9, 0, 0, 6]
            ])

    # This one was bruteforced
    fv.add([[1, 0, 0, 5, 0, 0, 7, 0, 0],
            [3, 0, 7, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 9, 0, 0, 5, 0, 0, 0, 0],
            [0, 2, 0, 3, 6, 0, 0, 8, 0],
            [0, 0, 0, 0, 2, 0, 0, 6, 0],
            [9, 0, 2, 0, 0, 0, 4, 7, 0],
            [0, 1, 0, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 8, 0, 0]
            ], "Bruteforced")

    # Crapy solution
    fv.add([[7, 0, 0, 5, 1, 0, 0, 0, 6],
            [1, 9, 0, 0, 7, 0, 0, 5, 0],
            [4, 0, 6, 9, 0, 2, 7, 0, 1],
            [0, 0, 2, 0, 0, 0, 8, 1, 9],
            [0, 0, 0, 4, 3, 1, 0, 0, 0],
            [0, 0, 0, 8, 2, 9, 0, 4, 7],
            [0, 6, 0, 7, 0, 8, 0, 2, 0],
            [0, 7, 0, 0, 4, 3, 0, 9, 5],
            [2, 0, 9, 0, 6, 0, 4, 7, 8]
            ], "Crapy solution")

    # Crapy solution
    fv.add([[6, 0, 0, 0, 9, 7, 0, 4, 0],
            [7, 0, 8, 0, 0, 0, 9, 6, 3],
            [0, 1, 9, 0, 3, 0, 7, 0, 5],
            [5, 8, 0, 4, 0, 0, 2, 9, 6],
            [0, 0, 4, 0, 7, 0, 8, 0, 1],
            [0, 6, 1, 0, 0, 0, 0, 3, 0],
            [9, 0, 3, 1, 6, 0, 5, 7, 0],
            [1, 5, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 5, 4, 6, 1, 9]
            ], "Crapy solution")

    fv.add([[5, 0, 0, 9, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 5],
            [1, 0, 0, 0, 7, 0, 0, 0, 6],
            [0, 5, 1, 0, 0, 6, 0, 0, 0],
            [0, 0, 8, 0, 5, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 0, 5, 8, 0],
            [0, 0, 0, 0, 4, 5, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 7, 0, 0],
            [0, 0, 5, 0, 0, 0, 6, 0, 0]
            ], "Solved")

    fv.add([[0, 3, 0, 0, 0, 0, 0, 6, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 4],
            [5, 0, 0, 0, 0, 0, 7, 2, 0],
            [0, 0, 0, 0, 0, 6, 0, 7, 0],
            [0, 9, 0, 5, 0, 3, 0, 0, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 6, 0, 9, 0, 0],
            [0, 0, 4, 2, 0, 0, 0, 5, 0],
            [0, 0, 6, 0, 0, 0, 4, 0, 0]
            ], "Solved")

    fv.add([[0, 0, 0, 0, 0, 5, 9, 0, 0],
            [0, 2, 0, 0, 0, 9, 0, 3, 0],
            [4, 9, 0, 0, 3, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [8, 0, 0, 0, 1, 0, 0, 0, 3],
            [0, 0, 4, 0, 0, 0, 0, 0, 9],
            [0, 0, 8, 0, 9, 0, 0, 4, 0],
            [0, 0, 0, 7, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 0, 0, 1, 0]
            ], "10 min")

    # 9 in square 3,2 is possible only in first column. Thus, in squares 1,2 and 2,2 it is not possible at column 3
    fv.add([[0, 0, 4, 0, 7, 0, 5, 0, 0],
            [2, 6, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 2, 9, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 9],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 7, 9, 0, 0, 0, 0],
            [7, 0, 0, 0, 0, 3, 4, 0, 0],
            [0, 5, 0, 0, 0, 0, 0, 9, 0],
            [0, 0, 0, 0, 1, 6, 0, 0, 0]
            ], "Solved")

    fv.add([[0, 0, 0, 2, 0, 9, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 5, 0, 0, 0, 0, 6, 0],
            [0, 5, 0, 0, 8, 0, 0, 0, 9],
            [0, 0, 9, 0, 3, 0, 7, 0, 0],
            [8, 0, 0, 0, 9, 0, 0, 4, 0],
            [0, 3, 0, 0, 0, 0, 4, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 9, 0],
            [0, 0, 0, 8, 0, 5, 0, 0, 0]
            ])

    fv.add([[0, 0, 0, 2, 0, 9, 0, 0, 0],
            [0, 0, 0, 2, 0, 9, 0, 0, 0],
            [0, 0, 0, 2, 0, 9, 0, 0, 0],
            [0, 0, 0, 2, 0, 9, 0, 0, 0],
            [0, 0, 0, 2, 0, 9, 0, 0, 0],
            [0, 0, 0, 2, 0, 9, 0, 0, 0],
            [0, 0, 0, 2, 0, 9, 0, 0, 0],
            [0, 0, 0, 2, 0, 9, 0, 0, 0],
            [0, 0, 0, 2, 0, 9, 0, 0, 0]
            ], "Wrong")

    fv.add([[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ], "Empty")

    fv.add([
        [3, 9, 0, 0, 0, 0, 0, 0, 6],
        [8, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 0, 9, 1, 0, 0, 2, 0],
        [0, 3, 9, 0, 0, 0, 2, 0, 0],
        [2, 0, 0, 1, 3, 9, 0, 0, 0],
        [0, 0, 8, 0, 0, 0, 9, 0, 0],
        [0, 0, 0, 2, 9, 0, 0, 4, 0],
        [0, 4, 0, 0, 0, 0, 0, 9, 2],
        [9, 0, 0, 0, 0, 6, 0, 0, 7]
    ], )

    fv.add([
        [5, 0, 0, 0, 0, 6, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 6],
        [4, 6, 0, 0, 0, 0, 0, 0, 8],
        [2, 1, 0, 0, 5, 0, 0, 0, 0],
        [0, 4, 0, 8, 0, 7, 0, 5, 0],
        [0, 5, 0, 0, 0, 0, 4, 0, 0],
        [0, 0, 4, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 3, 0, 0, 8, 0, 0],
        [0, 0, 5, 0, 0, 2, 7, 0, 0]
    ])

    fv.add([
        [6, 0, 0, 5, 0, 2, 0, 0, 0],
        [0, 0, 9, 0, 0, 0, 0, 0, 0],
        [4, 0, 2, 0, 7, 0, 0, 5, 0],
        [2, 0, 0, 0, 0, 5, 0, 3, 0],
        [0, 0, 8, 0, 0, 0, 9, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 5],
        [0, 2, 0, 0, 5, 0, 0, 0, 0],
        [0, 6, 0, 0, 0, 0, 0, 1, 7],
        [0, 4, 0, 0, 0, 0, 0, 0, 3]
    ])

    fv.add([
        [6, 0, 0, 5, 0, 2, 0, 0, 0],
        [0, 0, 9, 0, 0, 0, 0, 0, 0],
        [4, 0, 2, 0, 7, 0, 0, 5, 0],
        [2, 0, 0, 0, 0, 5, 0, 3, 0],
        [0, 0, 8, 0, 0, 0, 9, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 5],
        [0, 2, 0, 0, 5, 0, 0, 0, 0],
        [0, 6, 0, 0, 0, 0, 0, 1, 7],
        [0, 4, 0, 0, 0, 0, 0, 0, 3]
    ], "Currently unsolvable")

    fv.add([
        [0, 0, 0, 0, 7, 0, 8, 4, 0],
        [0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 7, 9, 0],
        [0, 0, 0, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 3, 0, 1, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 4, 0, 0],
        [0, 8, 0, 0, 0, 9, 0, 0, 5],
        [4, 0, 7, 0, 0, 0, 0, 0, 3],
        [1, 0, 0, 0, 3, 0, 0, 0, 0]
    ], "Currently unsolvable")

    return fv


fv = load_FieldVals()

if __name__ == '__main__':
    # print(fv.get_all(tag="Currently unsolvable")[0])
    # print(fv.get_all()[0])
    print(fv.get_one_random())
    # print(fv.get_one_random(tag="Currently unsolvable"))