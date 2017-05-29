
from utils import *
import random

"""
alphabeta_search: Player player, Game game
-Takes a Game object and also the player who is going next
- and returns the best move based on the heuristics function

Helper functions included:
    search
    min_value
    max_value
    surcessor
    heuristics
    
Local Variables:
    numPrunedNode
    
- 
"""
def alphabeta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    
    '''
    Terminates when game.actions is empty
    Class Game needs the following functions:
        - game.result(state, a) -- successor
        - game.actions(state) -- possible moves
        - game.utility -- returns the state of the game (win/lose or tie, when game is terminal)
        
    '''
    state = game
    d = 20 #this is the cutoff test depth value. if we exceed this value, stop
    cutoff_test=None
    eval_fn = None 
    player = game.to_move(state)
    
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            print "max call:"
            print state.moves
            print game.moves
            print a
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    #def cutoff_test and eval_fn 
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    #by default, utility score is used
    
    #argmax goes through all the possible actions and 
    #  applies the alphabeta search onto all of them
    #  and returns the move with the best score 
    return argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a),
                                      -infinity, infinity, 0))
                                      
class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        "Return a list of the allowable moves at this point."
        pass

    def result(self, state, move):
        "Return the state that results from making a move from a state."
        pass

    def utility(self, state, player):
        "Return the value of this final state to player."
        pass

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.actions(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        pass
        #print(state)

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

   
class goGame(Game):               
    ''' State should contain the player, moves (possible moves), liberty (*utility*--same as score), board, connectedpieces
        - .initial function defines
        
        Functions:  
            update_spaces: null -> null
                - Run this to check for valid move (run terminal_test?)
                - and update to check game status
                - Update pieces in the game
                    - Checks if connectedPieces merges can happen
            make_move: int x, int y -> boolean
                - checks if move is good
            terminal_test: null -> boolean
                - checks if the game is done (i.e. no more moves)
                - updates possible_moves
            draw_graph: null -> null
                - displays current game grid
            successor: Game, int x, int y -> Game
                - put in a move and generates new Game object (successor)
    '''
    '''
        initpieces: array of [int, int]
        boardwidth: int
        boardheight: int
    '''
    '''initialize fn********************************************************************************'''
    
    survivalState = None
    def __init__(self, player, moves, board, connectedPieces, survivalState):
        '''
            initialize all state variables here
        '''
        self.player = player
        self.moves = moves
        self.board = board
        self.connectedPieces = connectedPieces
        self.survivalState = survivalState
        
    def actions(self, state):
        ''' returns the allowable moves, this is predefined???? '''
        return state.moves
    
    '''successor fn********************************************************************************'''
    def result(self, state, move):
        print "successor with:"
        print state.moves
        print move
        ''' successor function, takes a move and returns a state '''
        return generateSuccessors(state, move)
        
    #do not use utility, use heuristics fn instead
    def utility(self, state, player):
        "Return the value of this final state to player."
        '''  print the board        '''
        self.display(state)
        return 0
    
    '''terminal test********************************************************************************'''
    def terminal_test(self, state):
        '''checks if actions is empty. if it is empty, then we are terminal. 
        or if we reach survival state is true. '''
        if state.actions(state):
            return False
        else:
            return True
        '''alternatively, 'return self.actions(self, state)' '''

    '''returns a player'''
    def to_move(self, state):
        "Return the player whose move it is in this state."
        return if_(state.player == 'Att', 'Def', 'Att')

    def display(self, state):
        "Print or otherwise display the state."
        pass
        #for i in self.board:
            #print i

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
    
    
#query_player asks user for an input of int, int, this is translated
#  to a board move and input into state
def query_player(game, state):
    "Make a move by querying standard input."
    game.display(state)
    return num_or_str(raw_input('Your move? '))

#queries the alphabeta algorithm for a game move
# input is game class object and a state. returns a game move of [int, int]
def alphabeta_player(game, state):
    return alphabeta_search(state, game)
        
def play_game(game, initgame, *players):
    '''
    Variables: Player one, Player two, Game game
        
    Function:
        Play_game: null -> null, output to std_io
            1. Checks if everything is initialized
                - Game baord needs to be initialized and
                - Player needs to be initialized (at least 1)
            2. Loops through player AI_1 and AI_2 or
                Loops through input and player AI_1
            *. If player is null, then look for player input instead
    '''
    
    state = generateInitialState(initgame[0], initgame[1], initgame[2], initgame[3])
    while True:
        for player in players:
            move = player(game, state)
            state = game.result(state, move)
            if game.terminal_test(state):
                return game.utility(state, game.to_move(game.initial))

def allbut(dpieces, apieces, dim):
  gavail = []
  for i in xrange(dim[0]):
    for j in xrange(dim[1]):
      gavail.append((i,j))
  for i in dpieces:
    if i in gavail:
      gavail.remove(i)
  for i in apieces:
    if i in gavail:
      gavail.remove(i)
  return gavail
  
def printgame(dpieces, apieces, dim):
  disp = []
  
  for i in xrange(dim[1]): 
    disp.append([]) 
    for j in xrange(dim[0]): 
      disp[i].append(0)
  
  for i in dpieces:
      disp[i[0]][i[1]] = 1 #white
  for i in apieces:
      disp[i[0]][i[1]] = 2 #black
  
  
  for i in disp:
      print i
  
  #this is printboard fn, to be split off
  print '_______________________________'
  for i in disp:
    for j in i:
      if j == 0: #space
        print u'\u2009' + ' |',
      if j == 1: #white
        print u'\u25FB' + '|',
      if j == 2: #black
        print u'\u25FC' + '|',
    print ''
  print '_______________________________'
  
'''''''''''''''''''''''''''''''''
#################################################################
#################################################################

#################################################################
#################################################################

#################################################################
#################################################################

#################################################################
#################################################################

#################################################################
#################################################################

#################################################################
#################################################################

#################################################################
#################################################################

'''''''''''''''''''''''''''''''''


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


def generateConnectedPieces(pieceList, board):
    #inputs:
    #pieceList: list of tuples containing all 'Att' or 'Def' pieces
    #board: {'Att': attackerPieces, 'Def': defenderPieces, 'Avail': availableSpots, 'All':allSpots}
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
    connectedPiecesWithLib = []
    for connectedPieces in connectedPiecesList:
        liberties = calculateLiberties(connectedPieces, board)
        connectedPiecesWithLib.append((connectedPieces, liberties))
    return connectedPiecesWithLib


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
            if (move in group[1]) & (len(group[1]) > 1):
                return True
        # check if opponents pieces will be taken as a result of putting the next pieces down
        # if so don't remove those pieces (only checking for legal move)
        for group in connectedPieces[opp]:
            if (move in group[1]) & (len(group[1]) == 1):
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

def checkSurvivalState(board):
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
    connectedPiecesWithLibAtt = generateConnectedPieces(newBoard['Att'], newBoard)
    # defender pieces
    connectedPiecesWithLibDef = generateConnectedPieces(newBoard['Def'], newBoard)
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

    newSurvivalState = checkSurvivalState(newBoard)
    newState = goGame(newPlayer, newMoves, newBoard, newConnectedPieces, newSurvivalState)
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
    initialState = goGame(player, moves, board, connectedPieces, survivalState)
    return initialState

  
'''''''''''''''''''''''''''''''''
#################################################################
#################################################################

#################################################################
#################################################################

#################################################################
#################################################################

#################################################################
#################################################################

#################################################################
#################################################################

#################################################################
#################################################################

#################################################################
#################################################################

'''''''''''''''''''''''''''''''''

if __name__ == "__main__":
    dpieces0 = [(1,0), (1,2), (1,3), (2,3), (3,0), (3,1), (3,2)]
    apieces0 = [(0,1), (0,3), (0,4), (1,4), (2,4), (3,3), (3,4), (4,0), (4,1), (4,2)]
    avail0 = [(0,0), (0,2), (1,1), (2,0), (2,1), (2,2)]
    dim0 = (6,6)
    game0 = [dpieces0, apieces0, avail0, dim0]
    
    dpiecesd1 = [(1,1),(1,2),(1,3),(2,0),(2,2),(3,1),(3,3),(4,3)]
    apiecesd1 = [(2,3),(2,4),(2,5),(3,2),(3,4),(4,1),(4,2)]
    availd1 = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), 
              (1, 0), (1, 4), (1, 5), (1, 6), 
              (2, 6), 
              (3, 0), (3, 5), (3, 6), 
              (4, 0), (4, 4), (4, 5), (4, 6), 
              (5, 0), (5, 1), (5, 2), (5, 3), (5, 4)]
    dimd1 = (6,7)
    gamed1 = [dpiecesd1, apiecesd1, availd1, dimd1]
    
    dpieceds2 = [(0,0),(1,1),(1,2),(1,3),(2,3),(3,0),(3,3),(4,2),(5,2),(6,2),(7,1),(8,2)]
    apieceds2 = [(1,0),(2,0),(2,1),(2,2),(4,1),(5,1),(6,0),(6,1)]
    dims2 = (10,5)
    avails2 = [(0, 1), (0, 2), (0, 3), (0, 4), 
                (1, 4), 
                (2, 4), 
                (3, 1), (3, 2), (3, 4), 
                (4, 0), (4, 3), (4, 4), 
                (5, 0), (5, 3), (5, 4), 
                (6, 3), (6, 4), 
                (7, 0), (7, 2), (7, 3), 
                (8, 0), (8, 1), (8, 3), 
                (9, 0), (9, 1), (9, 2), (9, 3)]
    games2 = [dpieceds2, apieceds2, avails2, dims2]
    
    dpieces1 = [(0,1),(1,2),(1,3),(2,1),(3,1),(3,2),(4,3),(5,3),(6,1),(6,2)]
    apieces1 = [(1,1),(1,4),(2,2),(2,3),(2,4),(3,3),(4,1),(4,2),(5,1)]
    dims1 = (8,6)
    avails1 = [(0, 0), (0, 2), (0, 3), (0, 4), (0, 5), 
                (1, 0), (1, 5), 
                (2, 0), (2, 5), 
                (3, 0), (3, 4), (3, 5),
                (4, 0), (4, 4), (4, 5),
                (5, 0), (5, 2), (5, 4),
                (6, 0), (6, 3), (6, 4), 
                (7, 0), (7, 1), (7, 2), (7, 3)]
    games1 = [apieces1, dpieces1, avails1, dims1]
    
    gamestate1 = generateInitialState(game0[0], game0[1], game0[2], game0[3])
    
    alphabeta_search(gamestate1, gamestate1)
    
    
    
    
    
    
    
    
    
    
    
    