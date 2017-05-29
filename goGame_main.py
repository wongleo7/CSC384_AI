'''****************************************************
GO - Life or Death

CSC384 Final Project

Team Members:  
- Shayne Lin 
- Leo Wong

Main function used to call alpha-beta search, query players, play game,
and contains the main function.

Other files include goGameClass.py and problems.py

goGameClass contains the go game class and functionality for the game
problems.py contains a huge selection of Tsumego problems for the AI to solve
problems are mostly from the mobile app 'Tsumego Pro' (link in documentation)
****************************************************'''

from utils import *
import random
import copy
from random import *
from goGameClass import *
import problems as ps
import timeit
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

#tree depth is actually +2 
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
    d = depthset[0] #this is the cutoff test depth value. if we exceed this value, stop
    cutoff_test=None
    sort_fn = [vitalpoint, eyeHeur]
    eval_fn = survivalheur 
    player = state.to_move()
    prune = 0
    pruned = {} #this will store the depth of the prune
    totaldepth = [0]
    visited = {}
    heuristicInd = 0
    
    def max_value(state, alpha, beta, depth, heuristicInd):
        branches = len(state.actions())
        onbranch = 0
        
        if totaldepth[0] < depth:
            totaldepth[0] = depth
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        
        #sort by vital spots first, returns a list of actions
        # for sorts in sort_fn:
        tempher = heuristicInd

        sorts = sort_fn[heuristicInd]
        sortedactions, heuristicInd = sorts(state)
        
        for a in sortedactions:
            if visited.get(depth) == None:
                visited[depth] = [a]
            else:
                visited[depth].append(a)
            
            onbranch += 1
            v = max(v, min_value(state.result(a),
                                 alpha, beta, depth+1, heuristicInd)) 
            if v >= beta: #pruning happens here, but in branches
                if pruned.get(depth) == None:
                    pruned[depth] = branches - onbranch
                else:
                    pruned[depth] += (branches - onbranch)
                return v
            alpha = max(alpha, v)
            
        return v

    def min_value(state, alpha, beta, depth, heuristicInd):
        branches = len(state.actions())
        onbranch = 0
        
        if totaldepth[0] < depth:
            totaldepth[0] = depth
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        
        #sort state.actions based on heuristics before calling
        #min wants increasing
        tempher = heuristicInd
        sorts = sort_fn[heuristicInd]
        sortedactions, heuristicInd = sorts(state, 1)
        for a in sortedactions: 
            onbranch += 1
            if visited.get(depth) == None:
                visited[depth] = [a]
            else:
                visited[depth].append(a)
            v = min(v, max_value(state.result(a),
                                 alpha, beta, depth+1, heuristicInd))
            if v <= alpha: #pruning happens here, but in branches
                if pruned.get(depth) == None:
                    pruned[depth] = branches - onbranch
                else:
                    pruned[depth] += (branches - onbranch)
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or state.terminal_test()))
    eval_fn = eval_fn or (lambda state: state.utility(player))
    #by default, utility score is used
    
    #argmax goes through all the possible actions and 
    #  applies the alphabeta search onto all of them
    #  and returns the move with the best score 
    heuristicInd = 0
    sorts = sort_fn[heuristicInd]
    sortedact, heuristicInd = sorts(state)
    abmove = argmax(sortedact,
                  lambda a: min_value(state.result(a),
                                      -infinity, infinity, 0, heuristicInd))

    print 'problem,', problemno[0], ', total tree depth,', totaldepth[0]
    for i in range(1, len(visited)):
        if (len(pruned) -1 < i):
            pruned[i] = 0
        print i, ",", len(visited[i]), ",", pruned[i]
    
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
                Loops through manual input and player AI_1
    '''
    
    #state = generateInitialState(initgame[0], initgame[1], initgame[2], initgame[3])
    
    state.display()
    print "START!"
    moveno = 0
    
    while True:
        for player in players:
            depthset[0] = depthset[0] - 1
            moveno += 1
            print 'Move Number,', moveno
            start_time = timeit.default_timer()
            move = player(state)
            elapsed = timeit.default_timer() - start_time
            print 'Time elapsed,', elapsed
            print ''
            state = state.result(move)
            if state.terminal_test():
                state.display()
                return state
  
'''''''''''''''''''''''''''''''''
Code below is used to generate initial state for initializing a game object
A lot of computational heavy things are done to generate the board and encode
the moves. A lot of information is also generated and stored for later
analysis purposes.
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
    eyes = determinEyes(board)
    #create a GoGame object
    initialState = GoGame(player, moves, board, connectedPieces, survivalState, eyes)
    return initialState

'''''''''''''''''''''''''''''''''
Main part of the program calls playgame function after the game and search depth
is selected. Higher depth provides more accurate results but takes longer to solve.
An overly higher depth would not always return a favorable result, usually between 4-10 is
a good range depending on the problem. An IDS implementation would solve this dependency. 

'''''''''''''''''''''''''''''''''

if __name__ == "__main__":
    input = int(raw_input('Which game would you like to play? (0 to 15)'))
    problemno = [input]
    gamestate1 = ps.getProblems(problemno[0])
    input = int(raw_input('Depth?'))
    depthset = [input]
    final_state = play_game(gamestate1, alphabeta_player, query_player)
    print('Final State')
    final_state.display()
    
    
    
    