from __future__ import annotations

from functools import cached_property, cache
from typing import Callable

import numpy as np

from schelling.base_types import Agent, Tolerance, Radius

def_rng = np.random.default_rng()


class DividedCoords:

    def __init__(self, happy_coords: set[Coord], unhappy_coords: set[Coord], empty_coords: set[Coord]):
        self.happy_coords = happy_coords
        self.unhappy_coords = unhappy_coords
        self.empty_coords = empty_coords

    @cached_property
    def happy_count(self):
        return len(self.happy_coords)

    @cached_property
    def agent_count(self):
        return self.happy_count + len(self.unhappy_coords)

    def copy_with_changes(self, prev_agent_coord: Coord, new_agent_coord: Coord, is_now_happy: bool) -> DividedCoords:
        unhappy_coords = self.unhappy_coords.copy()
        unhappy_coords.remove(prev_agent_coord)

        empty_coords = self.empty_coords.copy()
        empty_coords.remove(new_agent_coord)
        empty_coords.add(prev_agent_coord)

        happy_coords = self.happy_coords

        if is_now_happy:
            happy_coords = happy_coords.copy()
            happy_coords.add(new_agent_coord)
        else:
            unhappy_coords.add(new_agent_coord)

        return DividedCoords(happy_coords, unhappy_coords, empty_coords)

    @cached_property
    def are_all_happy(self):
        return not self.unhappy_coords

    @classmethod
    def from_grid(cls, grid: Grid, is_unhappy: Callable[[Coord], bool]) -> DividedCoords:
        empty_coords = set()
        happy_coords = set()
        unhappy_coords = set()

        for coord in grid.all_coords():
            if grid[coord] == grid.empty:
                empty_coords.add(coord)
                continue

            is_happy = not is_unhappy(coord)
            if is_happy:
                happy_coords.add(coord)
            else:
                unhappy_coords.add(coord)

        return DividedCoords(happy_coords, unhappy_coords, empty_coords)


class Coord:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __repr__(self):
        return f"\u007bx:{self.x} y:{self.y}\u007d"

    def as_tuple(self):
        return self.y, self.x

    def with_diff(self, x_diff: int, y_diff: int) -> Coord:
        return Coord(self.x + x_diff, self.y + y_diff)

    def bound_by(self, shape) -> Coord:
        return Coord(self.x % shape[1], self.y % shape[0])

    def _key(self):
        return self.as_tuple()

    def __eq__(self, other):
        return isinstance(other, Coord) and other._key() == self._key()

    def __hash__(self):
        return hash(self._key())


class Grid:
    def __init__(self, arr: np.ndarray, agent_type_count, empty: Agent):
        self.agent_type_count = agent_type_count
        self.arr = arr
        self.empty = empty

    @cached_property
    def size(self):
        return self.arr.size

    @cached_property
    def shape(self):
        return self.arr.shape

    def all_coords(self):
        for x in range(0, self.shape[1]):
            for y in range(0, self.shape[0]):
                yield Coord(x, y)

    def __getitem__(self, item: Coord):
        return self.arr[item.as_tuple()]

    def clone_with_switch(self, empty_coord: Coord, agent_coord: Coord):
        copy = Grid(self.arr.copy(), self.agent_type_count, self.empty)
        copy.arr[agent_coord.as_tuple()] = self.empty
        copy.arr[empty_coord.as_tuple()] = self[agent_coord]
        return copy

    @staticmethod
    def generate(ratios=(4.5, 4.5, 1), size: int = 70, rng=def_rng) -> Grid:
        ratio_sum = sum(ratios)
        size_squared = size ** 2
        empty = len(ratios) - 1
        nums = [np.repeat(i, (rat / ratio_sum) * size_squared) for i, rat in enumerate(ratios)]
        total_size = sum(map(lambda num: num.size, nums))

        missing = size_squared - total_size
        if missing > 0:
            nums.append(np.repeat(empty, missing))

        concatenated = np.concatenate(nums)
        rng.shuffle(concatenated)
        rng.shuffle(concatenated)
        grid = concatenated.reshape((size, size))
        return Grid(grid, len(ratios) - 1, empty)

    def is_empty(self, coord: Coord):
        return self[coord] == self.empty


class Schelling:

    def __init__(self, grid: Grid, divided_coords: DividedCoords = None, rng=def_rng, tol: Tolerance = .7,
                 radius: Radius = 3):
        self.grid = grid
        self.rng = rng
        self.tol = tol
        self.radius = radius
        if divided_coords is None:
            divided_coords = DividedCoords.from_grid(grid, lambda c: self._is_unhappy(c))
        self._divided_coords = divided_coords

    @property
    def agent_count(self):
        return self._divided_coords.agent_count

    @cached_property
    def happy_count(self):
        return len(self._divided_coords.happy_coords)

    @cached_property
    def are_all_happy(self) -> bool:
        return self._divided_coords.are_all_happy

    @cached_property
    def happy_ratio(self):
        return self.happy_count / self._divided_coords.agent_count

    @cache
    def _ratio(self, c: Coord, grid=None):
        grid = self.grid if grid is None else grid

        shape = grid.shape
        same_agent_count = 1
        total_agent_count = 1

        current = grid[c]

        r = range(-self.radius, self.radius + 1)
        for x_diff in r:
            for y_diff in r:
                if y_diff == 0 and x_diff == 0:
                    continue

                bound_coord = c \
                    .with_diff(x_diff, y_diff) \
                    .bound_by(shape)

                agent = grid[bound_coord]
                if agent != grid.empty:
                    total_agent_count += 1
                    if agent == current:
                        same_agent_count += 1

        return same_agent_count / total_agent_count

    def is_unhappy(self, c: Coord) -> bool:
        return c in self._divided_coords.unhappy_coords

    def _is_unhappy(self, c: Coord, grid=None) -> bool:
        grid = self.grid if grid is None else grid
        return self._ratio(c, grid) < self.tol

    @property
    def _all_unhappy_coords(self, ):
        return self._divided_coords.unhappy_coords

    @property
    def _all_empty_coords(self, ):
        return self._divided_coords.empty_coords

    def next(self):
        unhappy_agent_coords = self._all_unhappy_coords
        unhappy_agent_coords_count = len(unhappy_agent_coords)
        if unhappy_agent_coords_count == 0:
            return self

        new_agent_coord = self.rng.choice(tuple(self._all_empty_coords))
        prev_agent_coord = self.rng.choice(tuple(unhappy_agent_coords))

        copy = self.grid.clone_with_switch(new_agent_coord, prev_agent_coord)

        is_now_happy = not self._is_unhappy(new_agent_coord, copy)
        div_coords = self._divided_coords.copy_with_changes(prev_agent_coord, new_agent_coord, is_now_happy)
        return Schelling(copy, div_coords, self.rng, self.tol, self.radius)
