"""
Tic Tac Toe Player
"""
import math
import copy

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


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Defining the return set
    return_set = set(()) 

    # Looping through all rows in the board
    for i_board in range(len(board)):
        
        # Looping through all places in each row
        for i_place in range(len(board[i_board])):
            # Checking if place is empty
            if board[i_board][i_place] == EMPTY:
                # Adding empty places to return set
                return_set.add((i_board, i_place))
    # Returning the empty places.
    return return_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Determining which player's turn it is
    turn = player(board)
    # Defining which row and column the action is referring to.
    row = action[0]
    column = action[1]

    # Creating a copy of the board
    new_board = copy.deepcopy(board)
    new_board[row][column] = turn

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.

    """

    # Checking horizontally
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == O:
                return O
            if board[i][0] == X:
                return X
    # Checking vertically    
    for v in range(3):
        if board[0][v] == board[1][v] == board[2][v]:
            if board[0][v] == O:
                return O
            if board[0][v] == X:
                return X
            
    # Checking diagonals
    
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        if board[0][0] == O:
            return O
    
    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == X:
            return X
        if board[0][2] == O:
            return O
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
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

    if total_x + total_o == 9:
        return True
    
    if winner(board) == None:
        return False
    else: 
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = 1
    lose = -1
    draw = 0
    
    if terminal(board) ==  True:
        
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0
    else:
        return 0



def find_final_state(board, action, start=True):
    global utility_list;
    global test;
    if start == True:
        utility_list = []
        test = 0
       
    new_board = result(board, action)
    

    if terminal(new_board):
        
        utility_list.append(utility(new_board))
        new_board = []
        
    else:
        for action_2 in actions(new_board):            
            find_final_state(new_board, action_2, start=False)
            if terminal(new_board):
                break
    
    return utility_list

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    best_action = tuple()
    action_set = set()
    
    turn = player(board)
    # Returning Nothing if the game is over.
    if terminal(board) == True:
        return None

    if turn == X:
        best_action = (None, float('-inf'))
        for action in actions(board):
            val = sum(find_final_state(board,action,start=True))
            if val > best_action[1]:
                best_action = (action, val)
                           
    elif turn == O: 
        best_action = (None, float('inf'))
        for action in actions(board):
            val = sum(find_final_state(board,action,start=True))
            if val < best_action[1]:
                best_action = (action, val)

    return best_action[0]
    



    
    
    

    
