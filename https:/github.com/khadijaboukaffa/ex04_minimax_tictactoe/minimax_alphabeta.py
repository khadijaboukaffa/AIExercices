X = "X"
O = "O"
EMPTY = None

nodes_evaluated = 0


def print_board(board):
    for row in board:
        display_row = []
        for cell in row:
            display_row.append(cell if cell is not None else "_")
        print(" ".join(display_row))
    print()


def player(board):
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
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                moves.append((i, j))
    return moves


def result(board, action):
    i, j = action

    if board[i][j] is not EMPTY:
        raise ValueError("Cell already occupied")

    new_board = [row.copy() for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
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
    if winner(board) is not None:
        return True

    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False

    return True


def utility(board):
    game_winner = winner(board)
    if game_winner == X:
        return 1
    if game_winner == O:
        return -1
    return 0


def max_value(board, alpha, beta):
    global nodes_evaluated
    nodes_evaluated += 1

    if terminal(board):
        return utility(board)

    v = float("-inf")

    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)

        if alpha >= beta:
            break

    return v


def min_value(board, alpha, beta):
    global nodes_evaluated
    nodes_evaluated += 1

    if terminal(board):
        return utility(board)

    v = float("inf")

    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)

        if alpha >= beta:
            break

    return v


def minimax_alpha_beta(board):
    global nodes_evaluated
    nodes_evaluated = 0

    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        best_score = float("-inf")
        best_action = None
        alpha = float("-inf")
        beta = float("inf")

        for action in actions(board):
            score = min_value(result(board, action), alpha, beta)
            print(f"Action {action} -> score {score}")

            if score > best_score:
                best_score = score
                best_action = action

            alpha = max(alpha, best_score)

        return best_action

    else:
        best_score = float("inf")
        best_action = None
        alpha = float("-inf")
        beta = float("inf")

        for action in actions(board):
            score = max_value(result(board, action), alpha, beta)
            print(f"Action {action} -> score {score}")

            if score < best_score:
                best_score = score
                best_action = action

            beta = min(beta, best_score)

        return best_action


def main():
    board = [
        [X, O, X],
        [O, X, EMPTY],
        [EMPTY, EMPTY, O]
    ]

    print("Current board:")
    print_board(board)

    print("Current player:", player(board))
    print()

    best_move = minimax_alpha_beta(board)
    print()
    print("Best move with alpha-beta:", best_move)
    print("Nodes evaluated:", nodes_evaluated)

    new_board = result(board, best_move)
    print("Board after move:")
    print_board(new_board)


if __name__ == "__main__":
    main()