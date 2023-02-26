from __future__ import annotations

import _thread

from schelling.classes import Schelling, Grid
from schelling.utils import run, print_grid, print_data

done = False

grid = Grid.generate()
schelling = Schelling(grid)
data = []

print_grid(schelling)


def run_schelling():
    global schelling
    for progress in run(schelling):
        schelling = progress
        data.append(schelling.happy_count)
    global done
    done = True


def show_scatter():
    while True:
        print("printing")
        s = schelling
        print_grid(s)
        if data:
            print_data(data)


schelling_thread = _thread.start_new_thread(run_schelling, ())
# scatter_thread = _thread.start_new_thread(show_scatter, ())

while not done:
    pass

print_grid(schelling)
print_data(data)

# run_dash()
