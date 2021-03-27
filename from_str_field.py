def parse_field(field_str: str) -> list:
    tbl = {".": "0", "-": "",
           "|": "", " ": ""}
    field_str_cleared = field_str.translate(field_str.maketrans(tbl))
    lst = [[int(el) for el in line] for line in field_str_cleared.split("\n") if len(line) == 9]
    return lst


if __name__ == '__main__':
    txt = """-------------------------------
| .  .  . | .  7  . | 8  4  . |
| .  .  6 | .  .  . | .  .  . |
| .  .  . | .  .  2 | 7  9  . |
-------------------------------
| .  .  . | 9  .  . | .  .  . |
| .  .  . | 3  .  1 | .  .  . |
| 9  .  . | .  .  . | 4  .  . |
-------------------------------
| .  8  . | .  .  9 | .  .  5 |
| 4  .  7 | .  .  . | .  .  3 |
| 1  .  . | .  3  . | .  .  . |
-------------------------------"""
    print("[\n\t" + ",\n\t".join(map(str, parse_field(txt))) + "\n]")
