import string, sys, random
from sys import argv

"""
Game board for reference's sake (7x6 dimensions)
  0 1 2 3 4 5 6
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
starting_player = "O"
active_player = "O"
comp_player = "X"

#session vars
games_played = 0.0
x_wins = o_wins = draws = 0.0




"""     ***************     DRAWING FUNCTIONS     ***************     """

#draws the main menu and prompts user for input
def draw_main():
    menu = "\n=====ConnectPy=====\n"
    menu += " 1. New game\n"
    menu += " 2. Statistics\n"
    menu += " 3. Settings\n"
    menu += " 4. Help\n"
    menu += " 5. Exit\n"
    print menu

#draw the game board
def draw_board():
    board_str = "  0 1 2 3 4 5 6\n-----------------\n"
    for i in range (0, len(board)):
        board_str += "| "
        for j in range(0,7):
            board_str += board[i][j] + " "
        board_str += "|\n"
    board_str += "-----------------"
    print board_str
    
#calculate and print the game results for the current session
def draw_stats():
    global x_wins, o_wins_draws
    if games_played == 0.0:
       print "No games have been completed in this session"
       return
    x_per = '%.2f' % ((x_wins / games_played) * 100)
    o_per = '%.2f' % ((o_wins / games_played) * 100)
    d_per = '%.2f' % ((draws / games_played) * 100)
    res = "=====Session Statistics=====\n"
    res += "Games: %s\n" % int(games_played)
    res += "X wins: %s , %s%%\n" % (int(x_wins), x_per)
    res += "O wins: %s , %s%%\n" % (int(o_wins), o_per)
    res += "Draws: %s , %s%%" % (int(draws), d_per)
    print res
    

"""     ***************     PROCESSING FUNCTIONS     ***************     """

def check_win():
    row_check = col_check = diag_check = [] #lists of three-length lists
    #Example win: row_check = [[0,0,"X"], [0,1,"X"], [0,2,"X"], [0,3,"X"]]
    
    #checking for win by row
    for i in range(0, len(board)):
        row_check = []
        for j in range(0,7):
            if j > 0: 
                if board[i][j] == board[i][j-1] and board[i][j] != " ":
                    prev = [i,j-1, board[i][j]]
                    curr = [i,j, board[i][j]]
                    #place them both into row_check
                    if not(prev in row_check):
                        row_check.append(prev)
                    row_check.append(curr)
                    #if we now have at least 4 in row_check, it's a winner
                    if len(row_check) > 3:
                        winner = ["row", row_check]
                        return winner
                else: #current row_check is broken, start it over
                    row_check = []
    #checking for win by column   
    for j in range(0,7):
        col_check = []
        for i in range(0, len(board)):
            if i > 0:
                if board[i-1][j] == board[i][j] and board [i][j] != " ":
                    prev = [i-1,j, board[i][j]]
                    curr = [i,j, board[i][j]]
                    if not(prev in col_check):
                        col_check.append(prev)
                    col_check.append(curr)
                    if len(col_check) > 3:
                        winner = ["col", col_check]
                        return winner
                else:
                    prev = [i-1,j, "O"]
                    if prev in col_check: #prev was in col_check but not this
                        col_check = []
                    prev = [i-1,j, "X"]
                    if prev in col_check:
                        col_check = []
            
            
          
    return [] #no winner returned yet, return empty list
    
    
"""     ***************     GAME FUNCTIONS     ***************     """
    
#reset the game board to its initial state
def initialize_board():
    global board
    for i in range(0, len(board)):
        board[i] = [" ", " ", " ", " ", " ", " ", " "]
    
#attempt to insert a piece into a column, returns true if successful
def insert_piece(column, piece):
    global board
    for i in range (0, len(board)):
        if board[5-i][column] == " ":
            board[5-i][column] = piece
            return True #successful insert, return true
    return False #never inserted, column must be full, return false
            
    
    
    
    
    
"""     ***************     MAIN     ***************     """
       
if __name__ == "__main__":
    initialize_board()
    flag = True
    while (flag):
        if active_player == "X":
            active_player = "O"
        else:
            active_player = "X" 
        draw_board()
        insert_piece((int(raw_input(" > "))), active_player)
        winner = check_win()
        if winner != []:
            flag = False
    print winner
        
    
    
