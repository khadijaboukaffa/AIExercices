class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


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
        self.solution = None

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

    def print(self, show_explored=False):
        solution = self.solution[1] if self.solution is not None else None

        print()
        for i in range(self.height):
            for j in range(self.width):
                if self.walls[i][j]:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                elif show_explored and hasattr(self, "explored") and (i, j) in self.explored:
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

    def solve(self):
        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)

        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("No solution")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


def main():
    maze = Maze("maze1.txt")

    print("Maze:")
    maze.print()

    print("Solving...")
    maze.solve()

    print("Solved!")
    print("States explored:", maze.num_explored)
    print("Solution actions:", maze.solution[0])

    print("Explored states:")
    maze.print(show_explored=True)

    print("Final path:")
    maze.print()


if __name__ == "__main__":
    main()