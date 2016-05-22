import copy
import sys

board = []
positions = [[]]
player = ''
depth = 0
cutoff = 0
''' arg for battle simulation '''
player1 = ''
player2 = ''
cutoff1 = 0
cutoff2 = 0
depth1 = 0
depth2 = 0
task1 = 0
task2 = 0
'''read command'''
assert sys.argv[1] == "-i"
filename = sys.argv[2]

f = open(filename)

task = int(f.readline().strip())
if task != 4:
    player = f.readline().strip()
    cutoff = int(f.readline().strip())
    depth = cutoff
    
if task == 4:
    player1 = f.readline().strip()
    task1 = int(f.readline().strip())
    cutoff1 = int(f.readline().strip())
    depth1 = cutoff1
    player2 = f.readline().strip()
    task2 = int(f.readline().strip())
    cutoff2 = int(f.readline().strip()) 
    depth2 = cutoff2

for i in range(5):
    c = f.readline().strip().split(' ')
    board.append(c)

readpos = f.read()
itsline = readpos.split()
line0 = list(itsline[0])
line1 = list(itsline[1])
line2 = list(itsline[2])
line3 = list(itsline[3])
line4 = list(itsline[4])

positions = [line0,line1,line2,line3,line4]


f.close()
coordinates =  {(0,0): 'A1', (0,1): 'B1', (0,2): 'C1', (0,3): 'D1', (0,4): 'E1', 
                (1,0): 'A2', (1,1): 'B2', (1,2): 'C2', (1,3): 'D2', (1,4): 'E2',
                (2,0): 'A3', (2,1): 'B3', (2,2): 'C3', (2,3): 'D3', (2,4): 'E3',
                (3,0): 'A4', (3,1): 'B4', (3,2): 'C4', (3,3): 'D4', (3,4): 'E4',
                (4,0): 'A5', (4,1): 'B5', (4,2): 'C5', (4,3): 'D5', (4,4): 'E5'}

opponent = ''
if task != 4:
    def getOpp(player):
        if player == 'X':
            opponent = 'O'
        if player == 'O':
            opponent = 'X'
        return opponent
    opponent = getOpp(player)

def boardIsFull(positions):
    isFull = True
    for i in range(5):
        for j in range(5):
            if positions[i][j] == '*':
                isFull = False
    return isFull

def getBoardNums(board):
    for i in range(5):  #convert str to int
        for j in range(5):
            board[i][j] = int(board[i][j])
    return board

def getVal(positions,board,player):
    val = 0
    board = getBoardNums(board)
    for i in range(5):  #def curValue
        for j in range(5):
            if positions[i][j] == player:
                val += board[i][j]
            elif positions[i][j] == '*':
                continue
            else:
                val -= board[i][j]
    return val

poscopy = copy.deepcopy(positions)

def getNextState(poscopy, positions, i, j, player):
    poscopy[i][j] = player
    if 1<=i<=3 and 1<=j<=3:
        if positions[i-1][j] == player or positions[i+1][j] == player or positions[i][j-1] == player or positions[i][j+1] == player:    #raid
            ##print "haha"
            if positions[i-1][j] != '*' and positions[i-1][j] != player:
                poscopy[i-1][j] = player
            if positions[i+1][j] != '*' and positions[i+1][j] != player:
                poscopy[i+1][j] = player
            if positions[i][j-1] != '*' and positions[i][j-1] != player:
                poscopy[i][j-1] = player
            if positions[i][j+1] != '*' and positions[i][j+1] != player:
                poscopy[i][j+1] = player
        #else: poscopy[i][j] = player   #sneak

    elif j == 0 and 1<=i<=3:    #left boarder
        if positions[i-1][0] == player or positions[i+1][0] == player or positions[i][1] == player: #raid
            if positions[i-1][0] != '*' and positions[i-1][0] != player:
                poscopy[i-1][0] = player
            if positions[i+1][0] != '*' and positions[i+1][0] != player:
                poscopy[i+1][0] = player
            if positions[i][1] != '*' and positions[i][1] != player:
                poscopy[i][1] = player
        #else: poscopy[i][j] = player   #sneak

    elif j == 4 and 1<=i<=3:    #right boarder
        if positions[i-1][4] == player or positions[i+1][4] == player or positions[i][3] == player: #raid
            if positions[i-1][4] != '*' and positions[i-1][4] != player:    #raid
                poscopy[i-1][4] = player
            if positions[i+1][4] != '*' and positions[i+1][4] != player:
                poscopy[i+1][4] = player
            if positions[i][3] != '*' and positions[i][3] != player:
                poscopy[i][3] = player
        #else: poscopy[i][j] = player     #sneak

    elif i == 0 and 1<=j<=3:    #top boarder
        if positions[0][j-1] == player or positions[0][j+1] == player or positions[1][j] == player: #raid
            if positions[0][j-1] != '*' and positions[0][j-1] != player:
                poscopy[0][j-1] = player
            if positions[0][j+1] != '*' and positions[0][j+1] != player:
                poscopy[0][j+1] = player
            if positions[1][j] != '*' and positions[1][j] != player:
                poscopy[1][j] = player
        #else: poscopy[i][j] = player    #sneak

    elif i == 4 and 1<=j<=3:    #bottom boarder
        if positions[4][j-1] == player or positions[4][j+1] == player or positions[3][j] == player: #raid
            if positions[4][j-1] != '*' and positions[4][j-1] != player:
                poscopy[4][j-1] = player
            if positions[4][j+1] != '*' and positions[4][j+1] != player:
                poscopy[4][j+1] = player
            if positions[3][j] != '*' and positions[3][j] != player:
                poscopy[3][j] = player
        #else: poscopy[i][j] = player  #sneak

    elif i == 0 and j == 0:   #topleft corner
        if positions[0][1] == player or positions[1][0] == player:      #raid
            if positions[0][1] != '*' and positions[0][1] != player:
                poscopy[0][1] = player
            if positions[1][0] != '*' and positions[1][0] != player:
                poscopy[1][0] = player
        #else: poscopy[i][j] = player     #sneak
    elif i == 0 and j == 4:  #topright corner
        if positions[0][3] == player or positions[1][4] == player:      #raid
            if positions[0][3] != '*' and positions[0][3] != player:
                poscopy[0][3] = player
            if positions[1][4] != '*' and positions[1][4] != player:
                poscopy[1][4] = player
        #else: poscopy[i][j] = player    #sneak
    elif i == 4 and j == 0: #bottomleft corner
        if positions[3][0] == player or positions[4][1] == player:  #raid
            if positions[3][0] != '*' and positions[3][0] != player:
                poscopy[3][0] = player
            if positions[4][1] != '*' and positions[4][1] != player:
                poscopy[4][1] = player
        #else: tmpval += val    #sneak
    elif i == 4 and j == 4: #bottomright corner
        if positions[3][4] == player or positions[4][3] == player:  #raid
            if positions[3][4] != '*' and positions[3][4] != player:
                poscopy[3][4] = player
            if positions[4][3] != '*' and positions[4][3] != player:
                poscopy[4][3] = player

    return poscopy

def greedy(poscopy, positions, board, player):
    
    val = getVal(positions, board, player)
    maxval = val
    nextMove = poscopy
    tmpval = 0

    for i in range(5):
        for j in range(5):
            if positions[i][j] != '*':
                continue
            else:
                poscopy = getNextState(poscopy, positions, i, j, player)
                #print poscopy
                tmpval = getVal(poscopy, board, player)
                #print tmpval

                if tmpval > maxval:
                    maxval = tmpval
                    nextMove = copy.deepcopy(poscopy)

                tmpval = 0
                poscopy = copy.deepcopy(positions)
               
    return nextMove

nextState = copy.deepcopy(positions)

def minimaxDecision(positions, player, cutoff):
    depth = cutoff
    """ code added by Chi Zhang """
    #bestAction = (i, j)
    bestRow = 0
    bestCol = 0
    bestValue = -9999    # actual it is not a very good way to
    """ end """
    if task != 4:
        f1.write("root," + "0," + "-Infinity" + '\r\n')
        #print "root,", "0,", "-Infinity"

    for i in range(5):
        for j in range(5):
            if positions[i][j] != '*':
                continue
            coordTmp = coordinates[(i,j)]
            if depth != 1 and task != 4:
                f1.write(coordTmp + "," + str(depth-cutoff+1) + "," + "Infinity" + '\r\n')
                #print i, j, 1, "Infinity"
            poscopy = copy.deepcopy(positions)
            
            nextState = getNextState(poscopy, positions, i, j, player)
            stateCopy = copy.deepcopy(nextState)
            
            currValue = minValue(i, j, nextState, cutoff-1) # The cutoff should be read from the file
            if currValue > bestValue:
                #bestAction = (i, j)    some problem with this statement
                bestRow = i
                bestCol = j
                bestValue = currValue
            if task != 4:
                f1.write("root," + "0," + str(bestValue))
                if i !=4 or j != 4:
                    f1.write('\r\n')

            #print "root:", 0, bestValue

    tempPos = copy.deepcopy(positions)
    nextMove = getNextState(tempPos, positions, bestRow, bestCol, player)

    return nextMove

def maxValue(row, col, state, cutoff):
    if cutoff == 0 or boardIsFull(state):
        tempVal = getVal(state, board, player)
        coordTmp = coordinates[(row, col)]
        if task != 4:
            f1.write(coordTmp + "," + str(depth - cutoff) + "," + str(tempVal) + '\r\n')        
            #print  row, col, depth - cutoff, tempVal
        return tempVal
    v = -9999
    for i in range(5):
        for j in range(5):
            if state[i][j] != '*':
                continue
            stateCopy = copy.deepcopy(state)
            nextState = getNextState(stateCopy, state, i, j, player)
            v = max(v, minValue(i, j, nextState, cutoff-1))
            coordTmp = coordinates[(row, col)]
            if task != 4:
                f1.write(coordTmp + "," + str(depth - cutoff) + "," + str(v) + '\r\n')
                #print row, col, depth - cutoff, v
    
    return v

def minValue(row, col, state, cutoff):
    if cutoff == 0 or boardIsFull(state):
        tempVal = getVal(state, board, player)
        coordTmp = coordinates[(row, col)]
        if task != 4:
            f1.write(coordTmp + "," + str(depth - cutoff) + "," + str(tempVal) + '\r\n')  
            #print   row, col, depth - cutoff, tempVal
        return tempVal
    v = 9999
    for i in range(5):
        for j in range(5):
            if state[i][j] != '*':
                continue
            stateCopy = copy.deepcopy(state)
            nextState = getNextState(stateCopy, state, i, j, opponent)

            v = min(v, maxValue(i, j, nextState, cutoff-1))
            coordTmp = coordinates[(row, col)]
            if task != 4:
                f1.write(coordTmp + "," + str(depth - cutoff) + "," + str(v) + '\r\n')
                #print row, col, depth - cutoff, v
    
    return v

def alpha_beta_pruning(positions, player, cutoff):
    
    """ code added by Chi Zhang """
    #bestAction = (i, j)
    bestRow = 0
    bestCol = 0
    bestValue = -9999    # actual it is not a very good way to
    """ end """
    if task != 4:
        f1.write("root," + "0," + "-Infinity," + "-Infinity," + "Infinity" + '\r\n')
        #print "root," + "0," + "-Infinity" + "-Infinity," + "Infinity"

    alpha = -9999
    beta = 9999
    for i in range(5):
        for j in range(5):
            if positions[i][j] != '*':
                continue

            if depth != 1 and task != 4:
                if alpha == -9999:
                    alphaTmp = "-Infinity"
                else: alphaTmp = str(alpha)
                if beta == 9999:
                     betaTmp = "Infinity"
                else: betaTmp = str(beta)
                coordTmp = coordinates[(i,j)]
                f1.write(coordTmp + "," + str(1) + "," + "Infinity," + alphaTmp + "," + betaTmp + '\r\n')
                #print coordTmp + "," + str(1) + "," + "Infinity," + alphaTmp + "," + betaTmp

            poscopy = copy.deepcopy(positions)
            
            nextState = getNextState(poscopy, positions, i, j, player)
            stateCopy = copy.deepcopy(nextState)

            
            currValue = pruning_minValue(i, j, nextState, cutoff-1, alpha, beta) # The cutoff should be read from the file
            if(currValue >= beta):
                if positions[i][j] != '*':
                    continue
                if task != 4:
                    if alpha == -9999:
                        alphaTmp = "-Infinity"
                    else: alphaTmp = str(alpha)
                    if beta == 9999:
                         betaTmp = "Infinity"
                    else: betaTmp = str(beta)
                    coordTmp = coordinates[(i,j)]
                    f1.write(coordTmp + "," + str(depth - cutoff) + "," + "Infinity," + alphaTmp + "," + betaTmp + '\r\n')
                    #print coordTmp + "," + str(depth - cutoff) + "," + "Infinity," + alphaTmp + "," + betaTmp
                    ##print i, j, depth - cutoff, currValue, alpha, beta
                bestRow = i
                bestCol = j
                tempPos = copy.deepcopy(positions)
                nextMove = getNextState(tempPos, positions, bestRow, bestCol, player)

                return nextMove

            #alpha = max(alpha, currValue)
            if task != 4:
                if currValue > alpha:
                    #bestAction = (i, j)    some problem with this statement
                    bestRow = i
                    bestCol = j
                    alpha = currValue

                if alpha == -9999:
                    alphaTmp = "-Infinity"
                else: alphaTmp = str(alpha)
                if beta == 9999:
                     betaTmp = "Infinity"
                else: betaTmp = str(beta)
                f1.write("root," + str(0) + "," + alphaTmp + ","+ alphaTmp + "," + betaTmp)
                #print "root," + str(0) + "," + alphaTmp + ","+ alphaTmp + "," + betaTmp
                if i != 4 or j != 4:
                    f1.write('\r\n')

    tempPos = copy.deepcopy(positions)
    nextMove = getNextState(tempPos, positions, bestRow, bestCol, player)
    return nextMove       
    #return bestRow, bestCol

def pruning_maxValue(row, col, state, cutoff, alpha, beta):
    if cutoff == 0 or boardIsFull(state):
        tempVal = getVal(state, board, player)
        if task != 4:
            if alpha == -9999:
                alphaTmp = "-Infinity"
            else: alphaTmp = str(alpha)
            if beta == 9999:
                betaTmp = "Infinity"
            else: betaTmp = str(beta)
            coordTmp = coordinates[(row, col)]
            f1.write(coordTmp + "," + str(depth - cutoff) + "," + str(tempVal) + "," + alphaTmp + "," + betaTmp + '\r\n')
            #print coordTmp + "," + str(depth - cutoff) + "," + str(tempVal) + "," + alphaTmp + "," + betaTmp
            ##print  row, col, depth - cutoff, tempVal, alpha, beta
        return tempVal
    v = -9999
    for i in range(5):
        for j in range(5):
            if state[i][j] != '*':
                continue
            stateCopy = copy.deepcopy(state)
            nextState = getNextState(stateCopy, state, i, j, player)
            v = max(v, pruning_minValue(i, j, nextState, cutoff-1, alpha, beta))

            if v >= beta:
                if task != 4:
                    if alpha == -9999:
                        alphaTmp = "-Infinity"
                    else: alphaTmp = str(alpha)
                    if beta == 9999:
                        betaTmp = "Infinity"
                    else: betaTmp = str(beta)
                    coordTmp = coordinates[(row, col)]
                    f1.write(coordTmp + "," + str(depth - cutoff) + "," + str(v) + "," + alphaTmp + "," + betaTmp + '\r\n')
                    #print coordTmp + "," + str(depth - cutoff) + "," + str(v) + "," + alphaTmp + "," + betaTmp

                return v
            alpha = max(alpha, v)

            if task != 4:
                if alpha == -9999:
                    alphaTmp = "-Infinity"
                else: alphaTmp = str(alpha)
                if beta == 9999:
                    betaTmp = "Infinity"
                else: betaTmp = str(beta)
                coordTmp = coordinates[(row, col)]
                f1.write(coordTmp + "," + str(depth - cutoff) + "," + str(v) + "," + alphaTmp + "," + betaTmp + '\r\n')              
                #print coordTmp + "," + str(depth - cutoff) + "," + str(v) + "," + alphaTmp + "," + betaTmp
                #print row, col, depth - cutoff, v, alpha, beta

    
    return v

def pruning_minValue(row, col, state, cutoff, alpha, beta):
    if cutoff == 0 or boardIsFull(state):
        tempVal = getVal(state, board, player)
        if task != 4:
            if alpha == -9999:
                alphaTmp = "-Infinity"
            else: alphaTmp = str(alpha)
            if beta == 9999:
                betaTmp = "Infinity"
            else: betaTmp = str(beta)
            coordTmp = coordinates[(row, col)]
            f1.write(coordTmp + "," + str(depth - cutoff) + "," + str(tempVal) + "," + alphaTmp + "," + betaTmp + '\r\n')
            #print coordTmp + "," + str(depth - cutoff) + "," + str(tempVal) + "," + alphaTmp + "," + betaTmp
        return tempVal
    v = 9999
    for i in range(5):
        for j in range(5):
            if state[i][j] != '*':
                continue
            stateCopy = copy.deepcopy(state)
            nextState = getNextState(stateCopy, state, i, j, opponent)
            v = min(v, pruning_maxValue(i, j, nextState, cutoff-1, alpha, beta))

            if v <= alpha:
                if alpha == -9999:
                    alphaTmp = "-Infinity"
                else: alphaTmp = str(alpha)
                if beta == 9999:
                    betaTmp = "Infinity"
                else: betaTmp = str(beta)
                coordTmp = coordinates[(row, col)]
                f1.write(coordTmp + "," + str(depth - cutoff) + "," + str(v) + "," + alphaTmp + "," + betaTmp + '\r\n')               
                #print coordTmp + "," + str(depth - cutoff) + "," + str(v) + alphaTmp + "," + betaTmp

                return v
            beta = min(beta, v)

            if task != 4:
                if alpha == -9999:
                    alphaTmp = "-Infinity"
                else: alphaTmp = str(alpha)
                if beta == 9999:
                    betaTmp = "Infinity"
                else: betaTmp = str(beta)
                coordTmp = coordinates[(row, col)]
                f1.write(coordTmp + "," + str(depth - cutoff) + "," + str(v) + "," + alphaTmp + "," + betaTmp + '\r\n')           
                #print coordTmp + "," + str(depth - cutoff) + "," + str(v) + alphaTmp + "," + betaTmp

    return v


if task == 4:
    def battle_simulation(state, player, board):
        if boardIsFull(state):
            return state

        taskTmp = 0
        nextState = [[]]
        if player == player1:
            taskTmp = task1
            cutoffTmp = cutoff1
        else: 
            taskTmp = task2
            cutoffTmp = cutoff2

        currStateCopy = copy.deepcopy(state)

        if taskTmp == 1:
            nextState = greedy(currStateCopy, state, board, player)
        elif taskTmp == 2:
            nextState = minimaxDecision(state, player, cutoffTmp)
        elif taskTmp == 3:
            nextState = alpha_beta_pruning(state, player, cutoffTmp)

        for i in range(5):
            for j in range(5):
                f.write(nextState[i][j])   
            f.write('\r\n')     
        return nextState


if task == 1:
    nextMove = greedy(poscopy, positions, board, player)
    f = open('next_state.txt', 'w')
    for i in range(5):
        for j in range(5):
            f.write(nextMove[i][j])
        if i != 4 or j != 4:    
            f.write('\r\n')

if task == 2:
    f1 = open('traverse_log.txt', 'w')
    f1.write("Node," + "Depth," + "Value" + '\r\n')
    f2 = open('next_state.txt', 'w')
    nextMove = minimaxDecision(positions, player, cutoff)
    for i in range(5):
        for j in range(5):
            f2.write(nextMove[i][j])
        if i != 4 or j != 4:    
            f2.write('\r\n')

if task == 3:
    f1 = open('traverse_log.txt', 'w')
    f1.write("Node," + "Depth," + "Value," + "Alpha," + "Beta" + '\r\n')
    f2 = open('next_state.txt', 'w')
    nextMove = alpha_beta_pruning(positions, player, cutoff)
    for i in range(5):
        for j in range(5):
            f2.write(nextMove[i][j])
        if i != 4 or j != 4:    
            f2.write('\r\n')

if task == 4:
    f = open('trace_state.txt', 'w')
    initState = positions
    nextMove = battle_simulation(initState, player1, board)
    f.write('\r\n')
    while(not boardIsFull(nextMove)):
        nextMove = battle_simulation(nextMove, player2, board)
        f.write('\r\n')
        nextMove = battle_simulation(nextMove, player1, board)
        f.write('\r\n')


