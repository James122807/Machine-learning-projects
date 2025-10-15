"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)
    return "X" if x_count == o_count else "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is None}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    import copy
    i, j = action

    if not (0 <= i < 3 and 0 <= j < 3):
        raise Exception("Invalid move: out of bounds")

    if board[i][j] is not None:
        raise Exception("Invalid move!")

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] and row.count(row[0]) == 3:
            return row[0]
    for j in range(3):
        column = [board[i][j] for i in range(3)]
        if column[0] and column.count(column[0]) == 3:
            return column[0]
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    return all(cell is not None for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == "X":
        return 1
    elif win == "Y":
        return -1
    return 0


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float("-inf")
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float("inf")
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    turn = player(board)

    if turn == X:
        best_score = float("-inf")
        best_action = None
        for action in actions(board):
            score = min_value(result(board, action), float("-inf"), float("inf"))
            if score > best_score:
                best_score = score
                best_action = action
        return best_action

    else:  # O's turn
        best_score = float("inf")
        best_action = None
        for action in actions(board):
            score = max_value(result(board, action), float("-inf"), float("inf"))
            if score < best_score:
                best_score = score
                best_action = action
        return best_action

