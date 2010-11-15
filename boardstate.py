from copy import deepcopy

class BoardState:
    """ An object containing information for a hypothetical board state. """
       
    def __init__(self, *args, **kwargs):
        """ If one argument is passed in, it should be an old BoardState. 
            Otherwise, no arguments should be passed in and a new BoardState
            will be created. """
        if len(args) == 0:
            self.init_new()
        elif len(args) == 1 and isinstance(args[0], BoardState):
            self.init_from_old(args[0])
            
    def init_new(self):
        """ Constructs a new BoardState with empty data. """
        self.board = [[],[],[],[],[],[]] #current board state
        for i in range(0, len(self.board)): #initialize board
            self.board[i] = [" ", " ", " ", " ", " ", " ", " "]
        self.move_count = 0     #amount of moves made since start of state
        self.column_drops = [0,0,0,0,0,0,0] #amount of dropped pieces per column
        self.active_player = "" #player whose turn it is
        self.successors = {} #dictionary of possible successor states
    
    def init_from_old(self, old_board):
        """ Constructs a new BoardState based upon an older BoardState. """
        self.board = old_board.board
        self.move_count = old_board.move_count
        self.column_drops = old_board.column_drops
        self.active_player = old_board.active_player
        self.successors = {}
        
      
    def make_move(self, column, board_state):
        """ Makes the passed column move on the passed board state and
            returns the new BoardState, with the old BoardState unaltered. """
        new_state = deepcopy(board_state) #deep copy of pre-move BoardState
        
        if new_state.column_drops[column] == 6: #column is full, cannot move
            return None
        new_state.column_drops[column] += 1
        new_state.board[6-new_state.column_drops[column]][column] = new_state.active_player
        new_state.move_count += 1
        if (new_state.active_player == "X"):
            new_state.active_player = "O"
        else:
            new_state.active_player = "X"
            
        return new_state
        

        
        
        
