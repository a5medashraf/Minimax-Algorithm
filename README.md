# Minmax-Algorithm

## Introduction
A Strategic Implementation for Connect Four Game AI

## Methodology
**Game Representation:** Connect Four game boards with a grid of 7 columns by 6 rows. Each cell in the grid can be empty, occupied by player one, or occupied by player two.

**Minimax Algorithm:** Implement the minimax algorithm, which is a recursive strategy for minimizing the possible loss in a worst-case scenario. This algorithm will be used to determine the best move for the AI.

**Depth-Limited Search:** To keep the computation manageable, apply a depth limit to the minimax search. The AI will look ahead to a certain number of moves and evaluate the board positions.

**Evaluation Function:** Design an evaluation function to score the game board. This function assesses the board and gives higher scores for more favorable positions for the AI.

**Alpha-Beta Pruning:** Integrate alpha-beta pruning into the minimax algorithm. This technique "prunes" branches in the search tree that don't need to be explored because they can't possibly influence the final decision, significantly improving efficiency.

**Game Modes:** Develop different game modes, including AI vs. AI, AI vs. Human, and Minimax with Pruning vs. Normal Minimax. Each mode will showcase different aspects of the AI's capabilities.


## User Interface: 


<img src="https://github.com/a5medashraf/Minimax-Algorithm/assets/72763763/06c944ac-ee5d-4497-ba52-68da19fa6c9d" width="900" height="500">

