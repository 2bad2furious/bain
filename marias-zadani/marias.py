# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
import random
from functools import cmp_to_key
from itertools import combinations
from typing import Iterable, List, Tuple

import pygame

calculating_moves = 0
WIDTH, HEIGHT = 1200, 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Lizany Marias")

pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 10

LEVEL_FONT = pygame.font.SysFont("comicsans", 20)

# nacteni karet

CER_SEDMA = pygame.image.load("cer_sedma.png")
CER_OSMA = pygame.image.load("cer_osma.png")
CER_DEVITKA = pygame.image.load("cer_devitka.png")
CER_DESITKA = pygame.image.load("cer_desitka.png")
CER_SPODEK = pygame.image.load("cer_spodek.png")
CER_SVRSEK = pygame.image.load("cer_svrsek.png")
CER_KRAL = pygame.image.load("cer_kral.png")
CER_ESO = pygame.image.load("cer_eso.png")

ZAL_SEDMA = pygame.image.load("zal_sedma.png")
ZAL_OSMA = pygame.image.load("zal_osma.png")
ZAL_DEVITKA = pygame.image.load("zal_devitka.png")
ZAL_DESITKA = pygame.image.load("zal_desitka.png")
ZAL_SPODEK = pygame.image.load("zal_spodek.png")
ZAL_SVRSEK = pygame.image.load("zal_svrsek.png")
ZAL_KRAL = pygame.image.load("zal_kral.png")
ZAL_ESO = pygame.image.load("zal_eso.png")

LIS_SEDMA = pygame.image.load("lis_sedma.png")
LIS_OSMA = pygame.image.load("lis_osma.png")
LIS_DEVITKA = pygame.image.load("lis_devitka.png")
LIS_DESITKA = pygame.image.load("lis_desitka.png")
LIS_SPODEK = pygame.image.load("lis_spodek.png")
LIS_SVRSEK = pygame.image.load("lis_svrsek.png")
LIS_KRAL = pygame.image.load("lis_kral.png")
LIS_ESO = pygame.image.load("lis_eso.png")

KUL_SEDMA = pygame.image.load("kul_sedma.png")
KUL_OSMA = pygame.image.load("kul_osma.png")
KUL_DEVITKA = pygame.image.load("kul_devitka.png")
KUL_DESITKA = pygame.image.load("kul_desitka.png")
KUL_SPODEK = pygame.image.load("kul_spodek.png")
KUL_SVRSEK = pygame.image.load("kul_svrsek.png")
KUL_KRAL = pygame.image.load("kul_kral.png")
KUL_ESO = pygame.image.load("kul_eso.png")

TURN = pygame.image.load("turn.png")

CARD_WIDTH = 60
CARD_HEIGHT = 80

COLORS = ['cer', 'lis', 'zal', 'kul']
VALUES = ['sedma', 'osma', 'devitka', 'desitka', 'spodek', 'svrsek', 'kral', 'eso']
COLOR_PREF = {'kul': 1, 'zal': 2, 'lis': 3, 'cer': 4}
VALUE_PREF = {'sedma': 7, 'osma': 8, 'devitka': 9,
              'spodek': 10, 'svrsek': 11, 'kral': 12,
              'desitka': 13, 'eso': 14}


# trida karty
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.picture = None
        self.points = 0

        if value == 'desitka' or value == 'eso':
            self.points = 10

        # adds picture to a card
        if color == 'cer' and value == 'sedma':
            self.picture = CER_SEDMA
        if color == 'cer' and value == 'osma':
            self.picture = CER_OSMA
        if color == 'cer' and value == 'devitka':
            self.picture = CER_DEVITKA
        if color == 'cer' and value == 'desitka':
            self.picture = CER_DESITKA
        if color == 'cer' and value == 'spodek':
            self.picture = CER_SPODEK
        if color == 'cer' and value == 'svrsek':
            self.picture = CER_SVRSEK
        if color == 'cer' and value == 'kral':
            self.picture = CER_KRAL
        if color == 'cer' and value == 'eso':
            self.picture = CER_ESO

        if color == 'zal' and value == 'sedma':
            self.picture = ZAL_SEDMA
        if color == 'zal' and value == 'osma':
            self.picture = ZAL_OSMA
        if color == 'zal' and value == 'devitka':
            self.picture = ZAL_DEVITKA
        if color == 'zal' and value == 'desitka':
            self.picture = ZAL_DESITKA
        if color == 'zal' and value == 'spodek':
            self.picture = ZAL_SPODEK
        if color == 'zal' and value == 'svrsek':
            self.picture = ZAL_SVRSEK
        if color == 'zal' and value == 'kral':
            self.picture = ZAL_KRAL
        if color == 'zal' and value == 'eso':
            self.picture = ZAL_ESO

        if color == 'lis' and value == 'sedma':
            self.picture = LIS_SEDMA
        if color == 'lis' and value == 'osma':
            self.picture = LIS_OSMA
        if color == 'lis' and value == 'devitka':
            self.picture = LIS_DEVITKA
        if color == 'lis' and value == 'desitka':
            self.picture = LIS_DESITKA
        if color == 'lis' and value == 'spodek':
            self.picture = LIS_SPODEK
        if color == 'lis' and value == 'svrsek':
            self.picture = LIS_SVRSEK
        if color == 'lis' and value == 'kral':
            self.picture = LIS_KRAL
        if color == 'lis' and value == 'eso':
            self.picture = LIS_ESO

        if color == 'kul' and value == 'sedma':
            self.picture = KUL_SEDMA
        if color == 'kul' and value == 'osma':
            self.picture = KUL_OSMA
        if color == 'kul' and value == 'devitka':
            self.picture = KUL_DEVITKA
        if color == 'kul' and value == 'desitka':
            self.picture = KUL_DESITKA
        if color == 'kul' and value == 'spodek':
            self.picture = KUL_SPODEK
        if color == 'kul' and value == 'svrsek':
            self.picture = KUL_SVRSEK
        if color == 'kul' and value == 'kral':
            self.picture = KUL_KRAL
        if color == 'kul' and value == 'eso':
            self.picture = KUL_ESO

    def __repr__(self):
        return "Card:" + self.color + ' ' + self.value

    def __str__(self):
        return self.color + ' ' + self.value

    def __eq__(self, other):
        return isinstance(other, Card) and self.color == other.color and self.value == other.value

    def __hash__(self):
        return hash((self.color, self.value))


all_card_options = [Card(b, h) for b in COLORS for h in VALUES]


class Stych:
    def __init__(self, phase, card0, card1, hlaska0, hlaska1, wt):
        self.card0 = card0
        self.card1 = card1
        self.cards = [card0, card1]
        self.hlaska0 = hlaska0  # true/false, pokud karta byla hlaska
        self.hlaska1 = hlaska1
        self.hlasky = [hlaska0, hlaska1]  # pro pristupn skrze pole
        self.wt = wt  # who took
        self.phase = phase


class History:
    def __init__(self):
        self.stychy = []

    def add(self, phase, card0, card1, hlaska0, hlaska1, wt):
        self.stychy.append(Stych(phase, card0, card1, hlaska0, hlaska1, wt))

    def getlast(self) -> Stych:
        return self.stychy[-1]


# trida spravujici talon
class Talon:
    def __init__(self, cards):
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def isempty(self):
        if len(self.cards) == 0:
            return True
        return False

    def popcard(self):
        if not self.isempty():
            return self.cards.pop()
        return None


# trida spravujici karty v ruce 
class Hand:
    def __init__(self, cards=None):
        self.cards = list(cards) if cards is not None else []

    def __cmpcards__(self, card1, card2):

        c1_color_pref = COLOR_PREF[card1.color]
        c2_color_pref = COLOR_PREF[card2.color]
        c1_value_pref = VALUE_PREF[card1.value]
        c2_value_pref = VALUE_PREF[card2.value]

        if c1_color_pref < c2_color_pref:
            return 1
        elif c1_color_pref == c2_color_pref:
            if c1_value_pref < c2_value_pref:
                return 1
            elif c1_value_pref == c2_value_pref:
                return 0
            else:
                return -1
        else:
            return -1

    def sort(self):
        self.cards = sorted(self.cards, key=cmp_to_key(self.__cmpcards__))

    def addcard(self, card):
        self.cards.append(card)
        # neefektivni - tridi se pri kazdem liznuti karty
        self.sort()

    def isempty(self):
        if len(self.cards) == 0:
            return True
        return False

    def iscardpresent(self, col, val):
        for c in self.cards:
            if c.color == col and c.value == val:
                return True
        return False

    # vraci vsechny karty dane barvy
    def getcardscol(self, col):
        l = []
        for c in self.cards:
            if c.color == col:
                l.append(c)
        return l

    # vraci vsechny karty dane barvy vyssi nez value
    def getcardshigher(self, col, val):
        l = []
        for c in self.cards:
            if c.color == col and VALUE_PREF[c.value] > VALUE_PREF[val]:
                l.append(c)
        return l

    # vraci vsechny karty dane hodnoty
    def getcardsval(self, val):
        l = []
        for c in self.cards:
            if c.value == val:
                l.append(c)
        return l

    def removecard(self, col, val):
        index = -1
        if self.iscardpresent(col, val):
            for i in range(len(self.cards)):
                if (self.cards[i].color == col) and (self.cards[i].value == val):
                    index = i
                    break

        if index >= 0:
            del self.cards[index]
            return True

        return False

    def disp(self):
        for c in self.cards:
            c.disp()

    # returns valid card moves to opcard
    def validcardmoves(self, opcard: Card | None, phase, trumfcolor) -> List[Card]:
        # opcard.disp()
        # print("---")
        # print(phase)
        # print(trumfcolor)
        # print("---")

        if self.isempty():
            return []

        cardmoves: List[Card] = self.cards.copy()

        if opcard != None:

            cardmoves = self.getcardshigher(opcard.color, opcard.value)

            if len(cardmoves) == 0:
                # hrac nema zadne vyssi karty dane barvy
                # alespon chceme karty stejne barvy
                cardmoves = self.getcardscol(opcard.color)

                if len(cardmoves) == 0:
                    # hrac nema karty v barve protihracovy karty
                    if phase == 1:
                        # v prvni fazi muzeme hrat cokoli, pokud nemame barvu
                        # ve druhe fazi, kdyz nemame, musime trumfovat
                        cardmoves = self.getcardscol(trumfcolor)
                        if len(cardmoves) == 0:
                            cardmoves = self.cards.copy()
                    else:
                        cardmoves = self.cards.copy()

        # vyhozeni kralu z moznych tahu, kdyz mame i svrska
        # musime hrat svrska prvniho
        svrsci = self.getcardsval('svrsek')
        for s in svrsci:
            index = -1
            for i in range(len(cardmoves)):
                if cardmoves[i].color == s.color and cardmoves[i].value == 'kral':
                    index = i
                    break

            if index >= 0:
                del cardmoves[index]

        return cardmoves

        # vybere nahodnou kartu

    def chooserandom(self, cardlist):
        # print(cardlist)
        return random.choice(cardlist)

    def cards_set(self):
        return set(self.cards)

    def copy(self):
        return Hand(self.cards.copy())

    def without_card(self, card: Card):
        h = self.copy()
        h.removecard(card.color, card.value)
        return h


# trida hrace
class Player:
    def __init__(self, num, name):
        self.num = num
        self.name = name
        self.hand = Hand()

    def isdone(self):
        if self.hand.isempty():
            return True
        return False

    def addcard(self, card):
        self.hand.addcard(card)

    def play(self, history, phase, trumfcolor, first=True, opcard=None, player_index=0):
        if not self.isdone():
            hlaska = False

            if first:
                cm = self.hand.validcardmoves(None, phase, trumfcolor)

                # tisk validnich tahu
                #print("====================================")
                #print("Hrac:", self.name, "===============")
                #print("------ Ma v ruce:")
               # for c in self.hand.cards:
                #    print(c)
                #print("------ Muze hrat")
                #for c in cm:
                #    print(c)

                c = self.hand.chooserandom(self.hand.cards)

                if c.value == 'svrsek':
                    if self.hand.iscardpresent(c.color, 'kral'):
                        hlaska = True

                self.hand.removecard(c.color, c.value)

                return c, hlaska
            else:
                # hraje jako druhy
                cm = self.hand.validcardmoves(opcard, phase, trumfcolor)

                # tisk validnich tahu
                #print("====================================")
                #print("Hrac:", self.name, "===============")
                #print("------ Ma v ruce:")
                #for c in self.hand.cards:
                #    print(c)
                #print("------ Muze hrat")
                #for c in cm:
                 #   print(c)

                c = self.hand.chooserandom(cm)

                if c.value == 'svrsek':
                    if self.hand.iscardpresent(c.color, 'kral'):
                        hlaska = True

                self.hand.removecard(c.color, c.value)

                return c, hlaska

        return None, False


def calc_points(card: Card, hand: Hand, other_card: Card, phase: int, trumfcolor: str) -> Tuple[bool, int]:
    wins = Marias.firsttakes(card, other_card, phase, trumfcolor)
    points = 0
    card_points = card.points + other_card.points

    if wins:
        if hand.isempty():
            points += 10
        points += card_points
        if card.value == "spodek" and hand.iscardpresent(card.color, "kral"):
            call_points = 20 if trumfcolor != card.color else 40
            points += call_points
    else:
        if hand.isempty():
            points -= 10
        points -= card_points

    return wins, points


# trida spravujici hru
class Marias:
    def __init__(self):
        # init karet
        cards = [Card(b, h) for b in COLORS for h in VALUES]
        self.talon = Talon(cards)
        self.talon.shuffle()
        # print(self.talon.cards)
        self.player0 = MyPlayer(0, 'My AI')
        self.player1 = Player(1, 'Tunta')

        # rozdej
        for i in range(5):
            self.player0.addcard(self.talon.popcard())

        for i in range(5):
            self.player1.addcard(self.talon.popcard())

        self.trumfcolor = self.talon.cards[0].color
        self.lastcard = self.talon.cards[0]

        # posledni tah
        self.lastcard0 = None
        self.lastcard1 = None
        self.lasthlaska0 = False
        self.lasthlaska1 = False

        self.phase = 0  # 0... pripravna faze, 1...dolizany balik
        self.playerturn = 0

        self.player0points = 0  # body hracu
        self.player1points = 0

        self.round = 0
        self.history = History()

    def isdone(self):
        if self.player0.isdone() and self.player1.isdone():
            return True
        return False

    @staticmethod
    def firsttakes(card0, card1, phase, trumfcolor):

        if (card0 == None) or (card1 == None):
            return None

        if phase == 0:
            if (card1.color == card0.color) and (VALUE_PREF[card1.value] > VALUE_PREF[card0.value]):
                return False
            else:
                return True

        if phase == 1:
            if (card1.color == card0.color) and (VALUE_PREF[card1.value] > VALUE_PREF[card0.value]):
                return False
            elif (card1.color != card0.color) and (card1.color == trumfcolor):
                return False
            else:
                return True

    def play(self):

        if self.talon.isempty():
            self.phase = 1

        # tahy hracu
        if self.playerturn == 0:
            self.lastcard0, self.lasthlaska0 = self.player0.play(self.history, self.phase, self.trumfcolor, True, None,
                                                                 1)
            self.lastcard1, self.lasthlaska1 = self.player1.play(self.history, self.phase, self.trumfcolor, False,
                                                                 self.lastcard0, 0)

        else:
            self.lastcard1, self.lasthlaska1 = self.player1.play(self.history, self.phase, self.trumfcolor, True, None,
                                                                 1)
            self.lastcard0, self.lasthlaska0 = self.player0.play(self.history, self.phase, self.trumfcolor, False,
                                                                 self.lastcard1, 0)

        self.round += 1

        c0 = self.lastcard0
        c1 = self.lastcard1

        # kdo bere stych
        wt = None
        if self.playerturn == 0:
            ft = Marias.firsttakes(c0, c1, self.phase, self.trumfcolor)
            if ft:
                wt = 0
            else:
                wt = 1
        else:
            ft = Marias.firsttakes(c1, c0, self.phase, self.trumfcolor)
            if ft:
                wt = 1
            else:
                wt = 0

        self.history.add(self.phase, self.lastcard0, self.lastcard1, self.lasthlaska0, self.lasthlaska1, wt)

        # print("********************")
        # print(c0, " vs. ", c1, "wins: ", wt)
        # print("********************")

        if wt == 0:
            self.player0points += c0.points + c1.points
            self.playerturn = 0

            if not self.talon.isempty():
                # prvni dolizava hrac, ktery sebral stych
                self.player0.addcard(self.talon.popcard())
                self.player1.addcard(self.talon.popcard())

                # posledni stych
            if self.isdone():
                self.player0points += 10

        else:
            self.player1points += c0.points + c1.points
            self.playerturn = 1

            if not self.talon.isempty():
                self.player1.addcard(self.talon.popcard())
                self.player0.addcard(self.talon.popcard())

            # posledni stych
            if self.isdone():
                self.player1points += 10

        if self.lasthlaska0:
            if self.lastcard0.color == self.trumfcolor:
                self.player0points += 40
            else:
                self.player0points += 20

        if self.lasthlaska1:
            if self.lastcard1.color == self.trumfcolor:
                self.player1points += 40
            else:
                self.player1points += 20

        self.lastcard0 = None
        self.lastcard1 = None
        self.lasthlaska0 = False
        self.lasthlaska1 = False


def draw_window(marias):
    # WIN.blit(SEA, (0, 0))
    WIN.fill(WHITE)

    h1 = LEVEL_FONT.render("Hrac 0: " + marias.player0.name + " ::: Skore: " + str(marias.player0points), 1, BLACK)
    h2 = LEVEL_FONT.render("Hrac 1: " + marias.player1.name + " ::: Skore: " + str(marias.player1points), 1, BLACK)
    h3 = LEVEL_FONT.render("Trumfy: ", 1, BLACK)

    WIN.blit(h1, (30, 30))
    WIN.blit(h2, (30, 660))
    WIN.blit(h3, (1000, 10))

    # WIN.blit(FLAG, (WIDTH - ME_SIZE, HEIGHT - ME_SIZE - 10))

    # for mine in mines:
    #    WIN.blit(ENEMY, (mine.rect.x, mine.rect.y))

    # cards of player 1 (top) 
    x = 50
    y = 70
    for c in marias.player0.hand.cards:
        WIN.blit(c.picture, (x, y))
        x += 70

    # cards of player 2 (down)
    x = 50
    y = 550
    for c in marias.player1.hand.cards:
        WIN.blit(c.picture, (x, y))
        x += 70

    # draw history 
    x = 50
    y = 250
    for stych in marias.history.stychy:
        c0 = stych.card0
        c1 = stych.card1

        if c0 != None:
            d = 0
            if stych.hlaska0:
                d = 20
            WIN.blit(c0.picture, (x, y - d))

        if c1 != None:
            d = 0
            if stych.hlaska1:
                d = 20
            WIN.blit(c1.picture, (x, y + 120 + d))

        wt = stych.wt

        if wt == 0:
            WIN.blit(TURN, (x + 20, y - 50))
        if wt == 1:
            WIN.blit(TURN, (x + 20, y + 250))

        x += 70

    WIN.blit(marias.lastcard.picture, (1000, 50))
    pygame.draw.line(WIN, BLACK, (814, 200), (814, 520), 3)

    pygame.display.update()


# hlavni smycka hry
def main():

    marias = Marias()

    clock = pygame.time.Clock()

    run = True
    firstdraw = True
    play = False

    while run:

        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()

        # herni kolo - stridaji se tahy hracu
        if keys_pressed[pygame.K_SPACE] and not marias.isdone():
            # if not marias.isdone():
            marias.play()

        draw_window(marias)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


def get_last_card_from_stych(history: History, index: int):
    try:
        return history.getlast().cards[index]
    except IndexError:
        return None

def get_depth(len: int)->int:
    if len > 10:
        return 2
    if len > 7:
        return 3
    #if len > 6:
    #    return 4
    return 5

class MyPlayer(Player):



    def __init__(self, num, name):
        super().__init__(num, name)


    def play(self, history, phase, trumfcolor, first=True, opcard=None, player_index=0):
        start = datetime.datetime.now()
        #print(f"started calculating move at {start.isoformat()}")
        used_cards_in_history = frozenset([c for s in history.stychy for c in s.cards])
        filtered_options = list(
            filter(lambda c: c not in self.hand.cards and c != opcard and c not in used_cards_in_history,
                   all_card_options))

        move = MMC.next_move(filtered_options, self.hand.copy(), trumfcolor, opcard, phase, depth=get_depth(len(filtered_options)))
        end = datetime.datetime.now()
        #print(f"ended calculating move at {end.isoformat()}")
        global calculating_moves
        calculating_moves = 0
        card = move.card
        call = move.is_calling
        removed = self.hand.removecard(card.color, card.value)

        return card, call


def has_king_of(cards: Iterable[Card], color: str) -> bool:
    for card in cards:
        if card.value == "kral" and card.color == color:
            return True
    return False


class Evaluated_move:
    def __init__(self, card: Card, points: float):
        self.card = card
        self.points = points

    def with_calling_based_on(self, hand: Hand) -> Card_move:
        return Card_move(self.card, self.points,
                         self.card.value == "sasek" and has_king_of(hand.cards, self.card.color))


class Card_move:
    def __init__(self, card: Card, points: float, is_calling: bool):
        self.card = card
        self.points = points
        self.is_calling = is_calling


def all_hands_with(card_options: List[Card], card: Card) -> Iterable[Hand]:
    size = 4
    if len(card_options) < size:
        return [Hand(list(card_options) + [card])]

    hand_cards = combinations(card_options, size)
    return list(map(lambda cards: Hand(list(cards) + [card]), hand_cards))


def all_hands(card_options: List[Card]) -> Iterable[Hand]:
    size = 5
    if len(card_options) < size:
        return [Hand(card_options)]

    hand_cards = combinations(card_options, size)
    return map(lambda cards: Hand(cards), hand_cards)


def create_hands_list(hand: Hand, card_options: List[Card]) -> List[Hand]:
    if len(hand.cards) == 5 or len(card_options) == 0:
        return [hand.copy()]

    result = []
    for card in card_options:
        result.append(Hand(hand.cards + [card]))
    return result


def card_options_without_those_in_hand(card_options: List[Card], hand: Hand) -> List[Card]:
    return list(filter(lambda c: c not in hand.cards, card_options))


def register_move_calculating():
    global calculating_moves
    calculating_moves += 1
    #if calculating_moves % 1_000 == 0:
        #print(f"Moves {calculating_moves:_}")


def card_options_without_any(card_options: List[Card], cards: List[Card]):
    return list(filter(lambda c: c not in cards, card_options))


def card_options_without(card_options: List[Card], card: Card):
    return list(filter(lambda c: c != card, card_options))


def create_hand_options(hand: Hand, card_options: List[Card], phase: int) -> List[Hand]:
    if phase == 1:
        return [hand]

    result = []
    for card in card_options:
        result.append(Hand(hand.cards + [card]))
    return result


def avg_repeated(values: List[Tuple[float, int]], avg: float = 0.0, count: int = 0) -> Tuple[float, int]:
    for value in values:
        avg_value, avg_count = value
        for _ in range(avg_count):
            count += 1
            avg += (avg_value - avg) / count
    return avg, count


class MMC:

    @staticmethod
    def _next_turn(wins: bool, phase: int, trumfcolor: str, hand: Hand, card_options: List[Card], depth: int) -> Tuple[
        float,
        int]:
        register_move_calculating()
        if len(card_options) == 0 or depth <= 1:
            return 0, 0

        if len(card_options) <= 5:
            phase = 1

        if wins:
            count = 0
            avg = 0
            hands = create_hand_options(hand, card_options, phase)
            for hand in hands:
                for card in hand.validcardmoves(None, phase, trumfcolor):
                    card_options_without_card = card_options_without_those_in_hand(card_options, hand)
                    turn_avg, turn_count = MMC._make_first_move(card_options_without_card, hand, card, trumfcolor, phase, depth - 1)
                    avg, count = avg_repeated([(turn_avg, turn_count)], avg, count)

            return avg, count

        avg = 0
        count = 0
        for opcard in card_options:
            card_options_without_opcard = card_options_without(card_options, opcard)
            hands = create_hands_list(hand, card_options_without_opcard)
            for hand in hands:
                validcards = hand.validcardmoves(opcard, phase, trumfcolor)
                for card in validcards:
                    new_card_options = card_options_without(card_options_without_opcard, card)
                    new_hand = hand.without_card(card)
                    turn_avg, turn_count = MMC._make_answer_move(new_card_options, new_hand, card, opcard, trumfcolor,
                                                                 phase, depth - 1)
                    avg, count = avg_repeated([(turn_avg, turn_count)], avg, count)
        return avg, count

    @staticmethod
    # for eliminating cards from opponent's possible cards
    def next_move(filtered_options: List[Card], hand: Hand, trumfcolor: str, opcard: Card | None, phase: int,
                  depth: int) -> Card_move:

        if len(filtered_options) <= 5:
            phase = 1
        # TODO fix wrong hand prediction when we have less than 5
        # if player is starting we want to get max first, otherwise we want min first

        if opcard is None:
            make_move = lambda card: MMC._make_first_move(filtered_options,
                                                          hand.without_card(card), card, trumfcolor, phase, depth)
        else:
            make_move = lambda card: MMC._make_answer_move(filtered_options,
                                                           hand.without_card(card), card, opcard, trumfcolor,
                                                           phase, depth)

        maximum = None
        for card in hand.validcardmoves(opcard, phase, trumfcolor):
            points, _ = make_move(card)
            if maximum is None or points > maximum.points:
                maximum = Evaluated_move(card, points)

        return maximum.with_calling_based_on(hand)

    @staticmethod
    def _make_first_move(card_options: List[Card], hand: Hand, card: Card, trumfcolor: str, phase: int,
                         depth: int) -> Tuple[float, int]:

        count = 0
        avg = 0
        valid_opcards = Hand(card_options).validcardmoves(None, phase, trumfcolor)
        for opcard in valid_opcards:
            count += 1
            wins, turn_score = calc_points(card, hand, opcard, phase, trumfcolor)
            card_options_without_opcard = card_options_without(card_options, opcard)
            next_turn_score, next_turn_score_weight = MMC._next_turn(wins, phase, trumfcolor, hand,
                                                                     card_options_without_opcard, depth)
            avg, count = avg_repeated([(next_turn_score, next_turn_score_weight), (turn_score, 1)], avg, count)

        return avg, count

    @staticmethod
    def _make_answer_move(card_options: List[Card], hand: Hand, card: Card, opcard: Card, trumfcolor: str,
                          phase: int, depth: int) -> Tuple[float, int]:
        if len(card_options) <= 5:
            phase = 1

        wins, turn_score = calc_points(card, hand, opcard, phase, trumfcolor)
        next_turn_score, next_turn_score_weight = MMC._next_turn(wins, phase, trumfcolor, hand, card_options,
                                                                 depth)
        avg, count = avg_repeated([(next_turn_score, next_turn_score_weight)])

        return avg, count


if __name__ == "__main__":
    total_games = 0
    wins = 0
    avg_ratio = 0
    for _ in range(10_000):
        marias = Marias()
        while not marias.isdone():
            marias.play()
        total_games += 1
        ratio = 10 if marias.player1points == 0 else marias.player0points / marias.player1points
        print(f"game over {marias.player0.name}:{marias.player0points} vs {marias.player1.name}:{marias.player1points} ", end="")
        if ratio >= 1:
            wins += 1
            print("win")
        else:
            print("loss")

        avg_ratio += ((ratio - avg_ratio) / total_games)
        print(f"avg_ratio {avg_ratio}")
        print(f"wins {wins}/{total_games} total games - {(wins/total_games)*100}% WR")
