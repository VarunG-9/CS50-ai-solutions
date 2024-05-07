from tictactoe import *

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # If board has nothing on it, return X as X goes first
    if board == initial_state():
        return "X"
    
    # Defining the total X and O variables
    total_x = 0
    total_o = 0

    # Counting the number of X's and O's and adding them to the variable
    for list in board:
        for place in list:
            if place == "X":
                total_x +=1
            if place == "O":
                total_o +=1
    
    # Using logic to determine whose turn it is: if there are more X's then O's, it's O's turn. Otherwise, it's X's turn.
    if total_x > total_o:
        return "O"
    elif total_x == total_o:
        return "X"
b1 = [['X', 'O', 'O'], ['O', 'X', 'X'], [None, 'O', 'O']]

print(player(b1))
