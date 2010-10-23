import string, sys, random
from sys import argv
import boardstate

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

Flag options for reference's sake




"""

#game vars
board = [[],[],[],[],[],[]]
column_drops = []
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
    board_str = "\n  0 1 2 3 4 5 6\n-----------------\n"
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

#prompt user for input for a number of options ranging from 1 to total_choices
def prompt_input(prompt, total_choices):
    while True:
        try:
            choice = int(raw_input(prompt))
        except ValueError: #if users enter a non-integer
            print "Please enter a valid choice (1-%s)" % total_choices
            continue
            
        if not(choice < (total_choices + 1) and choice > 0):
            print "Please enter a valid choice (1-%s)" % total_choices
        else:
            return choice

#control the flow from the user's choice at the main menu
def process_main():
    choice = prompt_input(" > ", 5)
    print ""
    if choice == 1: #new game
        game_loop()
    elif choice == 2: #statistics
        draw_stats()
        draw_main()
        process_main()
    elif choice == 3: #settings
        #process_settings()
        draw_main()
        process_main()
    elif choice == 4: #help
        #draw_help()
        draw_main()
        process_main()
    elif choice == 5: #exit
        print "Good bye"
        sys.exit()
    else:
        print "We're not really quite sure what just happened"
        sys.exit()

#checks the current game board state for any winning sequences of four
#Example win: row_check = ['row', [0,0,"X"], [0,1,"X"], [0,2,"X"], [0,3,"X"]]
#returns empty list [] if no winner, returns ["Draw"] if draw
def check_win():
    row_check = col_check = diag_check = [] #lists of three-length lists
    empty_check = False #flag denoting True if any slots are empty
    
    #checking for win by row
    for i in range(0, len(board)):
        row_check = []
        for j in range(0,7):
            if board[i][j] == " ": #found at least one empty slot, see below
                empty_check = True
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
            
    #checking for win by diagonal (very sneaky, sis)
    for i in range(0, len(board)):
        for j in range(0,7):
            try: #try to go down and to the right
                if board[i][j] == board[i+1][j+1] and board[i][j] != " ":
                    flag = True
                    for a in range(2,4): #check if two more consecutively
                        if board[i][j] != board[i+a][j+a]:
                            flag = False
                            break
                    if flag: #got 4 consecutively, prepare our 
                        diag_check = []
                        for b in range(0,4):
                            diag_check.append([(i+b),(j+b),board[i][j]])
                        winner = ["diag", diag_check]
                        return winner
            except IndexError: #if we go beyond bounds of table
                 pass
            try: #try to go down and to the left
                if board[i][j] == board[i+1][j-1] and board[i][j] != " " and j>0:
                    flag = True
                    for a in range(2,4):
                        if board[i][j] != board[i+a][j-a] or j-a < 0:
                            flag = False
                            break
                    if flag:
                        diag_check = []
                        for b in range(0,4):
                            diag_check.append([(i+b),(j-b),board[i][j]])
                        winner = ["diag", diag_check]
                        return winner
            except IndexError:
                 continue         
    
    if empty_check:
        return [] #no winner returned yet, board not full, return empty list
    else:
        return ["Draw"] #no winner yet, board full, return "Draw" inside list
    
#process the results of the game and congratulate the winner
def process_result(winlist):
    global x_wins, o_wins, draws, games_played
    print winlist
    if len(winlist) == 1:
        draws += 1.0
        current = draws
        winner = "Draw"
    else:
        winner = winlist[1][0][2]
        print winner
        if winner == "X":
            x_wins += 1.0
            current = x_wins
        elif winner == "O":
            o_wins += 1.0
            current = o_wins
        else:
            print "We're not really quite sure what just happened!!"
            return
    
    games_played += 1.0
    draw_board()
    
    if winner == starting_player:
        player = "Player 1"
    else:
        player = "Player 2"
    if winner == "Draw":
        print "It's a draw! There have been %s draw(s) in this session!" % int(current)
    else:
        print "Congratulations %s! %s wins!" % (player, winner)
        print "%s has now won %s game(s) in this session!" % (winner, int(current))
        
        
    
#switches whose turn it is
def switch_turn():
    global active_player
    if active_player == "X":
        active_player = "O"
    elif active_player == "O":
        active_player = "X"
    
    
"""     ***************     GAME FUNCTIONS     ***************     """
    
#reset game variables for a new match
def reset_game():
    global board, active_player
    active_player = starting_player
    initialize_board()
    
#reset the game board to its initial state
def initialize_board():
    global board, column_drops
    for i in range(0, len(board)):
        board[i] = [" ", " ", " ", " ", " ", " ", " "]
    column_drops = [0,0,0,0,0,0,0]
    
#attempt to insert a piece into a column, returns true if successful
def insert_piece(column, piece):
    global board, column_drops
    if column_drops[column] < 6:
        column_drops[column] += 1
        board[6-column_drops[column]][column] = piece
        return True #successful insert, return true
    return False #never inserted, column must be full, return false
            
#control loop of an actual tic tac toe game
def game_loop():
    global active_player
    active_player = starting_player
    finished = False
    #takes care of processing for one full game
    while not(finished):
        draw_board()
        flag = False
        while not(flag):
            try:
                column = int(raw_input("Pick a column (0-6) or 7 to quit\n %s > " % active_player))
            except ValueError: #if users enter a non-integer
                print "Invalid input"
                continue
                
            if not(column < 8 and column > -1):
                    print "Invalid input"
            else:
                if column == 7: #chose 9 to quit
                    print "Quitting current game"
                    reset_game()
                    draw_main()
                    process_main()
                else: #chose a column (0-6)
                    if insert_piece(column, active_player):
                        flag = True
                    else:
                        print "Column is already filled to the top"
        #have a valid pick at this point
        winlist = check_win()
        if winlist == []:
            switch_turn()
        else:
            finished = True
            
    process_result(winlist)
    reset_game()
    draw_main()
    process_main()

    
    
"""     ***************     MAIN     ***************     """
       
if __name__ == "__main__":
    initialize_board()
    draw_main()
    process_main()
    
    
    
