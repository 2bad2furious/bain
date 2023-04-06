from random import random
from numpy import average

def mojesuperduperrozhodovacifunkce(moje_tahy, tvoje_tahy):
    if len(tvoje_tahy) == 0:
        predicted_move = 1
    else:
        predicted_move = average(tvoje_tahy)
        if abs(predicted_move - 0.5) < 0.2:
            predicted_move = 1

    betray = rozdej_skore(1, predicted_move)
    not_betray = rozdej_skore(0, predicted_move)
    return betray < not_betray

def a(my_history, his_history):
    if len(his_history) == 0:
        his_move = 0
    else:
        his_move = his_history[-1]
    return his_move

def rozdej_skore(tah1, tah2):
    # 1 = zradi, 0 = nezradi

    skores = (0, 0)

    if (tah1 == 1) and (tah2 == 1):
        skores = (2, 2)

    if (tah1 == 1) and (tah2 == 0):
        skores = (0, 3)

    if (tah1 == 0) and (tah2 == 1):
        skores = (3, 0)

    if (tah1 == 0) and (tah2 == 0):
        skores = (1, 1)

    return skores


def play(f1, f2, stepsnum):
    skore1 = 0
    skore2 = 0

    historie1 = []
    historie2 = []

    for i in range(stepsnum):
        tah1 = f1(historie1, historie2)
        tah2 = f2(historie2, historie1)

        s1, s2 = rozdej_skore(tah1, tah2)
        skore1 += s1
        skore2 += s2

        historie1.append(tah1)
        historie2.append(tah2)

    return skore1, skore2


def always_cooperate(myhistory, otherhistory):
    return 0


# náhodná odpověď
def random_answer(myhistory, otherhistory):
    p = random()
    if p < 0.5:
        return 1

    return 0

# seznam funkci o testování
ucastnici = [mojesuperduperrozhodovacifunkce, a]

# funkce se mohou v seznamu i opakovat
# ucastnici = [always_cooperate, always_cooperate, random_answer, random_answer, random_answer]


STEPSNUM = 20

l = len(ucastnici)
skores = [0 for i in range(l)]

print("=========================================")
print("Turnaj")
print("hra délky:", STEPSNUM)
print("-----------------------------------------")

for i in range(l):
    for j in range(i + 1, l):
        f1 = ucastnici[i]
        f2 = ucastnici[j]
        skore1, skore2 = play(f1, f2, STEPSNUM)
        print(f1.__name__, "x", f2.__name__, " ", skore1, ":", skore2)
        skores[i] += skore1
        skores[j] += skore2

print("=========================================")
print("= Výsledné pořadí")
print("-----------------------------------------")

# setrideni indexu vysledku
index = sorted(range(l), key=lambda k: skores[k])

poradi = 1
for i in index:
    f = ucastnici[i]
    print(poradi, ".", f.__name__, ":", skores[i])
    poradi += 1

