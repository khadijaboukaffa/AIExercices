X = "X"
O = "O"
EMPTY = None


def print_board(board):
    print()
    for i, row in enumerate(board):
        display_row = []
        for j, cell in enumerate(row):
            if cell is None:
                display_row.append(f"{i},{j}")
            else:
                display_row.append(cell)
        print(" | ".join(display_row))
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


def get_human_move(board):
    while True:
        try:
            row = int(input("Row (0, 1, 2): "))
            col = int(input("Col (0, 1, 2): "))
            move = (row, col)

            if move not in actions(board):
                print("Invalid move. Try again.")
                continue

            return move
        except ValueError:
            print("Please enter numbers only.")


def main():
    board = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]

    human = input("Choose your side (X/O): ").strip().upper()
    if human not in [X, O]:
        human = X

    ai = O if human == X else X

    print(f"You are {human}. AI is {ai}.")

    while not terminal(board):
        print_board(board)
        current = player(board)

        if current == human:
            print("Your turn.")
            move = get_human_move(board)
            board = result(board, move)
        else:
            print("AI is thinking...")
            move = minimax(board)
            print("AI chooses:", move)
            board = result(board, move)

    print_board(board)

    game_winner = winner(board)
    if game_winner is None:
        print("Draw!")
    elif game_winner == human:
        print("You win!")
    else:
        print("AI wins!")


if __name__ == "__main__":
    main()