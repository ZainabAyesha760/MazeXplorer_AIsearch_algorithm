
# maze_xplorer_part3.py
# MazeXplorer Part 3: AI vs AI
# A* Search vs Minimax vs Alpha-Beta Pruning

import heapq
from itertools import count
from collections import deque

# ---------------- MAZE ----------------

# P = Player, X = Enemy, G = Goal
# # = Wall, . = Normal Path
# F, O = Mud (Cost 10), E = Water (Cost 20)

maze = [
    ['P', '.', '.', '#', '.'],
    ['.', '#', 'F', '#', '.'],
    ['.', '.', 'E', '.', 'X'],
    ['#', '#', 'O', '#', '.'],
    ['.', '.', '.', '.', 'G']
]

ROWS, COLS = 5, 5

PLAYER_START = (0, 0)
ENEMY_START = (2, 4)
GOAL = (4, 4)

COST_MAP = {
    '.': 1,
    'P': 1,
    'X': 1,
    'G': 1,
    'F': 10,
    'O': 10,
    'E': 20
}

WIN_SCORE = 10000
SEARCH_DEPTH = 4
MAX_ROUNDS = 30


# ---------------- NEIGHBORS ----------------

def get_neighbors(pos):
    r, c = pos

    for dr, dc in [(-1, 0), (1, 0),
                   (0, -1), (0, 1)]:

        nr, nc = r + dr, c + dc

        if (0 <= nr < ROWS and
            0 <= nc < COLS and
            maze[nr][nc] != '#'):

            yield (nr, nc)


# ---------------- DISTANCE ----------------

def shortest_distance(start, target):
    """Find shortest distance while considering walls."""

    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        pos, dist = queue.popleft()

        if pos == target:
            return dist

        for n in get_neighbors(pos):
            if n not in visited:
                visited.add(n)
                queue.append((n, dist + 1))

    return 999


# ---------------- A* SEARCH ----------------

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(start, goal):

    tie = count()

    pq = [
        (heuristic(start, goal), 0,
         next(tie), start, [start])
    ]

    g_score = {start: 0}
    visited = set()
    nodes = 0

    while pq:

        f, cost, _, pos, path = heapq.heappop(pq)

        # Ignore outdated entries
        if cost != g_score.get(pos):
            continue

        if pos in visited:
            continue

        visited.add(pos)
        nodes += 1

        if pos == goal:
            return path, cost, nodes

        for n in get_neighbors(pos):

            new_cost = cost + COST_MAP[maze[n[0]][n[1]]]

            if new_cost < g_score.get(n, float('inf')):

                g_score[n] = new_cost

                new_f = new_cost + heuristic(n, goal)

                heapq.heappush(
                    pq,
                    (new_f, new_cost, next(tie),
                     n, path + [n])
                )

    return None, float('inf'), nodes


# ---------------- EVALUATION FUNCTION ----------------

def evaluate(player_pos, enemy_pos):

    # Enemy catches Player
    if player_pos == enemy_pos:
        return -WIN_SCORE

    # Player reaches Goal
    if player_pos == GOAL:
        return WIN_SCORE

    dist_goal = shortest_distance(player_pos, GOAL)
    dist_enemy = shortest_distance(player_pos, enemy_pos)

    # Player wants high score
    # Enemy wants low score

    return (dist_enemy * 2) - (dist_goal * 5)


# ---------------- MINIMAX ----------------

def minimax_search(player_pos, enemy_pos, depth, is_max):

    minimax_search.nodes += 1

    if (depth == 0 or
        player_pos == GOAL or
        player_pos == enemy_pos):

        return evaluate(player_pos, enemy_pos)

    if is_max:

        moves = list(get_neighbors(player_pos))

        if not moves:
            return -WIN_SCORE + depth

        best = -float('inf')

        for n in moves:

            score = minimax_search(
                n, enemy_pos, depth - 1, False
            )

            best = max(best, score)

        return best

    else:

        moves = list(get_neighbors(enemy_pos))

        if not moves:
            return WIN_SCORE - depth

        best = float('inf')

        for n in moves:

            score = minimax_search(
                player_pos, n, depth - 1, True
            )

            best = min(best, score)

        return best


minimax_search.nodes = 0


# ---------------- ALPHA-BETA PRUNING ----------------

def alphabeta_search(player_pos, enemy_pos,
                     depth, alpha, beta, is_max):

    alphabeta_search.nodes += 1

    if (depth == 0 or
        player_pos == GOAL or
        player_pos == enemy_pos):

        return evaluate(player_pos, enemy_pos)

    if is_max:

        moves = list(get_neighbors(player_pos))

        if not moves:
            return -WIN_SCORE + depth

        best = -float('inf')

        for n in moves:

            score = alphabeta_search(
                n, enemy_pos, depth - 1,
                alpha, beta, False
            )

            best = max(best, score)
            alpha = max(alpha, best)

            # Pruning
            if beta <= alpha:
                break

        return best

    else:

        moves = list(get_neighbors(enemy_pos))

        if not moves:
            return WIN_SCORE - depth

        best = float('inf')

        for n in moves:

            score = alphabeta_search(
                player_pos, n, depth - 1,
                alpha, beta, True
            )

            best = min(best, score)
            beta = min(beta, best)

            # Pruning
            if beta <= alpha:
                break

        return best


alphabeta_search.nodes = 0


# ---------------- BEST MOVE SELECTION ----------------

def best_move(player_pos, enemy_pos, is_max,
              use_alpha_beta):

    if is_max:
        moves = list(get_neighbors(player_pos))
    else:
        moves = list(get_neighbors(enemy_pos))

    if not moves:
        return None, evaluate(player_pos, enemy_pos), 0

    best_score = (
        -float('inf') if is_max else float('inf')
    )

    selected_move = None

    nodes_before = (
        alphabeta_search.nodes
        if use_alpha_beta
        else minimax_search.nodes
    )

    alpha = -float('inf')
    beta = float('inf')

    for n in moves:

        if is_max:

            if use_alpha_beta:
                score = alphabeta_search(
                    n, enemy_pos, SEARCH_DEPTH - 1,
                    alpha, beta, False
                )
            else:
                score = minimax_search(
                    n, enemy_pos,
                    SEARCH_DEPTH - 1, False
                )

            if score > best_score:
                best_score = score
                selected_move = n

            if use_alpha_beta:
                alpha = max(alpha, best_score)

        else:

            if use_alpha_beta:
                score = alphabeta_search(
                    player_pos, n, SEARCH_DEPTH - 1,
                    alpha, beta, True
                )
            else:
                score = minimax_search(
                    player_pos, n,
                    SEARCH_DEPTH - 1, True
                )

            if score < best_score:
                best_score = score
                selected_move = n

            if use_alpha_beta:
                beta = min(beta, best_score)

            if use_alpha_beta and beta <= alpha:
                break

    nodes_after = (
        alphabeta_search.nodes
        if use_alpha_beta
        else minimax_search.nodes
    )

    return selected_move, best_score, nodes_after - nodes_before


# ---------------- GAME SIMULATION ----------------

def play_game():

    player_pos = PLAYER_START
    enemy_pos = ENEMY_START

    print("\n=== MAZEXPLORER: AI VS AI ===")
    print("Player: MAX")
    print("Enemy: MIN")
    print("Decision Algorithm: Alpha-Beta Pruning")
    print("")

    for round_no in range(1, MAX_ROUNDS + 1):

        print(f"\n--- Round {round_no} ---")

        # PLAYER TURN

        move, score, _ = best_move(
            player_pos, enemy_pos,
            True, True
        )

        if move is None:
            print("Player has no legal moves!")
            print("Enemy Wins!")
            return

        player_pos = move

        print("Player moves to:", player_pos)
        print("Player Score:", score)

        if player_pos == enemy_pos:
            print("Enemy caught the Player!")
            print("Enemy Wins!")
            return

        if player_pos == GOAL:
            print("Player reached the Goal!")
            print("Player Wins!")
            return

        # ENEMY TURN

        move, score, _ = best_move(
            player_pos, enemy_pos,
            False, True
        )

        if move is None:
            print("Enemy has no legal moves!")
            print("Player Wins!")
            return

        enemy_pos = move

        print("Enemy moves to:", enemy_pos)

        if player_pos == enemy_pos:
            print("Enemy caught the Player!")
            print("Enemy Wins!")
            return

    print("\nMaximum rounds reached!")
    print("Game ended without a winner.")


# ---------------- FINAL COMPARISON ----------------

print("====================================")
print(" MAZEXPLORER PART 3: FINAL PROJECT")
print("====================================")

# A* PATHFINDING

path, cost, astar_nodes = astar(
    PLAYER_START, GOAL
)

print("\n--- A* SEARCH RESULT ---")

print("A* Path:", path)
print("A* Total Cost:", cost)
print("A* Nodes Explored:", astar_nodes)


# MINIMAX VS ALPHA-BETA

print("\n--- ALGORITHM COMPARISON ---")

minimax_move, minimax_score, minimax_nodes = best_move(
    PLAYER_START, ENEMY_START,
    True, False
)

alphabeta_move, alphabeta_score, alphabeta_nodes = best_move(
    PLAYER_START, ENEMY_START,
    True, True
)

print("Minimax Best Move:", minimax_move)
print("Minimax Score:", minimax_score)
print("Minimax Nodes Explored:", minimax_nodes)

print("\nAlpha-Beta Best Move:", alphabeta_move)
print("Alpha-Beta Score:", alphabeta_score)
print("Alpha-Beta Nodes Explored:", alphabeta_nodes)

if minimax_score == alphabeta_score:
    print("\nBoth algorithms found the same optimal score.")

if minimax_move == alphabeta_move:
    print("Both algorithms selected the same move.")
else:
    print("Different moves selected with equal or different scores.")

print("\nNodes Saved:",
      minimax_nodes - alphabeta_nodes)

if alphabeta_nodes < minimax_nodes:
    print("Alpha-Beta explored fewer nodes.")
elif alphabeta_nodes == minimax_nodes:
    print("Both explored the same number of nodes.")
else:
    print("Alpha-Beta explored more nodes in this search.")

# ACTUAL GAME

play_game()

print("\n====================================")
print(" SERIES COMPLETED")
print(" BFS -> DFS -> UCS -> A*")
print(" -> Minimax -> Alpha-Beta Pruning")
print("====================================")
