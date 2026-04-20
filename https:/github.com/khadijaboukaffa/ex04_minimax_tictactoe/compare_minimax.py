import time

X = "X"
O = "O"
EMPTY = None


# Compteurs globaux
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
    Retourne le joueur qui doit jouer maintenant.
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
    Retourne la liste des coups possibles.
    """
    moves = []

    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                moves.append((i, j))

    return moves


def result(board, action):
    """
    Retourne un nouveau plateau après avoir joué un coup.
    """
    i, j = action

    if board[i][j] is not EMPTY:
        raise ValueError("Invalid move: cell already occupied")

    new_board = [row.copy() for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Retourne X ou O s'il y a un gagnant, sinon None.
    """
    # Lignes
    for row in board:
        if row[0] is not None and row[0] == row[1] == row[2]:
            return row[0]

    # Colonnes
    for col in range(3):
        if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]

    # Diagonale principale
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    # Diagonale secondaire
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
    Retourne le score final :
    X gagne  ->  1
    O gagne  -> -1
    égalité  ->  0
    """
    game_winner = winner(board)

    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


# =========================================================
# MINIMAX NORMAL
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
# MINIMAX + ALPHA-BETA
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
# COMPARAISON
# =========================================================

def compare_algorithms(board):
    global minimax_nodes, alphabeta_nodes

    print("Current board:")
    print_board(board)
    print("Current player:", player(board))
    print()

    # --- Minimax normal ---
    minimax_nodes = 0
    start_time = time.perf_counter()
    minimax_move, minimax_score = minimax(board)
    minimax_time = time.perf_counter() - start_time

    # --- Alpha-Beta ---
    alphabeta_nodes = 0
    start_time = time.perf_counter()
    alphabeta_move, alphabeta_score = minimax_alphabeta(board)
    alphabeta_time = time.perf_counter() - start_time

    print("=== Comparison ===")
    print(f"Minimax best move       : {minimax_move}")
    print(f"Minimax best score      : {minimax_score}")
    print(f"Minimax nodes evaluated : {minimax_nodes}")
    print(f"Minimax time            : {minimax_time:.6f} seconds")
    print()

    print(f"Alpha-Beta best move       : {alphabeta_move}")
    print(f"Alpha-Beta best score      : {alphabeta_score}")
    print(f"Alpha-Beta nodes evaluated : {alphabeta_nodes}")
    print(f"Alpha-Beta time            : {alphabeta_time:.6f} seconds")
    print()

    print("Same move?", minimax_move == alphabeta_move)
    print("Same score?", minimax_score == alphabeta_score)


def main():
    # Exemple 1 : position intermédiaire
    board = [
        [X, O, X],
        [O, X, EMPTY],
        [EMPTY, EMPTY, O]
    ]

    compare_algorithms(board)

    print("\n" + "=" * 50 + "\n")

    # Exemple 2 : position un peu plus ouverte
    board2 = [
        [X, O, EMPTY],
        [EMPTY, X, EMPTY],
        [O, EMPTY, EMPTY]
    ]

    compare_algorithms(board2)


if __name__ == "__main__":
    main()