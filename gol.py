from typing import Tuple, Any

Generation = Tuple[bool]


def neighbors_on(row: Generation, i: int) -> int:
    left_on = row[i - 1] if i > 0 else False
    right_on = row[i + 1] if i < (len(row) - 1) else False
    return left_on + right_on


def step(row: Generation) -> Generation:
    res = []
    for i, on in enumerate(row):
        neighbors_on_count = neighbors_on(row, i)
        if neighbors_on_count == 0:
            res.append(True)
        elif neighbors_on_count == 2:
            res.append(on)
        else:
            res.append(not on)

    return tuple(res)


def printrow(row: Generation) -> None:
    print("\t".join(map(lambda on: "⚪️" if on else "⚫️", row)))


cur_gen1 = [True, False, False, True, True, False, True, False]
cur_gen = [False, True, False, True, True, False, False, True]
for _ in range(100):
    printrow(cur_gen)
    cur_gen = step(cur_gen)
