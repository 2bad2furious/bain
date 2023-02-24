import math
from datetime import datetime
from typing import Callable, Tuple

import numpy
import numpy as np
import matplotlib.pyplot as pp
import matplotlib.animation as animation
import matplotlib.axes as axes

from collections.abc import Sequence

rng = np.random.default_rng()
Grid = np.ndarray
Tolerance = float
Ratio = float
Count = int
Radius = int
EMPTY = 0
AGENT_1 = 1
AGENT_2 = 2
RADIUS = 1


class NoMoreUnhappy(Exception):
    pass


class Coord:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.y, self.x


def ratio(arr: Grid, coord: Coord, rad: Radius = RADIUS) -> Ratio:
    shape = arr.shape
    same_count = 1
    total_count = 1

    current = arr[coord.as_tuple()]

    for x_diff in range(-rad, rad + 1):
        for y_diff in range(-rad, rad + 1):
            if y_diff == 0 and x_diff == 0:
                continue

            x = x_diff + coord.x
            if x < 0:
                x += shape[1]
            y = y_diff + coord.y
            if y < 0:
                y += shape[0]

            item = arr[y % shape[0], x % shape[1]]
            if item != EMPTY:
                total_count += 1
                if item == current:
                    same_count += 1

    return same_count / total_count


def all_coords(grid: Grid) -> Sequence[Coord]:
    for x in range(0, grid.shape[1]):
        for y in range(0, grid.shape[0]):
            yield Coord(x, y)


def random_first(grid: Grid, predicate: Callable[[Coord], bool]) -> Coord:
    a = list(filter(predicate, all_coords(grid)))
    return rng.choice(a)


def unhappy_coord_and_all(grid: Grid, tol: Tolerance) -> Tuple[Coord, int]:
    a = list(filter(lambda c: grid[c.as_tuple()] != EMPTY and is_unhappy(grid, c, tol), all_coords(grid)))
    count = len(a)
    if count == 0:
        raise NoMoreUnhappy()
    chosen = rng.choice(np.array(a))
    return chosen, count


def empty_space_coord(grid: Grid) -> Coord:
    return random_first(grid, lambda c: grid[c.as_tuple()] == EMPTY)


def is_unhappy(grid: Grid, coord: Coord, tol: Tolerance) -> bool:
    rat = ratio(grid, coord)
    return rat < tol


def count_unhappy(arr: Grid, tol: Tolerance) -> Count:
    shape = arr.shape
    unhappy = 0
    for y in range(shape[0]):
        for x in range(shape[1]):
            unhappy += is_unhappy(arr, Coord(x, y), tol)

    return unhappy


def print_grid(grid: Grid, tol: Tolerance, pt: axes.Axes=pp):
    x = []
    y = []
    c = []
    for coord in all_coords(grid):
        x.append(coord.x)
        y.append(coord.y)

        c.append(get_color(grid, coord, tol))

    pt.title = datetime.now().isoformat()
    pt.scatter(x, y, c=c)
    pt.show()
    print("updating")


def get_color(grid: Grid, coord: Coord, tol: Tolerance) -> str:
    value = grid[coord.as_tuple()]
    if value == EMPTY:
        return 'black'

    unhappy = is_unhappy(grid, coord, tol)
    if value == AGENT_1:
        if unhappy:
            return 'pink'
        else:
            return 'red'
    else:
        if unhappy:
            return 'lightblue'
        else:
            return 'blue'


def step(arr: Grid, tol: Tolerance) -> tuple[Grid, Count]:
    try:
        agent_coord, unhappy_count = unhappy_coord_and_all(grid, tol)
    except NoMoreUnhappy:
        return arr, arr.size
    empty_coord = empty_space_coord(grid)

    copy = arr.copy()
    copy[agent_coord.as_tuple()] = EMPTY
    copy[empty_coord.as_tuple()] = arr[agent_coord.as_tuple()]
    return copy, arr.size - unhappy_count


def generate_grid(size: int, empty_ratio: float):
    agent_ratio = (1 - empty_ratio) / 2
    agent_count = math.ceil(agent_ratio * size ** 2)

    agent1_nums = np.repeat(AGENT_1, agent_count)
    agent2_nums = np.repeat(AGENT_2, agent_count)
    empty_count = size ** 2 - agent_count * 2
    empty_nums = np.repeat(0, empty_count)

    concatenated = np.concatenate([agent1_nums, agent2_nums, empty_nums])
    rng.shuffle(concatenated)
    grid = concatenated.reshape((size, size))
    return grid


if __name__ == '__main__':
    size = 70
    RADIUS = 3  # TODO pass as param
    grid = generate_grid(size, 0.1)
    data = []
    happy_count = 0
    tol = 0.7
    limit = 1000
    top_pct = .95
    i = 0

    print_grid(grid, tol)

    crossed_top_pct = False
    count_after_crossed = 0
    stop = False
    while happy_count != grid.size and count_after_crossed < limit and not stop:
        grid, happy_count = step(grid, tol)
        data.append(happy_count)
        i += 1

        happy_ratio = happy_count / size ** 2
        if not crossed_top_pct and happy_ratio > top_pct:
            crossed_top_pct = True
        elif crossed_top_pct:
            count_after_crossed += 1

        limit_str = "" if count_after_crossed == 0 else f" crossed top {count_after_crossed}/{limit}"
        print("rounds " + str(i) + ", happy: " + str(happy_count) + "/" + str(grid.size) + limit_str)

    pp.plot(data)
    pp.show()

    print_grid(grid, tol)

    print("total rounds = " + str(i))
