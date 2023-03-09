import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

rng = np.random.default_rng(12345)  # seed


# bere na vstupu pole barev vrcholu poporade, cislum priradi nahodne barvy a vykresli graf
def plot(G, cols):
    k = np.max(cols)
    symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    colmap = ["#" + ''.join(rng.choice(symbols, 6)) for i in range(k + 1)]

    colors = [colmap[c] for c in cols]

    nx.draw(G, node_color=colors, with_labels=True)
    plt.show()


def readdimacs(filename) -> nx.Graph:
    file = open(filename, 'r')
    lines = file.readlines()

    Gd = nx.Graph()

    for line in lines:
        if line[0] == "e":
            vs = [int(s) for s in line.split() if s.isdigit()]
            Gd.add_edge(vs[0] - 1, vs[1] - 1)
    return Gd
