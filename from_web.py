import requests as r


# from main import Field


def get_from_web(difficulty: int = 1):
    req = r.get("http://www.cs.utep.edu/cheon/ws/sudoku/new/", params={"level": difficulty, "size": 9})
    if req.ok:
        return req.json()
    else:
        return None


def fill_field_from_web(field, json_load: dict):
    squares = json_load.get('squares', None)
    if not squares:
        return None
    for el in squares:
        field.field[el['y']][el['x']].value = el['value']
    return field


if __name__ == '__main__':
    req = get_from_web(2)
    print(req)
