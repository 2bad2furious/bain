from __future__ import annotations

import _thread
import datetime
import time

from schelling.classes import Schelling, Grid
from schelling.utils import run, print_grid, print_data

done = False

grid = Grid.generate(ratios=(4.7, 4.7, .6), size=100)
schelling = Schelling(grid, tol=.7, radius=2)
data = ()

print_grid(schelling)

i = 0


def run_schelling():
    global schelling
    global data
    global done
    global i

    for s in run(schelling):
        schelling = s
        i += 1
    done = True


def show_scatter():
    while not done:
        print_grid(schelling)
        time.sleep(1)


start = datetime.datetime.now()

# schelling_thread = _thread.start_new_thread(run_schelling, ())
scatter_thread = _thread.start_new_thread(show_scatter, ())


# plot_thread = _thread.start_new_thread(show_plot, ())

def print_stats():
    while not done:
        s = schelling
        rounds = i
        print(f"rounds: {rounds}, happy: {s.happy_count}/{s.agent_count}")
        time_passed = datetime.datetime.now() - start
        print(f"time passed {round(time_passed.total_seconds())} s")
        time.sleep(5)


_thread.start_new_thread(print_stats, ())
try:

    run_schelling()
except KeyboardInterrupt as e:
    done = False
    raise e

end = datetime.datetime.now()
delta = end - start

print_grid(schelling)
print_data(data)

print(f"started at {start.isoformat()}")
print(f"ended at {end.isoformat()}")
print(f"this took {round(delta.total_seconds())} seconds")

# run_dash()
