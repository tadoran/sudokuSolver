import requests as r


def get_from_web(difficulty: int = 1):
    req = r.get("http://www.cs.utep.edu/cheon/ws/sudoku/new/", params={"level": difficulty, "size": 9})
    if req.ok:
        return req.json()
    else:
        return None


def matrix_from_web(json_load: dict):
    squares = json_load.get('squares', None)
    if not squares:
        return None

    field = [[0 for x in range(9)] for y in range(9)]
    for el in squares:
        field[el['y']][el['x']] = el['value']
    return field


if __name__ == '__main__':
    req = get_from_web(3)
    print(req)
