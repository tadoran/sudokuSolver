def parse_field(field_str: str) -> list:
    tbl = {".": "0", "-": "",
           "|": "", " ": ""}
    field_str_cleared = field_str.translate(field_str.maketrans(tbl))
    lst = [[int(el) for el in line] for line in field_str_cleared.split("\n") if len(line) == 9]
    return lst


if __name__ == '__main__':
    txt = """| 6  .  . | 5  .  2 | .  .  . |
| .  .  9 | .  .  . | .  .  . |
| 4  .  2 | .  7  . | .  5  . |
-------------------------------
| 2  .  . | .  .  5 | .  3  . |
| .  .  8 | .  .  . | 9  .  . |
| .  .  . | 7  .  . | .  .  5 |
-------------------------------
| .  2  . | .  5  . | .  .  . |
| .  6  . | .  .  . | .  1  7 |
| .  4  . | .  .  . | .  .  3 |
-------------------------------"""
    print("[\n\t" + ",\n\t".join(map(str, parse_field(txt))) + "\n]")
