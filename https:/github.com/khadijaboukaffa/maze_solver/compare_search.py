import sys
import time
import heapq


class Node:
    def __init__(self, state, parent, action, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        return self.frontier.pop()


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        return self.frontier.pop(0)


class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point A")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal point B")

        lines = contents.splitlines()
        self.height = len(lines)
        self.width = max(len(line) for line in lines)

        self.walls = []
        self.start = None
        self.goal = None

        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    char = lines[i][j]
                except IndexError:
                    char = " "

                if char == "A":
                    self.start = (i, j)
                    row.append(False)
                elif char == "B":
                    self.goal = (i, j)
                    row.append(False)
                elif char == "#":
                    row.append(True)
                else:
                    row.append(False)

            self.walls.append(row)

    def print(self, solution=None, explored=None):
        """
        Affiche le labyrinthe.
        - solution: liste de cellules du chemin
        - explored: set des cellules explorées
        """
        print()

        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)

                if self.walls[i][j]:
                    print("█", end="")
                elif cell == self.start:
                    print("A", end="")
                elif cell == self.goal:
                    print("B", end="")
                elif solution is not None and cell in solution:
                    print("*", end="")
                elif explored is not None and cell in explored:
                    print(".", end="")
                else:
                    print(" ", end="")
            print()

        print()

    def neighbors(self, state):
        row, col = state

        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []

        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))

        return result

    def heuristic(self, state):
        """
        Distance de Manhattan jusqu'au but.
        """
        row, col = state
        goal_row, goal_col = self.goal
        return abs(row - goal_row) + abs(col - goal_col)


def reconstruct_solution(node):
    """
    Reconstruit le chemin depuis le départ jusqu'au goal.
    Retourne :
    - actions
    - cells
    """
    actions = []
    cells = []

    while node.parent is not None:
        actions.append(node.action)
        cells.append(node.state)
        node = node.parent

    actions.reverse()
    cells.reverse()

    return actions, cells


def solve_bfs(maze):
    frontier = QueueFrontier()
    start = Node(state=maze.start, parent=None, action=None, cost=0)
    frontier.add(start)

    explored = set()
    num_explored = 0

    while True:
        if frontier.empty():
            raise Exception("No solution")

        node = frontier.remove()
        num_explored += 1

        if node.state == maze.goal:
            actions, cells = reconstruct_solution(node)
            return {
                "algorithm": "BFS",
                "actions": actions,
                "cells": cells,
                "path_length": len(actions),
                "states_explored": num_explored,
                "explored_set": explored
            }

        explored.add(node.state)

        for action, state in maze.neighbors(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action, cost=node.cost + 1)
                frontier.add(child)


def solve_dfs(maze):
    frontier = StackFrontier()
    start = Node(state=maze.start, parent=None, action=None, cost=0)
    frontier.add(start)

    explored = set()
    num_explored = 0

    while True:
        if frontier.empty():
            raise Exception("No solution")

        node = frontier.remove()
        num_explored += 1

        if node.state == maze.goal:
            actions, cells = reconstruct_solution(node)
            return {
                "algorithm": "DFS",
                "actions": actions,
                "cells": cells,
                "path_length": len(actions),
                "states_explored": num_explored,
                "explored_set": explored
            }

        explored.add(node.state)

        for action, state in reversed(maze.neighbors(node.state)):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action, cost=node.cost + 1)
                frontier.add(child)


def solve_astar(maze):
    start = Node(state=maze.start, parent=None, action=None, cost=0)

    frontier = []
    counter = 0
    heapq.heappush(frontier, (maze.heuristic(maze.start), counter, start))

    explored = set()
    num_explored = 0
    best_cost = {maze.start: 0}

    while frontier:
        _, _, node = heapq.heappop(frontier)

        if node.state in explored:
            continue

        explored.add(node.state)
        num_explored += 1

        if node.state == maze.goal:
            actions, cells = reconstruct_solution(node)
            return {
                "algorithm": "A*",
                "actions": actions,
                "cells": cells,
                "path_length": len(actions),
                "states_explored": num_explored,
                "explored_set": explored
            }

        for action, state in maze.neighbors(node.state):
            new_cost = node.cost + 1

            if state not in best_cost or new_cost < best_cost[state]:
                best_cost[state] = new_cost
                child = Node(state=state, parent=node, action=action, cost=new_cost)
                priority = new_cost + maze.heuristic(state)
                counter += 1
                heapq.heappush(frontier, (priority, counter, child))

    raise Exception("No solution")


def format_seconds(value):
    return f"{value:.6f}s"


def print_results_table(results):
    headers = ["Algorithm", "Path Length", "States Explored", "Time"]
    rows = []

    for result in results:
        rows.append([
            result["algorithm"],
            str(result["path_length"]),
            str(result["states_explored"]),
            format_seconds(result["time"])
        ])

    widths = []
    for i in range(len(headers)):
        max_len = len(headers[i])
        for row in rows:
            max_len = max(max_len, len(row[i]))
        widths.append(max_len)

    def make_separator():
        return "+-" + "-+-".join("-" * w for w in widths) + "-+"

    def make_row(values):
        return "| " + " | ".join(values[i].ljust(widths[i]) for i in range(len(values))) + " |"

    print(make_separator())
    print(make_row(headers))
    print(make_separator())
    for row in rows:
        print(make_row(row))
    print(make_separator())
    print()


def run_algorithm(maze, solve_function):
    start_time = time.perf_counter()
    result = solve_function(maze)
    elapsed = time.perf_counter() - start_time
    result["time"] = elapsed
    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 compare_search.py maze1.txt")
        sys.exit(1)

    filename = sys.argv[1]
    maze = Maze(filename)

    print("Maze:")
    maze.print()

    bfs_result = run_algorithm(maze, solve_bfs)
    dfs_result = run_algorithm(maze, solve_dfs)
    astar_result = run_algorithm(maze, solve_astar)

    results = [bfs_result, dfs_result, astar_result]

    print("Comparison:")
    print_results_table(results)

    print("BFS solution:")
    maze.print(solution=bfs_result["cells"])

    print("DFS solution:")
    maze.print(solution=dfs_result["cells"])

    print("A* solution:")
    maze.print(solution=astar_result["cells"])

    print("BFS explored states:")
    maze.print(explored=bfs_result["explored_set"])

    print("DFS explored states:")
    maze.print(explored=dfs_result["explored_set"])

    print("A* explored states:")
    maze.print(explored=astar_result["explored_set"])


if __name__ == "__main__":
    main()