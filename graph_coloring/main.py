import datetime
from math import floor, ceil

from graph_coloring.logic import color
from graph_coloring.utils import readdimacs, plot

graphs = {
    'dsjc250.5.col': 28,
    'dsjc125.9.col': 44,
    'dsjc125.1.col': 5,
    'dsjc500.1.col': 12,
    'dsjc1000.9.col': 223
}

path = 'dsjc125.9.col'

Gd = readdimacs(path)
print(f"nodes: {len(Gd.nodes)}")
print(f"edges: {len(Gd.edges)}")

known_best = graphs[path]
best = 60#len(Gd.nodes)
decrease_ratio = 0.9
repeating_power_exp = 1.15
repeating_steps = 1
edges_count = len(Gd.edges)
repeating_power = 1
max_steps_repeating = 5

while best > known_best:
    steps = ceil(edges_count ** repeating_power)
    for k in range(max(known_best, floor(best * decrease_ratio)), best):
        print(f"Trying k={k}, repeating_power={repeating_power}, repeating_steps={repeating_steps} steps={steps}, best {best}")
        start = datetime.datetime.now()
        cols, solved, min_max_conflicts, min_conflicts = color(Gd, k, steps)
        end = datetime.datetime.now()
        delta = end - start
        print(
            f"solved: {solved} k: {k}, min_max_conflicts: {min_max_conflicts}, min_conflicts={min_conflicts} took {delta.total_seconds()} s")
        if solved:
            print(f"cols {cols}")
            plot(Gd, cols)
            best = k
            repeating_power = 1
            repeating_steps = 1
            break
    else: # if did not break, repeat same steps some more
        repeating_steps += 1
        if repeating_steps >= max_steps_repeating: # increase the amount of steps
            print("Increasing repeating power")
            repeating_power = round(repeating_power * repeating_power_exp, 2)
            repeating_steps = 1
