import time

X = "X"
O = "O"
EMPTY = None

minimax_nodes = 0
alphabeta_nodes = 0


def print_board(board):
    """
    Affiche le plateau.
    """
    for row in board:
        display_row = []
        for cell in row:
            display_row.append(cell if cell is not None else "_")
        print(" ".join(display_row))
    print()


def player(board):
    """
    Retourne le joueur qui doit jouer.
    """
    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1

    return X if x_count <= o_count else O


def actions(board):
    """
    Retourne tous les coups possibles.
    """
    moves = []

    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                moves.append((i, j))

    return moves


def result(board, action):
    """
    Retourne un nouveau plateau après un coup.
    """
    i, j = action

    if board[i][j] is not EMPTY:
        raise ValueError("Invalid move: cell already occupied")

    new_board = [row.copy() for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Retourne le gagnant s'il existe.
    """
    for row in board:
        if row[0] is not None and row[0] == row[1] == row[2]:
            return row[0]

    for col in range(3):
        if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]

    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None


def terminal(board):
    """
    Retourne True si la partie est finie.
    """
    if winner(board) is not None:
        return True

    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False

    return True


def utility(board):
    """
    Retourne le score final.
    X gagne  ->  1
    O gagne  -> -1
    Draw     ->  0
    """
    game_winner = winner(board)

    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


# =========================================================
# MINIMAX
# =========================================================

def max_value_minimax(board):
    global minimax_nodes
    minimax_nodes += 1

    if terminal(board):
        return utility(board)

    v = float("-inf")
    for action in actions(board):
        v = max(v, min_value_minimax(result(board, action)))
    return v


def min_value_minimax(board):
    global minimax_nodes
    minimax_nodes += 1

    if terminal(board):
        return utility(board)

    v = float("inf")
    for action in actions(board):
        v = min(v, max_value_minimax(result(board, action)))
    return v


def minimax(board):
    """
    Retourne (best_action, best_score)
    """
    if terminal(board):
        return None, utility(board)

    current_player = player(board)

    if current_player == X:
        best_score = float("-inf")
        best_action = None

        for action in actions(board):
            score = min_value_minimax(result(board, action))
            if score > best_score:
                best_score = score
                best_action = action

        return best_action, best_score

    else:
        best_score = float("inf")
        best_action = None

        for action in actions(board):
            score = max_value_minimax(result(board, action))
            if score < best_score:
                best_score = score
                best_action = action

        return best_action, best_score


# =========================================================
# ALPHA-BETA
# =========================================================

def max_value_alphabeta(board, alpha, beta):
    global alphabeta_nodes
    alphabeta_nodes += 1

    if terminal(board):
        return utility(board)

    v = float("-inf")

    for action in actions(board):
        v = max(v, min_value_alphabeta(result(board, action), alpha, beta))
        alpha = max(alpha, v)

        if alpha >= beta:
            break

    return v


def min_value_alphabeta(board, alpha, beta):
    global alphabeta_nodes
    alphabeta_nodes += 1

    if terminal(board):
        return utility(board)

    v = float("inf")

    for action in actions(board):
        v = min(v, max_value_alphabeta(result(board, action), alpha, beta))
        beta = min(beta, v)

        if alpha >= beta:
            break

    return v


def minimax_alphabeta(board):
    """
    Retourne (best_action, best_score)
    """
    if terminal(board):
        return None, utility(board)

    current_player = player(board)

    if current_player == X:
        best_score = float("-inf")
        best_action = None
        alpha = float("-inf")
        beta = float("inf")

        for action in actions(board):
            score = min_value_alphabeta(result(board, action), alpha, beta)

            if score > best_score:
                best_score = score
                best_action = action

            alpha = max(alpha, best_score)

        return best_action, best_score

    else:
        best_score = float("inf")
        best_action = None
        alpha = float("-inf")
        beta = float("inf")

        for action in actions(board):
            score = max_value_alphabeta(result(board, action), alpha, beta)

            if score < best_score:
                best_score = score
                best_action = action

            beta = min(beta, best_score)

        return best_action, best_score


# =========================================================
# DISPLAY HELPERS
# =========================================================

def format_seconds(value):
    return f"{value:.6f}s"


def print_comparison_table(title, minimax_move, minimax_score, minimax_nodes_count, minimax_time,
                           alphabeta_move, alphabeta_score, alphabeta_nodes_count, alphabeta_time):
    """
    Affiche un tableau propre dans le terminal.
    """
    headers = ["Algorithm", "Best Move", "Score", "Nodes", "Time"]
    rows = [
        ["Minimax", str(minimax_move), str(minimax_score), str(minimax_nodes_count), format_seconds(minimax_time)],
        ["Alpha-Beta", str(alphabeta_move), str(alphabeta_score), str(alphabeta_nodes_count), format_seconds(alphabeta_time)],
    ]

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

    print(title)
    print(make_separator())
    print(make_row(headers))
    print(make_separator())
    for row in rows:
        print(make_row(row))
    print(make_separator())
    print()

    print("Same move? ", minimax_move == alphabeta_move)
    print("Same score?", minimax_score == alphabeta_score)

    if alphabeta_nodes_count > 0:
        saved = minimax_nodes_count - alphabeta_nodes_count
        percent = (saved / minimax_nodes_count) * 100 if minimax_nodes_count > 0 else 0
        print(f"Nodes saved by Alpha-Beta: {saved} ({percent:.2f}%)")

    print()


def compare_algorithms(board, title="Comparison"):
    global minimax_nodes, alphabeta_nodes

    print("=" * 60)
    print(title)
    print("=" * 60)
    print("Board:")
    print_board(board)
    print("Current player:", player(board))
    print()

    minimax_nodes = 0
    start_time = time.perf_counter()
    minimax_move, minimax_score = minimax(board)
    minimax_time = time.perf_counter() - start_time

    alphabeta_nodes = 0
    start_time = time.perf_counter()
    alphabeta_move, alphabeta_score = minimax_alphabeta(board)
    alphabeta_time = time.perf_counter() - start_time

    print_comparison_table(
        "Results",
        minimax_move, minimax_score, minimax_nodes, minimax_time,
        alphabeta_move, alphabeta_score, alphabeta_nodes, alphabeta_time
    )


def main():
    board1 = [
        [X, O, X],
        [O, X, EMPTY],
        [EMPTY, EMPTY, O]
    ]

    board2 = [
        [X, O, EMPTY],
        [EMPTY, X, EMPTY],
        [O, EMPTY, EMPTY]
    ]

    board3 = [
        [X, EMPTY, EMPTY],
        [EMPTY, O, EMPTY],
        [EMPTY, EMPTY, X]
    ]

    compare_algorithms(board1, title="Example 1")
    compare_algorithms(board2, title="Example 2")
    compare_algorithms(board3, title="Example 3")


if __name__ == "__main__":
    main()