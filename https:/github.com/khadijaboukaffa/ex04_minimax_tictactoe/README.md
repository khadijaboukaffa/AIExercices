# Tic-Tac-Toe Minimax Variants

## Files
- `minimax_scores.py` → shows the score of each possible move
- `minimax_play.py` → interactive game against the AI
- `minimax_alphabeta.py` → Minimax with alpha-beta pruning

## Concepts Used
- Game state
- Actions
- Result
- Terminal state
- Utility function
- Minimax
- Alpha-beta pruning

## Scores
- X win = 1
- Draw = 0
- O win = -1

## Run
```bash
python3 minimax_scores.py
python3 minimax_play.py
python3 minimax_alphabeta.py

## compare_minimax.py

This file compares:
- standard Minimax
- Minimax with Alpha-Beta pruning

It displays:
- best move
- best score
- number of evaluated nodes
- execution time

Run:
```bash
python3 compare_minimax.py


## compare_minimax_table.py

This script compares:
- standard Minimax
- Minimax with Alpha-Beta pruning

It displays a formatted comparison table with:
- best move
- score
- number of evaluated nodes
- execution time
- nodes saved by Alpha-Beta

Run:
```bash
python3 compare_minimax_table.py