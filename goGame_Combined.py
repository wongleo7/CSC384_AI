'''****************************************************
GO - Life or Death

CSC384 Final Project

Team Members:  
- Shayne Lin 
- Leo Wong
****************************************************'''

from utils import *
import random
import copy
from random import *
from goGameClass import *
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
def alphabeta_search(state):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    
    '''
    Terminates when game.actions is empty
    Class Game needs the following functions:
        - game.result(state, a) -- successor
        - game.actions(state) -- possible moves
        - game.utility -- returns the state of the game (win/lose or tie, when game is terminal)
        
    '''
    #sort state.actions in increasing or decreasing based on max or min (alpha or beta)
    #use heuristics fn to get a value for each move (move is in format (x,y) where x and y are ints
    
    d = 10 #this is the cutoff test depth value. if we exceed this value, stop
    cutoff_test=None
    eval_fn = survivalheur 
                #randnumheuristics 
    player = state.to_move()
    prune = 0
    pruned = {} #this will store the depth of the prune
    totaldepth = [0]
    visited = {}
    
    def max_value(state, alpha, beta, depth):
        branches = len(state.actions())
        onbranch = 0
        
        if totaldepth[0] < depth:
            totaldepth[0] = depth
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        
        #sort state.actions based on heuristics before calling
        #max wants decreasing
        #sorted(state.actions(), key = eval_sort, reverse = True)
        
        #print state.actions()
        for a in state.actions():
            if visited.get(depth) == None:
                visited[depth] = [a]
            else:
                visited[depth].append(a)
            
            onbranch += 1
            v = max(v, min_value(state.result(a),
                                 alpha, beta, depth+1))
            if v >= beta: #pruning happens here, but in branches
                if pruned.get(depth) == None:
                    pruned[depth] = branches - onbranch
                else:
                    pruned[depth] += (branches - onbranch)
                #print "prune", depth, " ", state.actions()
                #state.display()
                return v
            alpha = max(alpha, v)
            
        #print depth, " ", state.actions()
        #state.display()
        
        return v

    def min_value(state, alpha, beta, depth):
        branches = len(state.actions())
        onbranch = 0
        
        if totaldepth[0] < depth:
            totaldepth[0] = depth
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        
        #sort state.actions based on heuristics before calling
        #min wants increasing
        #sorted(state.actions(), key = eval_sort)
        #print state.actions()
        for a in state.actions():
            onbranch += 1
            if visited.get(depth) == None:
                visited[depth] = [a]
            else:
                visited[depth].append(a)
            v = min(v, max_value(state.result(a),
                                 alpha, beta, depth+1))
            if v <= alpha: #pruning happens here, but in branches
                if pruned.get(depth) == None:
                    pruned[depth] = branches - onbranch
                else:
                    pruned[depth] += (branches - onbranch)
                #print "prune", depth, " ", state.actions()
                #state.display()
                return v
            beta = min(beta, v)
        #print depth, " ", state.actions()
        #state.display()
        return v

    # Body of alphabeta_search starts here:
    #def cutoff_test and eval_fn 
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or state.terminal_test()))
    eval_fn = eval_fn or (lambda state: state.utility(player))
    #by default, utility score is used
    
    #argmax goes through all the possible actions and 
    #  applies the alphabeta search onto all of them
    #  and returns the move with the best score 
    #print state.actions()
    abmove = argmax(state.actions(),
                  lambda a: min_value(state.result(a),
                                      -infinity, infinity, 0))
    
    print "*********************************** Tree Depth: ", totaldepth[0], ". (depth: pruned branches)"
    print pruned
    print '************************************ nodes visited: '
    for i in visited:
        print i, ":", len(visited[i])
    
    
    return abmove
      
#query_player asks user for an input of int, int, this is translated
#  to a board move and input into state
def query_player(state):
    #"Make a move by querying standard input."
    state.display()
    print "Please pick the integer corresponding to your selected move: (1 to " + str(len(state.moves)) + ')'
    print ''
    counter = 0
    for i in state.moves:
        counter += 1
        print counter, ": ", i
    print ''
    # convert input to tuple
    while True:
        try:
           input = int(raw_input('Your move? (1 to ' + str(len(state.moves)) + ')'))
        except ValueError: # just catch the exceptions you know!
           print 'That\'s not a number!'
        else:
           if 1 <= input <= len(state.moves): # this is faster
               break
           else:
               print 'Out of range. Try again'
    
    #x = num_or_str(raw_input('Your move?(1 to ' + str(len(state.moves)) + ')'))
    #while ( (not (x >= 1)) or (not(x <= str(len(state.moves))))):
    #    x = num_or_str(raw_input('Please try again between 1 and ' + str(len(state.moves)) + ':'))
    return state.moves[input - 1]

#queries the alphabeta algorithm for a game move
# input is game class object and a state. returns a game move of [int, int]
def alphabeta_player(state):
    return alphabeta_search(state)
        
def play_game(state, *players):
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
    
    #state = generateInitialState(initgame[0], initgame[1], initgame[2], initgame[3])
    
    state.display()
    print "START!"
    
    while True:
        for player in players:
            move = player(state)
            state = state.result(move)
            if state.terminal_test():
                return state.utility(state.to_move())
  
'''''''''''''''''''''''''''''''''
#################################################################
#################################################################

'''''''''''''''''''''''''''''''''

def generateInitialState(attackerPieces, defenderPieces, availableSpots, eyeSpots, dim):
    #inputs:
    #attackerPieces: list of tuples specifying coordinates of all attacker pieces
    #defenderPieces: list of tuples specifying coordinates of all defender pieces
    #availableSpots: list of tuples specifying coordinates of all remaining spots that can be played
    #dim: tuple specifying dimension of the board

    #initial state is never a survivalState
    survivalState = False

    #Define board
    #allSpots: list of tuples specifying the boundary of the board (used to counting liberties)
    allSpots = [(x,y) for x in range(dim[0]) for y in range(dim[1])]
    for i in attackerPieces:
        allSpots.remove(i)
    for j in defenderPieces:
        allSpots.remove(j)
    board = {'Att': attackerPieces, 'Def': defenderPieces, 'Avail': availableSpots, 'All':allSpots, 'EyeSpots': eyeSpots}

    #find connnected pieces and calculate their liberties
    #attacker pieces
    connectedPiecesWithLibAtt = generateConnectedPieces(attackerPieces, board, True)

    #defender pieces
    connectedPiecesWithLibDef = generateConnectedPieces(defenderPieces, board, True)

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

'''''''''''''''''''''''''''''''''
#################################################################
#################################################################

'''''''''''''''''''''''''''''''''

if __name__ == "__main__":
    dpieces0 = [(1,0), (1,2), (1,3), (2,3), (3,0), (3,1), (3,2)]
    apieces0 = [(0,1), (0,3), (0,4), (1,4), (2,4), (3,3), (3,4), (4,0), (4,1), (4,2)]
    avail0 = [(0,0), (0,2), (1,1), (2,0), (2,1), (2,2)]
    dim0 = (6,6)
    game0 = [apieces0, dpieces0, avail0, dim0]
    
    apiecesd1 = [(1,1),(1,2),(1,3),(2,0),(2,2),(3,1),(3,3),(4,3)]
    dpiecesd1 = [(2,3),(2,4),(2,5),(3,2),(3,4),(4,1),(4,2)]
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
    
    eyeSpots = [(x,y) for x in range(3) for y in range(3)]

    gamestate1 = generateInitialState(game0[0], game0[1], game0[2], eyeSpots, game0[3])
    
    play_game(gamestate1, alphabeta_player, query_player)
    #print alphabeta_search(gamestate1)
    
    ''' easy 5 on Tsumego Pro app`'''
    #black
    #dpiecese5 = 
    #white
    #apiecese5 = 
    #dimse5 = (8,6)
    #availse5 = 
    #easy5
    
    '''  '''
    #black
    dpiecestest = [(0,3), (1,0), (1,1), (1,2), (1,3)]
    #white
    apiecestest = [(0,4), (1,4), (2,0), (2,1), (2,2), (2,3), (2,4)]
    dimstest = (3,5)
    availstest = [(0,0), (0,1), (0,2)]
    eyeSpotstest = [(0,0), (0,1), (0,2)]
    gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
    
    gamestatetest = generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
    
    #play_game(gamestatetest, alphabeta_player, query_player)
    '''
    connectedPieces:
    {'Att': [([(1, 1)], [(1, 0), (1, 2), (2, 1)]), 
                ([(2, 2)], [(2, 1), (2, 3), (3, 2), (1, 2)])], 
        'Def': [([(3, 3), (0, 1), (0, 0), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4)], [(3, 2), 
        (4, 3), (2, 3), (1, 0), (1, 2), (1, 3), (0, 5), (1, 5), (2, 5), (3, 5), (4, 4)]), 
        ([(4, 0), (4, 1), (4, 2), (3, 0), (2, 0)], 
        [(5, 0), (5, 1), (3, 1), (4, 3), (5, 2), (3, 2), (2, 1), (1, 0)])]}
    '''
    
    
    
    
    
    
    
    
    
    