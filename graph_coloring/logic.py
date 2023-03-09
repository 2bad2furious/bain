import random
import sys

import networkx as nx
import numpy as np
import numpy.random


def n_conflicts(g: nx.Graph, cols: list[int]) -> dict[int, int]:
    collisions: dict[int, int] = dict()
    for node in g.nodes:
        node_col = cols[node]
        for neighbor_node in g.neighbors(node):
            neighbor_col = cols[neighbor_node]
            if neighbor_col == node_col:
                collisions[node] = collisions.get(node, 0) + 1
    return collisions


def is_ok(g: nx.Graph, cols: list[int]) -> bool:
    return len(n_conflicts(g, cols)) == 0


def change_cols_at_max(cols: list[int], options: list[int], at: int, g: nx.Graph) -> list[int]:
    taken_colors = set([cols[neighbor_loc] for neighbor_loc in g.neighbors(at)])
    free_colors = set(cols).difference(taken_colors)
    if len(free_colors) == 0:
        free_colors = options # if none are free, just pick a random
    pos1 = random.randint(0, len(free_colors) - 1)
    cols[at] = list(free_colors)[pos1]
    return cols


def change_cols_at_random(cols: list[int], options: list[int]) -> list[int]:
    pos1 = random.randint(0, len(options) - 1)
    pos2 = random.randint(0, len(cols) - 1)
    cols[pos2] = options[pos1]
    return cols

default_conflicts = {0: 0}


def pick_random(max_ats: list[int]):
    i = random.randint(0, len(max_ats) - 1)
    return max_ats[i]

def color(g: nx.Graph, k: int, steps: int) -> tuple[list[int], bool, int]:
    options = list(range(k))
    cols = np.random.choice(k, len(g.nodes))
    solved = False
    taken_steps = 0
    conflicts = default_conflicts
    min_max_conflicts = sys.maxsize
    while not solved and taken_steps < steps:
        max_conflicts = max(conflicts.values())
        max_ats = [k for k,v in conflicts.items() if v == max_conflicts]
        if max_conflicts < min_max_conflicts and conflicts is not default_conflicts:
            min_max_conflicts = max_conflicts
        taken_steps += 1
        max_at = pick_random(max_ats)
        cols = change_cols_at_max(cols, options, max_at, g)
        # conflicts = n_conflicts(g, cols)
        conflicts = n_conflicts(g, cols)
        solved = len(conflicts) == 0
    return cols, solved, min_max_conflicts
