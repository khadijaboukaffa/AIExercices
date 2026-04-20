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