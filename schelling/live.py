from __future__ import annotations

import _thread
import datetime
import threading
import time

from schelling.classes import Schelling, Grid
from schelling.utils import run, print_grid, print_data

done = False

grid = Grid.generate(ratios=(4.8, 4.8, .6),size=70)
schelling = Schelling(grid, tol=.65, radius=3)
data = ()

print_grid(schelling)


def run_schelling():
    global schelling
    global data
    for progress in run(schelling, top_pct=.95, limit=grid.size *3):
        schelling = progress
        data = data + (schelling.happy_count,)
    global done
    done = True


def show_scatter():
    while not done:
        print_grid(schelling)
        time.sleep(1)




start = datetime.datetime.now()
schelling_thread = _thread.start_new_thread(run_schelling, ())
scatter_thread = _thread.start_new_thread(show_scatter, ())
#plot_thread = _thread.start_new_thread(show_plot, ())

while not done:
    pass

end = datetime.datetime.now()
delta = end - start

print_grid(schelling)
print_data(data)

print(f"started at {start.isoformat()}")
print(f"ended at {end.isoformat()}")
print(f"this took {delta.total_seconds()} seconds")

# run_dash()
