import math
from sys import maxint

cutoff_depth = 3
first_depth = 0
value_weights = (1, 5, 100, 10000, 2, 6, 200, 15000)
MIN_INT = -maxint - 1
MAX_INT = maxint


def get_successors(state):
    successors = {}
    for i in range(0, 7):
        successor_state = state.make_move(i,state)
        if successor_state != None: #drop in column i was valid
            successors[i] = successor_state
    return successors
    
    
def should_cutoff(state):
    state.state_value = heuristic_score(state.board)
    if abs(state.state_value) > 5000: #either computer or human has win
        return True
    if (state.move_count - first_depth) > cutoff_depth:
        return True
    return False
    
def generate_move(state):
    global first_depth
    state.successors = get_successors(state)
    first_depth = state.move_count
    best_score = max_score(state, MIN_INT, MAX_INT)
    
    for i in state.successors:
        if state.successors[i].state_value == best_score:
            return i
    return -1
    
    

def max_score(state, alpha, beta):
    if should_cutoff(state): #have a winning state or reached max search depth
        return state.state_value
        
    state.state_value = MIN_INT
    if len(state.successors) > 0:
        successors = state.successors
    else:
        successors = get_successors(state)
    
    for i in successors:
        state.state_value = max(state.state_value, min_score(successors[i], alpha, beta))
        if state.state_value >= beta:
            return state.state_value
        alpha = max(alpha, state.state_value)
    
    return state.state_value
    
def min_score(state, alpha, beta):
    if should_cutoff(state):
        return heuristic_score(state.board)
    
    state.state_value = MAX_INT
    if len(state.successors) > 0:
        successors = state.successors
    else:
        successors = get_successors(state)
        
    for i in successors:
        state.state_value = min(state.state_value, max_score(successors[i], alpha, beta))
        if state.state_value <= alpha:
            return state.state_value
        beta = min(beta, state.state_value)
    
    return state.state_value

def check_possibilities(pieces):
    score = 0
    
    for i in range(0, (len(pieces)-3)):
        computer = 0
        human = 0
        
        #count nearby computer and human pieces
        for j in range(0,4):
            if pieces[i+j] == "X":
                computer += 1
            elif pieces[i+j] == "O":
                human += 1
        
        if (computer > 0) and (human == 0):
            if computer == 4: #computer has a winning situation
                return value_weights[3]
            #award scpre for nearby computer pieces
            score += ((computer/3) * value_weights[2]) + ((computer/2) * value_weights[1]) + value_weights[0]
        elif (human > 0) and (computer == 0):
            if human == 4: #human has a winning situation
                return (value_weights[7] * -1)
            #penalize score for nearby human pieces
            score -= ((human/3) * value_weights[6]) + ((human/2) * value_weights[5]) + value_weights[4]
            
    return score
                

def heuristic_score(board):
    score = 0
    
    for i in range(0,6): #Check each row
        pieces = [board[i][0], board[i][1], board[i][2], board[i][3], board[i][4], board[i][5], board[i][6]]
        score += check_possibilities(pieces)
    
    for i in range(0,7): #Check each column
        pieces = [board[0][i], board[1][i], board[2][i], board[3][i], board[4][i], board[5][i]]
        score += check_possibilities(pieces)
    
    #Check all diagonal combinations (hardcoded, yes, but it works)
    #Left to right diagonals
    score += check_possibilities([board[2][0], board[3][1], board[4][2], board[5][3]])
    score += check_possibilities([board[1][0], board[2][1], board[3][2], board[4][3], board[5][4]])
    score += check_possibilities([board[0][0], board[1][1], board[2][2], board[3][3], board[4][4], board[5][5]])
    score += check_possibilities([board[0][1], board[1][2], board[2][3], board[3][4], board[4][5], board[5][6]])
    score += check_possibilities([board[0][2], board[1][3], board[2][4], board[3][5], board[4][6]])
    score += check_possibilities([board[0][3], board[1][4], board[2][5], board[3][6]])
    #Right to left diagonals
    score += check_possibilities([board[0][3], board[1][2], board[2][1], board[3][0]])
    score += check_possibilities([board[0][4], board[1][3], board[2][2], board[3][1], board[4][0]])
    score += check_possibilities([board[0][5], board[1][4], board[2][3], board[3][2], board[4][1], board[5][0]])
    score += check_possibilities([board[0][6], board[1][5], board[2][3], board[3][3], board[4][2], board[5][1]])
    score += check_possibilities([board[1][6], board[2][5], board[3][4], board[4][3], board[5][2]])
    score += check_possibilities([board[2][6], board[3][5], board[4][4], board[5][3]])
    
    return score
    
    
    



