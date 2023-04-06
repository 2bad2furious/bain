import random

import more_itertools as mi
import numpy as np
from deap import tools, creator, base, algorithms
from matplotlib import pyplot as plt

IND_SIZE = 20
POP_SIZE = 20
weights = (
    0.0,  # variabilita
    5.0,  # počet vrcholů
    -5.0,  # jak moc jdu k extrémům
    .50,  # % zatopených oblastí
    -5.0,  # velikost jezírek
)
WATER_LINE = .5
Individual = list[float]
IDEAL_PEAK_RATIO = .8
EXTREME_DIST = .5
PEAK_DIFF = .2
VARIABILITY = .1


def variability(individual: Individual) -> int:
    count = 0
    for window in mi.windowed(individual, 2):
        count += abs(window[1] - window[0]) < VARIABILITY
    print(f"var={count}")
    return count


def diff_from_calc_peak_ratio(individual: Individual) -> float:
    count = 0
    for window in mi.windowed(individual, 2):
        count += abs(window[1] - window[0]) > PEAK_DIFF  # TODO improve
    print(f"count={count}, len={len(individual)}")
    return abs((count / len(individual)) - IDEAL_PEAK_RATIO)


def dist_from_extreme(point: float) -> float:
    print(f"point={point} ext={1 - point if point > 0.5 else point}")
    return 1 - point if point > 0.5 else point


def calc_extremism(individual: Individual) -> float:
    return sum(map(lambda v: dist_from_extreme(v) > EXTREME_DIST, individual))


def calc_pct_flooded(individual: Individual) -> float:
    print(individual)
    pond_size = calc_pond_size(individual)
    length = len(individual)  # TODO improve
    # print(f"pond_size={pond_size} length={length}")
    return pond_size / length


def calc_pond_size(individual: Individual) -> int:
    pond = map(lambda v: v <= WATER_LINE, individual)
    # print(list(pond))
    return sum(pond)  # TODO improve


def evaluate(individual: Individual) -> tuple[int, float, float, float, float]:
    pond_count = variability(individual)
    peak_diff = diff_from_calc_peak_ratio(individual)
    extremism = calc_extremism(individual)
    pct_flooded = calc_pct_flooded(individual)
    pond_size = calc_pond_size(individual)
    print(f"peak_diff={peak_diff}")

    return pond_count, peak_diff, extremism, pct_flooded, pond_size


FITNESS_FUN = "FitnessMax"
INDIVIDUAL_FUN = "Individual"
ATTR_FLOAT_FUN = "attr_float"
POP_FUN = "population"

creator.create(FITNESS_FUN, base.Fitness, weights=weights)
creator.create(INDIVIDUAL_FUN, list, fitness=getattr(creator, FITNESS_FUN))

toolbox = base.Toolbox()
toolbox.register(ATTR_FLOAT_FUN, random.uniform, 0, 1)
toolbox.register(
    INDIVIDUAL_FUN,
    tools.initRepeat,
    getattr(creator, INDIVIDUAL_FUN),
    getattr(toolbox, ATTR_FLOAT_FUN),
    n=IND_SIZE
)

toolbox.register(POP_FUN, tools.initRepeat, list, getattr(toolbox, INDIVIDUAL_FUN))
# pop = getattr(toolbox, POP_FUN)(n=POP_SIZE)
# print(pop)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxOnePoint)
#toolbox.register("mutate", tools.mutPolynomialBounded,eta=, low=0, up=1, indpb=0.05)
toolbox.register("mutate", tools.mutGaussian,mu=0,sigma=.1, indpb=0.05)
#toolbox.register("select", tools.selTournament, tournsize=10)
toolbox.register("select", tools.selTournament, tournsize=2)

s = tools.Statistics(key=lambda ind: ind.fitness.values)
s.register("mean", np.mean)
s.register("max", np.max)
hof = tools.HallOfFame(1)
pop = getattr(toolbox, POP_FUN)(n=POP_SIZE)

NGEN = 500  # počet generací
CXPB = .5  # pravděpodobnost crossoveru na páru
MUTPB = .3  # pravděpodobnost mutace jedince
finalpop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, halloffame=hof)

plt.ylim(0, 1)  # Y je vzdycky 0-1
plt.axhspan(0, WATER_LINE, facecolor='lightblue', alpha=0.4)  # Vykresli vodu na 0.5
plt.plot(range(0, IND_SIZE), finalpop[0])
plt.show()
