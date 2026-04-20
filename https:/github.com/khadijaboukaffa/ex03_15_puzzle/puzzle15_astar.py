import heapq


GOAL_STATE = (
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 0
)


def print_board(state):
    """
    Affiche le puzzle de façon lisible.
    0 représente la case vide.
    """
    for i in range(0, 16, 4):
        row = state[i:i+4]
        print(" ".join(f"{num:2}" if num != 0 else " _" for num in row))
    print()


def get_blank_index(state):
    """
    Retourne l'index de la case vide (0).
    """
    return state.index(0)


def get_neighbors(state):
    """
    Retourne tous les états voisins possibles.
    Chaque voisin correspond à un mouvement de la case vide.
    """
    neighbors = []
    blank = get_blank_index(state)

    row = blank // 4
    col = blank % 4

    moves = []

    if row > 0:
        moves.append(("up", blank - 4))
    if row < 3:
        moves.append(("down", blank + 4))
    if col > 0:
        moves.append(("left", blank - 1))
    if col < 3:
        moves.append(("right", blank + 1))

    for move_name, new_blank in moves:
        new_state = list(state)

        # Échanger la case vide avec la case voisine
        new_state[blank], new_state[new_blank] = new_state[new_blank], new_state[blank]

        neighbors.append((move_name, tuple(new_state)))

    return neighbors


def manhattan_distance(state):
    """
    Heuristique A* :
    somme des distances de Manhattan de chaque tuile à sa position finale.
    """
    distance = 0

    for index, value in enumerate(state):
        if value == 0:
            continue

        current_row = index // 4
        current_col = index % 4

        goal_index = value - 1
        goal_row = goal_index // 4
        goal_col = goal_index % 4

        distance += abs(current_row - goal_row) + abs(current_col - goal_col)

    return distance


def reconstruct_path(came_from, current):
    """
    Reconstruit le chemin depuis l'état initial jusqu'au goal.
    """
    path = []

    while current in came_from:
        previous_state, move = came_from[current]
        path.append((move, current))
        current = previous_state

    path.reverse()
    return path


def a_star(start_state):
    """
    Résout le 15-puzzle avec A*.
    Retourne :
    - path : liste des mouvements
    - explored_nodes : nombre d'états explorés
    """
    frontier = []
    heapq.heappush(frontier, (manhattan_distance(start_state), 0, start_state))

    came_from = {}
    g_score = {start_state: 0}
    explored = set()
    explored_nodes = 0

    while frontier:
        f, g, current = heapq.heappop(frontier)

        if current in explored:
            continue

        explored.add(current)
        explored_nodes += 1

        if current == GOAL_STATE:
            path = reconstruct_path(came_from, current)
            return path, explored_nodes

        for move, neighbor in get_neighbors(current):
            if neighbor in explored:
                continue

            tentative_g = g + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                came_from[neighbor] = (current, move)
                f_score = tentative_g + manhattan_distance(neighbor)
                heapq.heappush(frontier, (f_score, tentative_g, neighbor))

    return None, explored_nodes


def main():
    # Exemple simple, proche de la solution
    start_state = (
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 10, 11, 12,
        13, 0, 14, 15
    )

    print("=== START STATE ===")
    print_board(start_state)

    print("=== GOAL STATE ===")
    print_board(GOAL_STATE)

    path, explored_nodes = a_star(start_state)

    if path is None:
        print("No solution found.")
        print(f"Explored nodes: {explored_nodes}")
        return

    print("=== SOLUTION FOUND ===")
    print(f"Number of explored nodes: {explored_nodes}")
    print(f"Number of moves in solution: {len(path)}")
    print()

    current_state = start_state
    print("Initial board:")
    print_board(current_state)

    step = 1
    for move, state in path:
        print(f"Step {step}: move blank {move}")
        print_board(state)
        step += 1


if __name__ == "__main__":
    main()