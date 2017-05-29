
from goGameClass import *

def generateNeighbors(piecelist):
    if len(piecelist) == 1:
        piece = piecelist[0]
        if piece == (0,0):
            return [(0,1), (1,0)]
        elif piece[0] == 0:
            return [(piece[0], piece[1] - 1), (piece[0], piece[1] + 1), (piece[0] + 1, piece[1])]
        elif piece[1] == 0:
            return [(piece[0], piece[1] + 1), (piece[0] + 1, piece[1]), (piece[0] - 1, piece[1])]
        else:
            return [(piece[0], piece[1] - 1), (piece[0], piece[1] + 1), (piece[0] + 1, piece[1]), (piece[0] - 1, piece[1])]
    else:
        neighbors = []
        for piece in piecelist:
            adjacentSpots = generateNeighbors([piece])
            for adjacentSpot in adjacentSpots:
                #add adjacentSpot to neighbors only if adjacentSpot is not one of the pieces in piecelist and is not part of neighbors already
                if (adjacentSpot not in piecelist) & (adjacentSpot not in neighbors):
                    neighbors.append(adjacentSpot)
        return neighbors

def findConnectedPieces(connectedPiecesList):
    connectionFound = False
    newConnectedPiecesList = list(connectedPiecesList)
    for i in range(len(connectedPiecesList)):
        for j in range(i + 1, len(connectedPiecesList)):
            neighbors = generateNeighbors(connectedPiecesList[i])
            for neighbor in neighbors:
                if neighbor in connectedPiecesList[j]:
                    newConnectedPiecesList.remove(connectedPiecesList[i])
                    newConnectedPiecesList.remove(connectedPiecesList[j])
                    newConnectedPiecesList.append(connectedPiecesList[i] + connectedPiecesList[j])
                    connectionFound = True
                    return (connectionFound, newConnectedPiecesList)
    #return original list if no connection found
    return (connectionFound, connectedPiecesList)


def generateConnectedPieces(pieceList, board, calcLib):
    #inputs:
    #pieceList: list of tuples containing all 'Att' or 'Def' pieces
    #board: {'Att': attackerPieces, 'Def': defenderPieces, 'Avail': availableSpots, 'All':allSpots, 'EyeSpots': eyespots}
    #calcLib: calculate liberties or not
    #board will not be used if calcLib is False
    connectedPiecesList = []
    for piece in pieceList:
        groupFound = False
        for connectedPieces in connectedPiecesList:
            if groupFound:
                break
            else:
                for groupPiece in connectedPieces:
                    if groupFound:
                        break
                    elif (abs(piece[0]-groupPiece[0]) + abs(piece[1]-groupPiece[1])) == 1:#check for adjacency
                        groupFound = True
                        connectedPieces.append(piece)
        if not groupFound:
            connectedPiecesList.append([piece])
    #merge connected pieces (pieces within a group might be separated depending on the order of pieces in piecelist
    connectionFound = True
    while connectionFound == True:
        connectionFound, connectedPiecesList = findConnectedPieces(connectedPiecesList)

    #calculate liberties for each group
    if calcLib:
        connectedPiecesWithLib = []
        for connectedPieces in connectedPiecesList:
            liberties = calculateLiberties(connectedPieces, board)
            connectedPiecesWithLib.append((connectedPieces, liberties))
        return connectedPiecesWithLib
    else:
        return connectedPiecesList


##not implemented (too complicated: need to update liberties for both sides and more complicated if some pieces are taken)
##generateConnectedPieces is used now to update the states
# def updateConnectedPieces(connectedPieces, move, player):
#     #input:
#     # connectedPieces: {'Att': connectedPiecesWithLibAtt, 'Def': connectedPiecesWithLibDef}
#     # move: tuple
#
#     #generate neighbors:
#     neighbors = generateNeighbors([move])
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
        neighbors = generateNeighbors([piece])
        for neighbor in neighbors:
            if (neighbor in board['All']) & (neighbor not in liberties):
                liberties.append(neighbor)
    return liberties

def checkLegal(move, board, connectedPiecesWithLib, player):
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
        for group in connectedPiecesWithLib[player]:
            if (move in group[1]) & (len(group[1]) > 1):
                return True
        # check if opponents pieces will be taken as a result of putting the next pieces down
        # if so don't remove those pieces (only checking for legal move)
        for group in connectedPiecesWithLib[opp]:
            if (move in group[1]) & (len(group[1]) == 1):
                #need to account for ko in the future
                return True
    return False

#update board
def updateBoard(move, board, connectedPiecesWithLib, player):
    #input: board{'Att': attackerPieces, 'Def': defenderPieces, 'Avail': availableSpots, 'All':allSpots}
    if player == 'Def':
        opp = 'Att'
    else:
        opp = 'Def'
    # check if opponents pieces will be taken as a result of putting the next pieces down
    # if so update opponents pieces
    for group in connectedPiecesWithLib[opp]:
        #if one of the opponents group only has one liberty left and the liberty spot is occupied by 'move',
        # the group should be removed. More than one group can be removed as a result of playing one piece
        if (move in group[1]) & (len(group[1]) == 1):
            #remove all taken pieces and refill available and all spots
            for  piece in group[0]:
                board[opp].remove(piece)
                board['Avail'].append(piece)
                board['All'].append(piece)
    # add move to player's pieces and remove it from 'Avail' and 'All'
    board[player].append(move)
    board['Avail'].remove(move)
    board['All'].remove(move)
    return board

def countDiagNeighborSpots(spot):
    #input: tuple:
    #output: number of diagonal neighbors the spot has
    if spot == (0,0):#corner spots
        #1 spot occupied by defender implies real eye, 1 spot occupied by attacker implies false eye
        return {'Real': 1, 'False': 1}
    elif (spot[0] == 0) | (spot[1] == 0):#edge spots
        #2 spots occupied by defender implies real eye, 1 spot occupied by attacker implies false eye
        return {'Real': 2, 'False': 1}
    else:#non-edge spots
        #3 spots occupied by defender implies real eye, 2 spots occupied by attacker implies false eye
        return {'Real': 3, 'False': 2}


def checkSurvivalState(board, player):
    #two solid eyes within one group of connected pieces
    #generate connected spots
    #potential eye spots are all available spot and any attacker pieces enclosed within of an eye
    availEyeSpot = board['Avail'] + [spot for spot in board['Att'] if spot in board['EyeSpots']]
    connectedSpots = generateConnectedPieces(availEyeSpot, None, False)
    eyes = []
    for group in connectedSpots:
        # if all neighbors of a group is occupied by the defender, the group forms an eye
        enclosed = True
        for neighbor in generateNeighbors(group):
            if neighbor in board['Att']:
                enclosed = False
                break
        if enclosed:
            #determine eye type
            #if any spots in an eye has diagonal neighbors that are occupied by the attacker pieces s.t.
            #  the neighbors forming the eye can be removed, it's a false eye
            eyeType = 'Real'
            falseSpotCount = 0
            for spot in group:
                vitalSpots = countDiagNeighborSpots(spot)
                diagNeighbors = [(spot[0]+1, spot[1] - 1), (spot[0]-1, spot[1] + 1), (spot[0] + 1, spot[1] +1), (spot[0] - 1, spot[1]-1)]
                #number of diagonal neighbors occupied by attacker pieces (not including ones trapped in eyes)
                attSpots = set(diagNeighbors).intersection(set(board['Att']))
                numAttSpots = len([spot for spot in attSpots if spot not in group])
                print([spot for spot in attSpots if spot not in group])
                if numAttSpots >= vitalSpots['False']:#false eyes
                    eyeType = 'False'
                    falseSpotCount += 1
                else:#unknown eyes
                    #number of diagNeighbors of a spot that is either ocupied by a defender piece or is part of the eye
                    print(board['Def']+group)
                    numDefSpots = len(set(diagNeighbors).intersection(set((board['Def']+group))))
                    if numDefSpots < vitalSpots['Real']:#3 or more spots occupied by defender consititutes a real eye
                        #false eye supercede real or unknown eyes
                        if eyeType != 'False':
                            eyeType = 'Unknown'
            #Each eye is a dictinary containing the following:
            #'Group': list the coordinate of all spots of an eye
            #'EyeType': 'Unknown', 'Real', or 'False'
            #'FalseSpots': number of spots in an eye that cannot form a real eye
            #'FalseSpots' is zero when eyeType is 'Real' or 'Unknown'
            eyes.append({'Group': group, 'EyeType': eyeType, 'FalseSpots': falseSpotCount})

    # if 2 solid eyes then survival state is true
    realEyes = [eye for eye in eyes if eye['EyeType'] == 'Real']
    if len(realEyes) >= 2:
        return True
    # #if only 1 solid eye, check for possible states that it could survive
    # #minimum 3 spaces required to constitute a survival state
    # elif len(realEyes) == 1:
    #     if (len(realEyes[0]['Group']) == 3) & player == 'Def':
    #         return True
    #     elif len(realEyes[0]['Group']) == 4:
    return False

#curState:
#availableSpots: List of available spots to put the next piece
#connectedPiecesAtt: List of connected pieces and the number of liberties of the attacker
#connectedPiecesDef: List of connected pieces and the number of liberties of the defender
def generateSuccessors(curState, move):
    #inputs:
    # curState: GoGame object
    # move: the move that will be added to curState
    newBoard = updateBoard(move, curState.board, curState.connectedPieces, curState.player)
    # find connnected pieces and calculate their liberties
    # attacker pieces
    connectedPiecesWithLibAtt = generateConnectedPieces(newBoard['Att'], newBoard, True)
    # defender pieces
    connectedPiecesWithLibDef = generateConnectedPieces(newBoard['Def'], newBoard, True)
    newConnectedPieces = {'Att': connectedPiecesWithLibAtt, 'Def': connectedPiecesWithLibDef}
    #alternate player for next state
    if curState.player == 'Def':
        newPlayer = 'Att'
    else:
        newPlayer = 'Def'
    #define all legal moves for the SUCCESSOR state, not the current state
    newMoves = []
    for nextMove in newBoard['Avail']:
        if checkLegal(nextMove, newBoard, newConnectedPieces, newPlayer):
            newMoves.append(nextMove)

    newSurvivalState = checkSurvivalState(newBoard, newPlayer)
    newState = GoGame(newPlayer, newMoves, newBoard, newConnectedPieces, newSurvivalState)
    return newState