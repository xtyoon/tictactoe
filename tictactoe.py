import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY] * 3 for _ in range(3)]


def player(board):
    x_count = sum(cell == X for row in board for cell in row)
    o_count = sum(cell == O for row in board for cell in row)
    return O if x_count > o_count else X


def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    # Check rows, columns, and diagonals for a winner
    lines = (
            board +  # Rows
            [[board[i][j] for i in range(3)] for j in range(3)] +  # Columns
            [[board[i][i] for i in range(3)], [board[i][2 - i] for i in range(3)]]  # Diagonals
    )

    for line in lines:
        if all(cell == line[0] and cell is not EMPTY for cell in line):
            return line[0]
    return None


def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
    return 0


def minimax(board):
    if terminal(board):
        return None
    return max_value(board)[1] if player(board) == X else min_value(board)[1]


def max_value(board):
    if terminal(board):
        return utility(board), None

    v, move = float('-inf'), None
    for action in actions(board):
        aux = min_value(result(board, action))[0]
        if aux > v:
            v, move = aux, action
            if v == 1:
                break  # Pruning
    return v, move


def min_value(board):
    if terminal(board):
        return utility(board), None

    v, move = float('inf'), None
    for action in actions(board):
        aux = max_value(result(board, action))[0]
        if aux < v:
            v, move = aux, action
            if v == -1:
                break  # Pruning
    return v, move
