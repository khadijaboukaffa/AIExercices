# Maze Solver Project

## Description
This project solves text-based mazes using different search algorithms.

## Files
- `maze_bfs.py` → Breadth-First Search
- `maze_dfs.py` → Depth-First Search
- `maze_astar.py` → A* Search
- `maze_png.py` → BFS + PNG output
- `maze1.txt` → example maze

## Maze Format
- `A` = start
- `B` = goal
- `#` = wall
- space = free cell

## Run BFS
```bash
python3 maze_bfs.py maze1.txt


## compare_search.py

This script compares three search algorithms on the same maze:
- BFS
- DFS
- A*

It displays:
- path length
- number of explored states
- execution time
- solution path
- explored states

Run:
```bash
python3 compare_search.py maze1.txt