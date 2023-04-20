# -*- coding: utf-8 -*-
import math
import queue
import random
import sys
from collections import deque
from typing import Iterable

import numpy as np
import pygame

BLOCKTYPES = 5

pathResult = tuple[deque, Iterable[tuple[int, int]]]

def pythagorian(x_diff, y_diff) -> float:
    return math.sqrt(x_diff**2 + y_diff**2)

h = lambda loc: abs(loc[0] - env.goalx) + abs(loc[1] - env.goaly)

# třída reprezentující prostředí
class Env:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.arr = np.zeros((height, width), dtype=int)
        self.startx = 0
        self.starty = 0
        self.goalx = width - 1
        self.goaly = height - 1

    def is_valid_xy(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.height and self.arr[y, x] == 0:
            return True
        return False

    def set_start(self, x, y):
        if self.is_valid_xy(x, y):
            self.startx = x
            self.starty = y

    def set_goal(self, x, y):
        if self.is_valid_xy(x, y):
            self.goalx = x
            self.goaly = y

    def is_empty(self, x, y):
        if self.arr[y, x] == 0:
            return True
        return False

    def add_block(self, x, y):
        if self.arr[y, x] == 0:
            r = random.randint(1, BLOCKTYPES)
            self.arr[y, x] = r

    def get_neighbors(self, x, y):
        l = []
        if x - 1 >= 0 and self.arr[y, x - 1] == 0:
            l.append((x - 1, y))

        if x + 1 < self.width and self.arr[y, x + 1] == 0:
            l.append((x + 1, y))

        if y - 1 >= 0 and self.arr[y - 1, x] == 0:
            l.append((x, y - 1))

        if y + 1 < self.height and self.arr[y + 1, x] == 0:
            l.append((x, y + 1))

        return l

    def get_tile_type(self, x, y):
        return self.arr[y, x]

    # vrací dvojici 1. frontu dvojic ze startu do cíle, 2. seznam dlaždic
    # k zobrazení - hodí se např. pro zvýraznění cesty, nebo expandovaných uzlů
    # start a cíl se nastaví pomocí set_start a set_goal
    # <------    ZDE vlastní metoda
    def path_planner(self) -> pathResult:
        return self.djikstra()

    def a_star(self) -> pathResult:
        goal = (env.goalx, env.goaly)
        source = (ufo.x, ufo.y)
        open_set = {source}

        came_from = dict()
        g_score = {source: 0}
        f_score = {source: h(source)}

        while len(open_set) > 0:
            current = min(open_set.intersection(f_score.keys()), key=f_score.get)
            open_set.remove(current)
            if current == goal:
                q = deque()
                backtrack_current = current
                while backtrack_current != source:
                    q.appendleft(backtrack_current)
                    backtrack_current = came_from[backtrack_current]
                return q, list(f_score.keys())

            for neighbor in env.get_neighbors(current[0], current[1]):
                tentative_gscore = g_score.get(current) + 0 # weight
                if tentative_gscore < g_score.get(neighbor, math.inf):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_gscore
                    f_score[neighbor] = tentative_gscore + h(neighbor)
                    open_set.add(neighbor)

        q = deque()
        return q, list()


    def djikstra(self) -> pathResult:
        dist = dict()
        prev = dict()
        source = (ufo.x, ufo.y)
        dist[source] = 0

        q = queue.PriorityQueue()
        for x in range(WIDTH):
            for y in range(HEIGHT):
                v = (x, y)
                q.put((dist.get(v, math.inf), v))

        while not q.empty():
            _, u = q.get()
            x, y = u
            for neighbor in env.get_neighbors(x,y):
                dist_u = dist.get(u, sys.maxsize)
                alt = dist_u + 1 # price
                dist_neighbor = dist.get(neighbor, math.inf)
                if alt < dist_neighbor:
                    dist[neighbor] = alt
                    prev[neighbor] = u
                    q.put((alt, neighbor))

            print(len(q.queue))


        resultQ = deque()
        location = (env.goalx, env.goaly)
        while location != source:
            resultQ.appendleft(location)
            location = prev.get(location)
        return resultQ, dist.keys()

    # lowest by h
    def greedy(self):
        source = (ufo.x, ufo.y)
        goal = (env.goalx, env.goaly)
        options = {source}
        came_from = {}

        while len(options) > 0:
            current = min(options, key=h)
            options.remove(current)

            if current == goal:
                q = deque()
                backtrack_current = current
                while backtrack_current != source:
                    q.appendleft(backtrack_current)
                    backtrack_current = came_from[backtrack_current]
                return q, list(came_from.keys())


            for neighbor in env.get_neighbors(current[0], current[1]):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    options.add(neighbor)

# třída reprezentující ufo        
class Ufo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = deque()
        self.tiles = []

    # přemístí ufo na danou pozici - nejprve je dobré zkontrolovat u prostředí, 
    # zda je pozice validní
    def move(self, x, y):
        self.x = x
        self.y = y

    # reaktivní navigace <------------------------ !!!!!!!!!!!! ZDE DOPLNIT
    def reactive_go(self, env):
        return self.path.popleft()

    # nastaví cestu k vykonání 
    def set_path(self, p, t: Iterable[tuple[int, int]]=()):
        self.path = p
        self.tiles = t

    # vykoná naplánovanou cestu, v každém okamžiku na vyzvání vydá další
    # way point 
    def execute_path(self):
        if self.path:
            return self.path.popleft()
        return (-1, -1)


# definice prostředí -----------------------------------

TILESIZE = 50

# <------    definice prostředí a překážek !!!!!!

WIDTH = 12
HEIGHT = 9

env = Env(WIDTH, HEIGHT)

env.add_block(1, 1)
env.add_block(2, 2)
env.add_block(3, 3)
env.add_block(4, 4)
env.add_block(5, 5)
env.add_block(6, 6)
env.add_block(7, 7)
env.add_block(8, 8)
env.add_block(0, 8)

env.add_block(11, 1)
env.add_block(11, 6)
env.add_block(1, 3)
env.add_block(2, 4)
env.add_block(4, 5)
env.add_block(2, 6)
env.add_block(3, 7)
env.add_block(4, 8)
env.add_block(0, 8)

env.add_block(1, 8)
env.add_block(2, 8)
env.add_block(3, 5)
env.add_block(4, 8)
env.add_block(5, 6)
env.add_block(6, 4)
env.add_block(7, 2)
env.add_block(8, 1)

# pozice ufo <--------------------------
ufo = Ufo(env.startx, env.starty)

WIN = pygame.display.set_mode((env.width * TILESIZE, env.height * TILESIZE))

pygame.display.set_caption("Block world")

pygame.font.init()

WHITE = (255, 255, 255)

FPS = 2

# pond, tree, house, car

BOOM_FONT = pygame.font.SysFont("comicsans", 100)
LEVEL_FONT = pygame.font.SysFont("comicsans", 20)

TILE_IMAGE = pygame.image.load("tile.jpg")
MTILE_IMAGE = pygame.image.load("markedtile.jpg")
HOUSE1_IMAGE = pygame.image.load("house1.jpg")
HOUSE2_IMAGE = pygame.image.load("house2.jpg")
HOUSE3_IMAGE = pygame.image.load("house3.jpg")
TREE1_IMAGE = pygame.image.load("tree1.jpg")
TREE2_IMAGE = pygame.image.load("tree2.jpg")
UFO_IMAGE = pygame.image.load("ufo.jpg")
FLAG_IMAGE = pygame.image.load("flag.jpg")

TILE = pygame.transform.scale(TILE_IMAGE, (TILESIZE, TILESIZE))
MTILE = pygame.transform.scale(MTILE_IMAGE, (TILESIZE, TILESIZE))
HOUSE1 = pygame.transform.scale(HOUSE1_IMAGE, (TILESIZE, TILESIZE))
HOUSE2 = pygame.transform.scale(HOUSE2_IMAGE, (TILESIZE, TILESIZE))
HOUSE3 = pygame.transform.scale(HOUSE3_IMAGE, (TILESIZE, TILESIZE))
TREE1 = pygame.transform.scale(TREE1_IMAGE, (TILESIZE, TILESIZE))
TREE2 = pygame.transform.scale(TREE2_IMAGE, (TILESIZE, TILESIZE))
UFO = pygame.transform.scale(UFO_IMAGE, (TILESIZE, TILESIZE))
FLAG = pygame.transform.scale(FLAG_IMAGE, (TILESIZE, TILESIZE))


def draw_window(ufo, env):
    for i in range(env.width):
        for j in range(env.height):
            t = env.get_tile_type(i, j)
            if t == 1:
                WIN.blit(TREE1, (i * TILESIZE, j * TILESIZE))
            elif t == 2:
                WIN.blit(HOUSE1, (i * TILESIZE, j * TILESIZE))
            elif t == 3:
                WIN.blit(HOUSE2, (i * TILESIZE, j * TILESIZE))
            elif t == 4:
                WIN.blit(HOUSE3, (i * TILESIZE, j * TILESIZE))
            elif t == 5:
                WIN.blit(TREE2, (i * TILESIZE, j * TILESIZE))
            else:
                WIN.blit(TILE, (i * TILESIZE, j * TILESIZE))

    for (x, y) in ufo.tiles:
        WIN.blit(MTILE, (x * TILESIZE, y * TILESIZE))

    WIN.blit(FLAG, (env.goalx * TILESIZE, env.goaly * TILESIZE))
    WIN.blit(UFO, (ufo.x * TILESIZE, ufo.y * TILESIZE))

    pygame.display.update()


def main():
    #  <------------   nastavení startu a cíle prohledávání !!!!!!!!!!
    env.set_start(0, 0)
    env.set_goal(9, 7)

    p, t = env.path_planner()   # cesta pomocí path_planneru prostředí
    ufo.set_path(p, t)
    # ---------------------------------------------------

    clock = pygame.time.Clock()

    run = True
    go = False

    while run:

        clock.tick(FPS)

        # <---- reaktivní pohyb dokud nedojde do cíle 
        if (ufo.x != env.goalx) or (ufo.y != env.goaly):
            x, y = ufo.reactive_go(env)

            # x, y = ufo.execute_path()

            if env.is_valid_xy(x, y):
                ufo.move(x, y)
            else:
                print('[', x, ',', y, ']', "wrong coordinate !")

        draw_window(ufo, env)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == "__main__":
    main()
