# kreslí hru
from collections import deque
from typing import Callable

Game = list[list[int]]
Moves = tuple[deque, float]
Player = int
HalfTurns = int
MAXIMIZING_PLAYER = 2


def printgame(game):
    for r in game:
        pr = ""
        for i in r:
            if i == 0:
                pr += "."
            elif i == 1:
                pr += "x"
            else:
                pr += "o"
        print(pr)


# říká kdo vyhrál 0=nikdo, 1, 2
def whowon(g: Game):
    # řádek
    if g[0][:] == [1, 1, 1] or g[1][:] == [1, 1, 1] or g[2][:] == [1, 1, 1]:
        return 1

    if g[0][:] == [2, 2, 2] or g[1][:] == [2, 2, 2] or g[2][:] == [2, 2, 2]:
        return 2

    # 1. sloupec
    if g[0][0] == g[1][0] == g[2][0] == 1:
        return 1

    if g[0][0] == g[1][0] == g[2][0] == 2:
        return 2

    # 2. sloupec
    if g[0][1] == g[1][1] == g[2][1] == 1:
        return 1

    if g[0][1] == g[1][1] == g[2][1] == 2:
        return 2

    # 3. sloupec
    if g[0][2] == g[1][2] == g[2][2] == 1:
        return 1

    if g[0][2] == g[1][2] == g[2][2] == 2:
        return 2

    # hlavní diagonála
    if g[0][0] == g[1][1] == g[2][2] == 1:
        return 1

    if g[0][0] == g[1][1] == g[2][2] == 2:
        return 2

    # hlavní anti-diagonála
    if g[0][2] == g[1][1] == g[2][0] == 1:
        return 1

    if g[0][2] == g[1][1] == g[2][0] == 2:
        return 2

    return 0


# vrací prázdná místa na šachovnici
def emptyspots(g: Game) -> list[tuple[int, int]]:
    emp = []
    for y in range(3):
        for x in range(3):
            if g[y][x] == 0:
                emp.append((x, y))
    return emp


def create_game() -> Game:
    game = []
    for y in range(3):
        row = []
        for x in range(3):
            row.append(0)
        game.append(row)
    return game


def halfmove_copy(game: Game, x: int, y: int, value: int) -> Game:
    new_game = []
    for old_y, row in enumerate(game):
        if old_y != y:
            new_game.append(row)
            continue

        new_row = []
        for old_x, old_value in enumerate(row):
            if old_x == x:
                new_row.append(value)
            else:
                new_row.append(old_value)
        new_game.append(new_row)
    return new_game


def calc_score(game: Game, half_turns: HalfTurns) -> float:
    won = whowon(game)
    target_player = MAXIMIZING_PLAYER
    other_player = 2 if target_player == 1 else 1
    target_won_k = -1 if won == other_player else (1 if won == target_player else 0)
    result = (1 / half_turns) * target_won_k
    return result


def take_extreme_result(
        game: Game,
        player: Player,
        other_player: Player,
        turns: HalfTurns,
        next: Callable[[Game, Player, Player, HalfTurns], Moves],
        reduce: Callable[[Moves, Moves], Moves]
) -> Moves:
    extreme_moves = None

    if whowon(game) != 0:
        return deque(), calc_score(game, turns)

    empty = emptyspots(game)
    if len(empty) == 0:
        return deque(), calc_score(game, turns)

    for x, y in empty:
        changed_game = halfmove_copy(game, x, y, player)
        next_moves, next_score = next(changed_game, other_player, player, turns + 1)
        next_moves.appendleft((x, y))
        if extreme_moves is None:
            extreme_moves = next_moves, next_score
        else:
            extreme_moves_before = extreme_moves
            extreme_moves = reduce(extreme_moves, (next_moves, next_score))
            extreme_moves = extreme_moves
    return extreme_moves


def take_min(m1: Moves, m2: Moves) -> Moves:
    return m1 if m1[1] < m2[1] else m2


def take_max(m1: Moves, m2: Moves) -> Moves:
    return m1 if m1[1] > m2[1] else m2


def minimax(game: Game, player: Player, other_player: Player, turns: HalfTurns) -> Moves:
    return take_extreme_result(game, player, other_player, turns, maximin, take_min)


def maximin(game: Game, player: Player, other_player: Player, turns: HalfTurns) -> Moves:
    return take_extreme_result(game, player, other_player, turns, minimax, take_max)


def ttt_move(game: Game, player: Player, other_player: Player) -> Moves:
    if player == MAXIMIZING_PLAYER:
        return maximin(game, player, other_player, 0)
    return minimax(game, player, other_player, 0)


prepared_moves = deque()

if __name__ == '__main__':
    game = create_game()
    player = 1
    otherplayer = 2
    prepared_moves, _ = ttt_move(game, player, otherplayer)

    while len(prepared_moves) != 0:
        print("-------")
        printgame(game)

        x, y = prepared_moves.popleft()
        game = halfmove_copy(game, x, y, player)
        player, otherplayer = otherplayer, player

    print("--------")
    printgame(game)
    print("--------")
    print(f"{whowon(game)} won")
