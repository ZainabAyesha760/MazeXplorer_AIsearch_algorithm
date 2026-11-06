# maze_xplorer_part3.py - FINAL Part of AI Search Algorithm Series
# Part 3: AI vs AI - Minimax vs Alpha-Beta Pruning

from collections import deque
import heapq

# Maze: S=Start, G=Goal, #=Wall, .=Cost1, F,O=Mud Cost10, E=Water Cost20
# P = Player, X = Enemy
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

COST_MAP = {'.':1, 'P':1, 'X':1, 'G':1, 'F':10, 'O':10, 'E':20}

def get_neighbors(pos):
    r, c = pos
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] != '#':
            yield (nr, nc)

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# ---------- PART 2 se liya hua A* - Player ke liye ----------
def astar(start, goal):
    pq = [(heuristic(start, goal), 0, start, [start])]
    visited = set()
    nodes = 0
    while pq:
        f, cost, pos, path = heapq.heappop(pq)
        if pos in visited: continue
        visited.add(pos)
        nodes += 1
        if pos == goal:
            return path, nodes
        for n in get_neighbors(pos):
            if n not in visited:
                new_cost = cost + COST_MAP[maze[n[0]][n[1]]]
                heapq.heappush(pq, (new_cost + heuristic(n, goal), new_cost, n, path + [n]))
    return None, nodes

# ---------- PART 3: Minimax + Alpha-Beta ----------
# Player chahta hai Goal ke qareeb jaye (Score +)
# Enemy chahta hai Player ke qareeb aaye (Score -)

nodes_minimax = 0
nodes_alphabeta = 0

def evaluate(player_pos, enemy_pos):
    # Agar Enemy ne pakar liya
    if player_pos == enemy_pos:
        return -100
    # Agar Player Goal pe pahunch gaya
    if player_pos == GOAL:
        return 100
    # Score = Enemy se doori - Goal se doori
    dist_to_goal = heuristic(player_pos, GOAL)
    dist_from_enemy = heuristic(player_pos, enemy_pos)
    return dist_from_enemy * 2 - dist_to_goal * 5

def minimax(player_pos, enemy_pos, depth, is_max):
    global nodes_minimax
    nodes_minimax += 1
    if depth == 0 or player_pos == GOAL or player_pos == enemy_pos:
        return evaluate(player_pos, enemy_pos)

    if is_max: # Player ki baari - Max karega
        best = -9999
        for n in get_neighbors(player_pos):
            best = max(best, minimax(n, enemy_pos, depth-1, False))
        return best
    else: # Enemy ki baari - Min karega
        best = 9999
        for n in get_neighbors(enemy_pos):
            best = min(best, minimax(player_pos, n, depth-1, True))
        return best

def alphabeta(player_pos, enemy_pos, depth, alpha, beta, is_max):
    global nodes_alphabeta
    nodes_alphabeta += 1
    if depth == 0 or player_pos == GOAL or player_pos == enemy_pos:
        return evaluate(player_pos, enemy_pos)

    if is_max:
        best = -9999
        for n in get_neighbors(player_pos):
            best = max(best, alphabeta(n, enemy_pos, depth-1, alpha, beta, False))
            alpha = max(alpha, best)
            if beta <= alpha: # PRUNING - Yahan kaam khatam
                break
        return best
    else:
        best = 9999
        for n in get_neighbors(enemy_pos):
            best = min(best, alphabeta(player_pos, n, depth-1, alpha, beta, True))
            beta = min(beta, best)
            if beta <= alpha: # PRUNING
                break
        return best

def best_move_minimax(player_pos, enemy_pos):
    best_score = -9999
    best_move = player_pos
    for n in get_neighbors(player_pos):
        score = minimax(n, enemy_pos, 2, False)
        if score > best_score:
            best_score = score
            best_move = n
    return best_move

def best_move_alphabeta(player_pos, enemy_pos):
    best_score = -9999
    best_move = player_pos
    for n in get_neighbors(player_pos):
        score = alphabeta(n, enemy_pos, 2, -9999, 9999, False)
        if score > best_score:
            best_score = score
            best_move = n
    return best_move

# ---------- FINAL GAME SIMULATION ----------
print("=== MazeXplorer Part 3 FINAL: AI vs AI ===")
print("Player: A* + Minimax | Enemy: A* Chaser")
print("")

# Pehle A* se rasta check karo
path, nodes = astar(PLAYER_START, GOAL)
print(f"A* Path: {path}")
print(f"A* Nodes: {nodes} | Cost: {sum(COST_MAP[maze[r][c]] for r,c in path[1:])}")
print("")

# Ab Minimax vs Alpha-Beta Compare karo
p_pos = PLAYER_START
e_pos = ENEMY_START

move1 = best_move_minimax(p_pos, e_pos)
print(f"Minimax Best Move: {p_pos} -> {move1} | Nodes Explored: {nodes_minimax}")

p_pos = PLAYER_START
move2 = best_move_alphabeta(p_pos, e_pos)
print(f"Alpha-Beta Best Move: {p_pos} -> {move2} | Nodes Explored: {nodes_alphabeta}")

print("")
print(f"Result: Alpha-Beta ne {nodes_minimax - nodes_alphabeta} nodes kam explore kiye!")
print("Winner: Alpha-Beta - Same Smart Decision, Faster!")
print("")
print("Series Completed: BFS -> DFS -> UCS -> A* -> Minimax -> Alpha-Beta")
