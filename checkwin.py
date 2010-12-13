def check_win(board):
    """ Checks the current game board state for any winning sequences of four.
        Win ex: row_check = ['row', [[0,0,"X"], [0,1,"X"], [0,2,"X"], [0,3,"X"]]].
        Returns empty list [] if no winner, returns ["Draw"] if draw. """
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
        
