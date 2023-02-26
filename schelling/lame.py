from schelling.classes import Schelling, Grid
from schelling.utils import run, print_grid

grid = Grid.generate(size=50,)

schelling = Schelling(grid, tol=.6, radius=3)
print_grid(schelling)
data = [schelling.happy_count]
i = 0
for s in run(schelling):
    data.append(schelling.happy_count)
    schelling = s
    i += 1

print_grid(schelling)
