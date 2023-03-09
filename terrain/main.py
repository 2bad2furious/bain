import random

from deap import tools, creator, base

IND_SIZE = 10
POP_SIZE = 10
weights = (1.0,)

def evaluate(individual)->float:
    pass

FITNESS_FUN = "FitnessMax"
INDIVIDUAL_FUN = "Individual"
ATTR_FLOAT_FUN = "attr_float"
POP_FUN = "population"



creator.create(FITNESS_FUN, base.Fitness, weights=weights)
creator.create(INDIVIDUAL_FUN, list, fitness=getattr(creator, FITNESS_FUN))

toolbox = base.Toolbox()
toolbox.register(ATTR_FLOAT_FUN, random.randint, 0, 1)
toolbox.register(
    INDIVIDUAL_FUN,
    tools.initRepeat,
    getattr(creator, INDIVIDUAL_FUN),
    getattr(toolbox, ATTR_FLOAT_FUN),
    n=IND_SIZE
)

toolbox.register(POP_FUN, tools.initRepeat, list, getattr(toolbox, INDIVIDUAL_FUN))
#pop = getattr(toolbox, POP_FUN)(n=POP_SIZE)
#print(pop)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=1, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
