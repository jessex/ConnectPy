from copy import deepcopy
from checkwin import check_win

class BoardState:
       
    def __init__(self):
        self.board = []
        for i in range(6):
            row = []
            for j in range(7):
                row.append(" ")
            self.board.append(row)
            
    #returns a unique copy of the board
    def copy_board(self):
        copy = BoardState()
        copy.board = deepcopy(self.board)
        return copy
        
    #adds a player's piece to a column, if possible
    def make_move(self, column, player):
        if column < 0 or column > 6:
            print "Error: invalid column"
            return False
        if not (player == "X" or player == "O"):
            print "Error: invalid player"
            return False
        for i in range(5, -1, -1):
            if self.board[i][column] == " ":
                self.board[i][column] = player
                return True
        return False
        
    #determines if the board is full
    def board_full(self):
        for row in self.board:
            for col in row:
                if col == " ":
                    return False
        return True
        
    #determines the current finishing state of the board
    def board_win(self):
        winner = check_win(self.board)
        if winner == []: #Empty list means not finished
            return 0
        elif winner[0] == "Draw": #Draw
            return 0
        elif winner[1][2] == "X": #"X" wins (AI)
            return 1
        else: #"O" wins (human)
            return -1
        

        
        
        
