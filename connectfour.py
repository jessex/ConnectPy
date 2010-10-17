import string, sys, random
from sys import argv

"""
Game board for reference's sake (7x6 dimensions)
-----------------
|               |
|               |
|               |
|               |
|               |
|               |
-----------------
"""

#game vars
board = [[],[],[],[],[],[]]

#session vars
games_played = 0.0
x_wins = o_wins = draws = 0.0

#reset the game board to its initial state
def initialize_board():
    global board
    for i in range(0, len(board)):
        board[i] = [" ", " ", " ", " ", " ", " ", " "]

#draw the game board
def draw_board():
    board_str = "-----------------\n"
    for i in range (0, len(board)):
        board_str += "| "
        for j in range(0,7):
            board_str += board[i][j] + " "
        board_str += "|\n"
    board_str += "-----------------"
    print board_str
    
    
    
    
    
    
"""     ***************     MAIN     ***************     """
       
if __name__ == "__main__":
    initialize_board()
    draw_board()
    
    
