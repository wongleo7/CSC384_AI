def generateNeighbors(piece):
    return [(piece[0], piece[1] - 1), (piece[0], piece[1] + 1), (piece[0] + 1, piece[1]), (piece[0] - 1, piece[1])]

def generateConnectedPieces(pieceList, board):
    #inputs:
    #pieceList: list of tuples connected to each piece
    #find all connected pieces
    connectedPiecesList = []
    for att in pieceList:
        groupFound = False
        for connectedPieces in connectedPiecesList:
            if groupFound:
                break
            else:
                for piece in connectedPieces:
                    if groupFound:
                        break
                    elif (abs(att[0]-piece[0]) + abs(att[1]-piece[1])) == 1:#check for adjacency
                        groupFound = True
                        connectedPieces.append(att)
        if not groupFound:
            connectedPiecesList.append([att])
    #calculate liberties for each group
    connectedPiecesWithLibAtt = []
    for connectedPieces in connectedPiecesList:
        liberties = calculateLiberties(connectedPieces, board)
        connectedPiecesWithLibAtt.append((connectedPieces, liberties))
    return connectedPiecesList


##not implemented (too complicated: need to update liberties for both sides and more complicated if some pieces are taken)
##generateConnectedPieces is used now to update the states
# def updateConnectedPieces(connectedPieces, move, player):
#     #input:
#     # connectedPieces: {'Att': connectedPiecesWithLibAtt, 'Def': connectedPiecesWithLibDef}
#     # move: tuple
#
#     #generate neighbors:
#     neighbors = generateNeighbors(move)
#     if player == 'Def':
#         newConnectedPieces = connectedPieces['Def']
#         joinedPieces = (move, 4)
#         for neighbor in neighbors:
#             for group in connectedPieces['Def']:
#                 if neighbor in group:
#                     newConnectedPieces.remove(group)
#                     joinedPieces.append(group)




def calculateLiberties(connectedPieces, board):
    #input:
    #connectedPieces: list of 2-element tuples: (group, liberties) where both group and liberties are list of coordinates
    #board: board dictionary (board['All'] will be used to count liberties)
    liberties = []
    for piece in connectedPieces:
        neighbors = generateNeighbors(piece)
        for neighbor in neighbors:
            if (neighbor in board['All']) & (neighbor not in liberties):
                liberties.append(neighbor)
    return liberties

def checkLegal(move, board, connectedPieces, player):
    if player == 'Def':
        opp = 'Att'
    else:
        opp = 'Def'
    #make sure move if not occupied
    if (move not in board['All']) | (move not in board['Avail']) | (move in board['Att']) | (move in board['Def']):
        print('Error: move already occupied')
    else:
        #if at least one neighbor is not occupied
        neighbors = [(move[0], move[1] - 1), (move[0], move[1] + 1), (move[0] + 1, move[1]),(move[0] - 1, move[1])]
        for neighbor in neighbors:
            if neighbor in board['All']:
                return True
        #check if next move is connected to a group of connected pieces and in which its liberties greater than 1
        #liberties need to be greater than 1 since the move itself will reduce its liberties by one
        for group in connectedPieces[player]:
            if move in group[1] & len(group[1]) > 1:
                return True
        # check if opponents pieces will be taken as a result of putting the next pieces down
        # if so don't remove those pieces (only checking for legal move)
        for group in connectedPieces[opp]:
            if move in group[1] & len(group[1]) == 1:
                #need to account for ko in the future
                return True
    return False

#update board
def updateBoard(move, board, connectedPieces, player):
    #input: board{'Att': attackerPieces, 'Def': defenderPieces, 'Avail': availableSpots, 'All':allSpots}
    if player == 'Def':
        opp = 'Att'
    else:
        opp = 'Def'
    # check if opponents pieces will be taken as a result of putting the next pieces down
    # if so update opponents pieces
    for group in connectedPieces[opp]:
        #if one of the opponents group only has one liberty left and the liberty spot is occupied by 'move',
        # the group should be removed. More than one group can be removed as a result of playing one piece
        if move in group[1] & len(group[1]) == 1:
            #remove all taken pieces and refill available and all spots
            for  piece in group[0]:
                board[opp].remove(piece)
                board['Avail'].append(piece)
                board['All'].append(piece)
    # add move to player's pieces
    board[player].append(move)
    return board

def checkSurvivalState(board):
    return False

#curState:
#availableSpots: List of available spots to put the next piece
#connectedPiecesAtt: List of connected pieces and the number of liberties of the attacker
#connectedPiecesDef: List of connected pieces and the number of liberties of the defender
def generateSuccessors(self, curState, move):
    #inputs:
    # curState: GoGame object
    # move: the move that will be added to curState
    newBoard = updateBoard(move, curState.board, curState.connectedPieces, curState.player)
    # find connnected pieces and calculate their liberties
    # attacker pieces
    connectedPiecesWithLibAtt = generateConnectedPieces(newBoard.attackerPieces, newBoard)
    # defender pieces
    connectedPiecesWithLibDef = generateConnectedPieces(newBoard.defenderPieces, newBoard)
    newConnectedPieces = {'Att': connectedPiecesWithLibAtt, 'Def': connectedPiecesWithLibDef}
    #alternate player for next state
    if curState.player == 'Def':
        newPlayer = 'Att'
    else:
        newPlayer = 'Def'
    #define all legal moves for the SUCCESSOR state, not the current state
    newMoves = []
    for nextMove in newBoard.availableSpots:
        if checkLegal(nextMove, newBoard, newConnectedPieces, newPlayer):
            newMoves.append(nextMove)

    newSurvivalState = checkSurvivalState(newBoard)
    newState = GoGame(newPlayer, newMoves, newBoard, newConnectedPieces, newSurvivalState)
    return newState

def generateInitialState(attackerPieces, defenderPieces, availableSpots, dim):
    #inputs:
    #attackerPieces: list of tuples specifying coordinates of all attacker pieces
    #defenderPieces: list of tuples specifying coordinates of all defender pieces
    #availableSpots: list of tuples specifying coordinates of all remaining spots that can be played
    #dim: tuple specifying dimension of the board

    #define whether this state is a survival state
    survivalState = False

    #Define board
    #allSpots: list of tuples specifying the boundary of the board (used to counting liberties)
    allSpots = [(x,y) for x in range(dim[0]) for y in range(dim[1])]
    for i in attackerPieces:
        allSpots.remove(i)
    for j in defenderPieces:
        allSpots.remove(j)
    board = {'Att': attackerPieces, 'Def': defenderPieces, 'Avail': availableSpots, 'All':allSpots}

    #find connnected pieces and calculate their liberties
    #attacker pieces
    connectedPiecesWithLibAtt = generateConnectedPieces(attackerPieces, board)

    #defender pieces
    connectedPiecesWithLibDef = generateConnectedPieces(defenderPieces, board)

    connectedPieces = {'Att': connectedPiecesWithLibAtt, 'Def': connectedPiecesWithLibDef}

    #define player who is playing next given the current state (defender always goes first)
    player = 'Def'

    #define all legal moves
    moves = []
    for move in availableSpots:
        if checkLegal(move, board, connectedPieces, player):
            moves.append(move)

    #create a GoGame object
    initialState = GoGame(player, moves, board, connectedPieces, survivalState)
    return initialState




defenderPieces = [(1,0), (1,2), (1,3), (2,3), (3,0), (3,1), (3,2)]
attackerPieces = [(0,1), (0,3), (0,4), (1,4), (2,4), (3,3), (3,4), (4,0), (4,1), (4,2)]
availableSpots = [(0,0), (0,2), (1,1), (2,0), (2,1), (2,2)]
dim = (6,6)
initialState = generateInitialState(defenderPieces, attackerPieces, availableSpots, dim)
print(initialState.player)
print(initialState.connectedPieces['Att'])
print(initialState.connectedPieces['Def'])
print(initialState.moves)
print(initialState.board)

#use utility to print states
#use eval_fn to calculate heuristics for next state
#have not implemented survivalState yet (assume false unless no more moves)

