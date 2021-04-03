from collections.abc import Iterable
from itertools import repeat


def string_mutations(input_str: str, positions_to_replace: tuple, values_to_insert: tuple) -> str:
    output_str = input_str
    replace_positions = 1

    if isinstance(positions_to_replace, Iterable):
        replace_positions = len(positions_to_replace)
        for pos in sorted(positions_to_replace, reverse=True):
            output_str = output_str[:pos] + "{}" + output_str[pos + 1:]
    else:
        pos = positions_to_replace
        output_str = output_str[:pos] + "{}" + output_str[pos + 1:]

    for insert_values in values_to_insert:
        if isinstance(insert_values, Iterable) and not isinstance(insert_values, str):
            yield output_str.format(*insert_values)
        else:
            yield output_str.format(*repeat(insert_values, times=replace_positions))


def difference_indices(first_string: str, second_string: str) -> list:
    assert len(first_string) == len(second_string), "Strings must be of same size"

    differences = []
    for i, el in enumerate(first_string):
        if el != second_string[i]:
            differences.append(i)
    return differences
