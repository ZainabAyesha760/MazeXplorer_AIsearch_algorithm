MazeXplorer – Part 3: AI vs AI

Minimax vs Alpha-Beta Pruning

1. Project Overview

MazeXplorer Part 3 is the final part of an AI Search Algorithm Series. This project demonstrates how Artificial Intelligence algorithms make decisions in a maze environment.

In this project, A* Search is used for pathfinding, while Minimax and Alpha-Beta Pruning are used for intelligent decision-making between two AI agents.

The Player tries to reach the Goal while avoiding the Enemy. Both agents make decisions using adversarial search algorithms.

2. Project Objectives

- Understand how Minimax works in an AI game environment.
- Implement Alpha-Beta Pruning to optimize decision-making.
- Compare Minimax and Alpha-Beta Pruning.
- Understand how AI agents make decisions against each other.
- Use A* Search to find a least-cost path from Start to Goal.
- Compare the number of nodes explored by both algorithms.

3. Maze Description

The project uses a 5×5 maze.

Symbol| Meaning| Movement Cost
P| Player| 1
X| Enemy| 1
G| Goal| 1
.| Normal Path| 1
#| Wall| Not allowed
F| Mud| 10
O| Mud| 10
E| Water| 20

Maze Layout:

P  .  .  #  .
.  #  F  #  .
.  .  E  .  X
#  #  O  #  .
.  .  .  .  G

4. Algorithms Used

A. A Search Algorithm*

A* is an informed search algorithm used to find a least-cost path from the starting position to the goal.

It uses the following formula:

f(n) = g(n) + h(n)

- g(n): Actual cost from the start node.
- h(n): Estimated distance to the goal.
- f(n): Total estimated cost.

In this project, A* uses Manhattan Distance as its heuristic and maintains the best known path cost using "g_score".

B. Minimax Algorithm

Minimax is a decision-making algorithm used in two-player competitive games.

It assumes that:

- The Player is the MAX player and tries to maximize the score.
- The Enemy is the MIN player and tries to minimize the score.
- Both players make intelligent decisions.
- The algorithm explores possible moves up to a specified search depth.

The Player tries to reach the Goal, while the Enemy tries to catch the Player.

C. Alpha-Beta Pruning

Alpha-Beta Pruning is an optimization technique of the Minimax algorithm.

It reduces unnecessary node exploration by skipping branches that cannot affect the final decision.

It uses two values:

- Alpha (α): Best value currently available to MAX.
- Beta (β): Best value currently available to MIN.

Pruning Condition:

if beta <= alpha:
    break

When Beta becomes less than or equal to Alpha, the remaining branches are skipped.

5. Evaluation Function

The evaluation function calculates how good a position is for the Player.

It considers:

- Distance from the Goal.
- Distance from the Enemy.
- Whether the Player has reached the Goal.
- Whether the Enemy has caught the Player.

The evaluation formula is:

Score = (Distance from Enemy × 2) - (Distance to Goal × 5)

Special scores:

- Player caught by Enemy = -10000
- Player reaches Goal = +10000

A higher score is better for the Player, while a lower score is better for the Enemy.

6. How the Program Works

1. The program creates a 5×5 maze.
2. It defines the Player, Enemy and Goal positions.
3. It uses A* Search to calculate a least-cost path to the Goal.
4. It runs Minimax to calculate the Player's best move.
5. It runs Alpha-Beta Pruning to calculate the Player's best move.
6. It compares the scores and number of nodes explored by both algorithms.
7. It starts an actual turn-by-turn game simulation.
8. The Player and Enemy take turns selecting their moves using Alpha-Beta Pruning.
9. The game ends when the Player reaches the Goal, the Enemy catches the Player, or the maximum number of rounds is reached.

7. Technologies Used

- Programming Language: Python 3
- Artificial Intelligence
- Search Algorithms
- Game Tree Search

Python Libraries:

- "heapq" – Priority queue for A* Search.
- "collections" – Queue support.
- "itertools" – Unique priority queue tie-breaking.

No external libraries are required.

8. How to Run the Project

Step 1: Install Python 3.

Step 2: Save the program as:

maze_xplorer_part3.py

Step 3: Open the terminal in the project folder.

Step 4: Run the following command:

python maze_xplorer_part3.py

9. Expected Output

The program displays:

- A* calculated path.
- A* total path cost.
- A* nodes explored.
- Best move selected by Minimax.
- Best move selected by Alpha-Beta Pruning.
- Scores calculated by both algorithms.
- Number of nodes explored by both algorithms.
- Nodes saved through pruning.
- Actual AI vs AI game simulation.
- Final game result.

Note: Exact output values depend on the execution of the program.

10. Minimax vs Alpha-Beta Pruning

Minimax| Alpha-Beta Pruning
Explores possible branches up to the search depth.| Skips unnecessary branches.
Does not use pruning.| Uses Alpha and Beta values.
Can explore more nodes.| Can explore fewer nodes.
Provides the best decision within the search depth.| Provides the same optimal score as Minimax.
Uses MAX and MIN decisions.| Uses MAX and MIN decisions with pruning.

11. Advantages

- Demonstrates intelligent decision-making.
- Shows how two AI agents compete.
- Reduces unnecessary search through pruning.
- Helps understand game-tree search.
- Demonstrates pathfinding using A*.
- Compares the performance of search algorithms.

12. Conclusion

MazeXplorer Part 3 demonstrates how Artificial Intelligence can solve pathfinding and decision-making problems in a competitive maze environment.

A* Search is used to find a least-cost path, while Minimax and Alpha-Beta Pruning are used for intelligent decision-making between two AI agents.

Both Minimax and Alpha-Beta Pruning aim to produce the same optimal score within the given search depth. However, Alpha-Beta Pruning can improve efficiency by avoiding unnecessary branches.

This project completes the AI Search Algorithm Series:

BFS → DFS → UCS → A → Minimax → Alpha-Beta Pruning*
