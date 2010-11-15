import string, sys, random
from sys import argv
from copy import deepcopy
import boardstate, checkwin, aimodule

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
board = [[],[],[],[],[],[]]                 #current game board
column_drops = []                           #amount of pieces per column
current_state = boardstate.BoardState()     #current board/game state
starting_player = "O"                       #starting player, default is "O"
active_player = "O"                         #current player whose turn it is
comp_player = "X"                           #computer player, always "X"
game_type = 2                               #amount of players, default is 2

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

#process the command line argmuents
def process_args(args):
    global game_type, starting_player
    del args[0] #remove the script name (connectfour.py)
    
    #iterate through command line arguments
    for i in range(0,len(args)):
        if args[i] == "--help": #help command
            draw_help()
            sys.exit()
        elif args[i] == "-p": #game type command
            if int(args[i+1]) == 1 or int(args[i+1]) == 2: 
                game_type = int(args[i+1])
            else:
                print "Command '-p' must be followed by 1 or 2"
        elif args[i] == "-f": #starting player command
            if args[i+1] == "X" or args[i+1] == "x":
                starting_player = "X"
            elif args[i+1] == "O" or args[i+1] == "o":
                starting_player = "O"
            else:
                print "Command '-f' must be followed by X or O"

#prints the settings menu and controls changes made herein
def process_settings():
    global game_type, starting_player
    print """
    Choose a selection:
    
    1. Player Count         [Currently %s]
    2. Starting Player      [Currently %s]
    3. Return to main menu
    """ % (game_type, starting_player)
    choice = prompt_input(" > ", 3)
    if choice == 1:
        game_type = prompt_input("Player total: ", 2)
    elif choice == 2:
        valid = False
        while valid == False:
            player = raw_input("Starting player: ")
            if player == "X" or player == "x":
                starting_player = "X"
                valid = True
            elif player == "O" or player == "o":
                starting_player = "O"
                valid = True
            else:
                print "Please enter a valid choice (X or O)"

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
        process_settings()
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
    global board, column_drops, current_state
    for i in range(0, len(board)):
        board[i] = [" ", " ", " ", " ", " ", " ", " "]
    column_drops = [0,0,0,0,0,0,0]
    current_state = boardstate.BoardState()
    current_state.active_player = starting_player
    
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
    global active_player, current_state
    active_player = starting_player
    finished = False
    #takes care of processing for one full game
    while not(finished):
        draw_board()
        flag = False
        #if Human v Comp and it's comp's turn
        if game_type == 1 and active_player == comp_player:
            print "Computer is thinking..."
            column = aimodule.generate_move(current_state)
            if column == -1:
                print "Computer doesn't know where to go!"
            else:
                print "Computer moves to column %s" % column
                insert_piece(column, active_player)
                new_state = current_state.make_move(column, current_state)
                current_state = deepcopy(new_state)
        else:
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
                            new_state = current_state.make_move(column, current_state)
                            current_state = deepcopy(new_state)
                        else:
                            print "Column is already filled to the top"
        #have a valid pick at this point
        winlist = checkwin.check_win(board)
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
    
    
    
