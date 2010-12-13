import boardstate

#evaluate all possible moves for a given board state
def evaluate(board, depth):
    if board.board_win() != 0 or board.board_full():
        return board.board_win() * 10000 * (25-depth)
    value = 0
    
    #three pieces in succession
    for i in range(0,4):
        for j in range(0,7):
            if board.board[i][j] == board.board[i+1][j] == board.board[i+2][j] and board.board[i][j] != ' ':
                if board.board[i][j] == "X":
                    value += .2
                else:
                    value -= .2
    for i in range(0,6):
        for j in range(0,5):
            if board.board[i][j] == board.board[i][j+1] == board.board[i][j+2] and board.board[i][j] != ' ':
                if board.board[i][j] == "X":
                    value += .2
                else:
                    value -= .2
    for i in range(0,4):
        for j in range(0,5):
            if board.board[i][j] == board.board[i+1][j+1] == board.board[i+2][j+2] and board.board[i][j] != ' ':
                if board.board[i][j] == "X":
                    value += .2
                else:
                    value -= .2
    for i in range(2,6):
        for j in range(0,5):
            if board.board[i][j] == board.board[i-1][j+1] == board.board[i-2][j+2] and board.board[i][j] != ' ':
                if board.board[i][j] == "X":
                    value += .2
                else:
                    value -= .2

    #two pieces in succession
    for i in range(0,5):
        for j in range(0,7):
            if board.board[i][j] == board.board[i+1][j] and board.board[i][j] != ' ':
                if board.board[i][j] == "X":
                    value += .05
                else:
                    value -= .05
    for i in range(0,6):
        for j in range(0,6):
            if board.board[i][j] == board.board[i][j+1] and board.board[i][j] != ' ':
                if board.board[i][j] == "X":
                    value += .05
                else:
                    value -= .05
    for i in range(0,5):
        for j in range(0,6):
            if board.board[i][j] == board.board[i+1][j+1] and board.board[i][j] != ' ':
                if board.board[i][j] == "X":
                    value += .05
                else:
                    value -= .05
    for i in range(0,5):
        for j in range(1,7):
            if board.board[i][j] == board.board[i+1][j-1] and board.board[i][j] != ' ':
                if board.board[i][j] == "X":
                    value += .05
                else:
                    value -= .05
    return value
    
#recursive alpha-beta pruner to generate the optimal move at a given state
def generate_move(board, depth, diff, alpha, beta, column, AI):
    #terminal condition has been met
    if board.board_win() != 0 or board.board_full() or depth == diff:
        return (evaluate(board, depth), -1, -1)
    else:
        if AI == True:
            score = float("-inf")
        else:
            score = float("inf")
        best = next = 0
        order = search_order(column)
        for i in order:
            if board.board[0][i] != " ": #skip empty
                continue
            temp = board.copy_board()
            if AI == True: #simulate human's next turn
                temp.make_move(i, "X")
                (value, c, nm) = generate_move(temp, depth+1, diff, alpha, beta, i, False)
                if value >= beta and depth != 0:
                    return (value, best, c)
                if value > score: #bested our previous score, adjust accordingly
                    score = value
                    best = i
                    next = c
                    alpha = score
            else: #simulate AI's next turn
                temp.make_move(i, "O")
                (value, c, nm) = generate_move(temp, depth+1, diff, alpha, beta, i, True)
                if value <= alpha and depth != 0:
                    return (value, best, c)
                if value < score: #bested our previous score, adjust accordingly
                    score = value
                    best = i
                    next = nm
                    beta = score
                
        return (score, best, next)  

#determine the column search order given a particular column drop
def search_order(col):
        if col == 0:
                return [0,1,2,3,4,5,6]
        elif col == 1:
                return [1,0,2,3,4,5,6]
        elif col == 2:
                return [2,1,3,0,4,5,6]
        elif col == 3:
                return [3,2,4,1,5,0,6]
        elif col == 4:
                return [4,3,5,2,6,1,0]
        elif col == 5:
                return [5,4,6,3,2,1,0]
        elif col == 6:
                return [6,5,4,3,2,1,0]
			
        return [3,2,4,1,5,0,6]


