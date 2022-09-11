"""
Tic Tac Toe Player
"""

import math
from tqdm import tqdm
import copy
import numpy as np
import random

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
    counter = 0
    for row in board:
        for i in row:
            if i != EMPTY:
                counter += 1
    if counter % 2 == 0:
        return X
    elif counter < 9:
        return O
    return None


def get_optimal_action(board, win, play):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    for r in range(0,3):
        for c in range(0,3):
            if board[r][c] == EMPTY:
                if win[r][c] == play:
                    return play, r, c

def board_equal(board1, board2):
    t = 0
    for r in range(3):
        for c in range(3):
            if board1[r][c] == board2[r][c]:
                t+=1
    if t == 9:
        return True
    return False

def result(node, player, i, j):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    children = node.children()
    for child in children:
        if child.board[i][j] == player:
            return child

def check_list(list):
    if list[0] == X and list[1] == X and list[2] == X:
        return X
    if list[0] == O and list[1] == O and list[2] == O:
        return O
    return None

def winner(board):
    # rows
    for row in board:
        result = check_list(row)
        if result is not None:
            return result

    # columns
    for i in range(3):
        result = check_list([board[0][i], board[1][i], board[2][i]])
        if result is not None:
            return result

    # diagonals
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    c = 0
    w = winner(board)
    if w is not None:
        return True
    else:
        for i in board:
            for j in i:
                if j == X or j == O:
                    c += 1
        if c == 9:
            return True
        return False

def get_diff(board1, board2):
    for r in range(0,3):
        for c in range(0,3):
            if board1[r][c] != board2[r][c]:
                return r,c


def dfs(node):
    """
    Returns the optimal action for the current player on the board.
    """
    play = player(node.board)
    s = Stack()
    s.push(node)
    while not s.is_empty():
        if winner(s.peek().board) == play:
            return get_optimal_action(node.board, s.peek().board, play)
        current = s.pop()
        for r in current.c:
            s.push(r)
    optimal_node = random.choice(node.c)
    i, j = get_diff(node.board, optimal_node.board)
    return play, i, j

class Stack:
    def __init__(self):
        self.stack = []  # start off with an empty list as our stack

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        if len(self.stack) == 0:
            return None
        else:
            return self.stack.pop()

    def peek(self):
        if len(self.stack) == 0:
            return None
        else:
            return self.stack[-1]

    def size(self):
        return len(self.stack)

    def is_empty(self):
        if len(self.stack) == 0:
            return True
        return False


class Node:
    def __init__(self, board):
        self.board = board
        self.c = []

    # Return value of node
    def value(self):
        return self.board

    # Return the array of children
    def children(self):
        return self.c

    # The method below takes in an array of children
    # and it extends the current children array, which is self.c,
    # using Python's extend() method.
    def add_children(self, children):
        self.c.extend(children)


# Tic Tac Toe tree

def get_children(state, value):
    c = []
    for i in range(3):
        for j in range(3):
            if state[i][j] is None:
                state2 = copy.deepcopy(state)
                state2[i][j] = value
                c.append(state2)
    return c

def get_tree():
    root = Node(initial_state())
    children = [Node(child) for child in get_children(root.board, X)]
    prev_val = X
    root.add_children(children)

    while (len(children) != 0):
        if prev_val == X:
            val = O
        else:
            val = X
        children3 = []
        for node in tqdm(children):
            children2 = [Node(child) for child in get_children(node.board, val)]
            node.add_children(children2)
            children3.extend(children2)
        prev_val = val
        children = children3
    return root

