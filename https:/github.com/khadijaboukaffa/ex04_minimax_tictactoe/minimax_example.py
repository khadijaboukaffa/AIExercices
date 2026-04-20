X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]


def print_board(board):
    for row in board:
        display_row = []
        for cell in row:
            if cell is None:
                display_row.append("_")
            else:
                display_row.append(cell)
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

    if x_count <= o_count:
        return X
    else:
        return O


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
        raise ValueError("Invalid action: cell already occupied")

    new_board = []
    for row in board:
        new_board.append(row.copy())

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
    elif game_winner == O:
        return -1
    else:
        return 0


def max_value(board):
    if terminal(board):
        return utility(board)

    v = float("-inf")

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = float("inf")

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def minimax(board):
    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        best_score = float("-inf")
        best_action = None

        for action in actions(board):
            score = min_value(result(board, action))
            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    else:
        best_score = float("inf")
        best_action = None

        for action in actions(board):
            score = max_value(result(board, action))
            if score < best_score:
                best_score = score
                best_action = action

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
    print("Possible actions:", actions(board))
    print("Winner:", winner(board))
    print("Terminal:", terminal(board))

    best_move = minimax(board)
    print("Best move according to Minimax:", best_move)

    new_board = result(board, best_move)
    print("Board after best move:")
    print_board(new_board)


if __name__ == "__main__":
    main()