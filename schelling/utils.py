from datetime import datetime
from typing import Iterable, Callable

import matplotlib.axes as axes
import matplotlib.pyplot as pp

from schelling.classes import Schelling, Coord


class GridData:

    def __init__(self, x: list[float], y: list[float], c: list[str]):
        self.x = x
        self.y = y
        self.c = c


def grid_data_for_scatter(schelling: Schelling) -> GridData:
    x = []
    y = []
    c = []
    for coord in schelling.grid.all_coords():
        x.append(coord.x)
        y.append(coord.y)

        c.append(get_color(schelling, coord))
    return GridData(x, y, c)


def print_grid(schelling: Schelling, pt: axes.Axes = pp):
    pt.title = datetime.now().isoformat()
    data = grid_data_for_scatter(schelling)
    pt.scatter(data.x, data.y, c=data.c)
    pt.show()


def print_data(data: Iterable[int], pt: axes.Axes = pp):
    pt.plot(data)
    pt.show()


def get_color(schelling: Schelling, coord: Coord) -> str:
    value = schelling.grid[coord]
    if schelling.grid.is_empty(coord):
        return 'black'

    unhappy = schelling.is_unhappy(coord)
    # TODO check agent type count in schelling
    if value == 1:
        if unhappy:
            return 'pink'
        else:
            return 'red'
    else:
        if unhappy:
            return 'lightblue'
        else:
            return 'blue'


def run_lambda(schelling: Schelling, on_each: Callable[[Schelling], None]):
    actual = schelling
    on_each(actual)
    while not actual.are_all_happy:
        actual = actual.next()
        on_each(actual)

def run(schelling: Schelling, top_pct=.95, limit: int = 1000):
    i = 0

    crossed_top_pct = False
    count_after_crossed = 0
    stop = False
    actual = schelling
    while not actual.are_all_happy: #and count_after_crossed < limit and not stop:
        actual = actual.next()
        yield actual
        i += 1

        # happy_ratio = actual.happy_ratio
        # if not crossed_top_pct and happy_ratio > top_pct:
        #     crossed_top_pct = True
        # elif crossed_top_pct:
        #     count_after_crossed += 1

      #  limit_str = "" if count_after_crossed == 0 else f" crossed top {count_after_crossed}/{limit}"
        #print(
     #       "rounds " + str(i) + ", happy: " + str(actual.happy_count) + "/" + str(actual.agent_count) + limit_str)

    #print("total rounds = " + str(i))
