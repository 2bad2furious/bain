import datetime

from schelling.classes import Schelling, Grid
from schelling.utils import run, print_grid

start = datetime.datetime.now()

grid = Grid.generate((4.7, 4.7, .6),size=100)

schelling = Schelling(grid, tol=.7, radius=2)
#print_grid(schelling)
data = [schelling.happy_count]
i = 0
for s in run(schelling, top_pct=1):
    data.append(schelling.happy_count)
    schelling = s
    i += 1

end = datetime.datetime.now()
delta = end - start
print(f"started at {start.isoformat()}")
print(f"ended at {end.isoformat()}")
print(f"this took {delta.total_seconds()} seconds")
print("total rounds: " + str(i))

print_grid(schelling)
