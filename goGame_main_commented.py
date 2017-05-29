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
alphabeta_search: Player player, Game game -> (int, int)
-Takes a GoGame object (state) and using the information, returns the best move through
- alpha beta pruning.
    
tree depth is actually the 'depth' variable + 2
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
    #sort_fn stores sorting heuristics used to prioritize moves that are estimated to be better first
    sort_fn = [vitalpoint, eyeHeur]
    #survivalheur returns a 1 if the input state is a goal state
    eval_fn = survivalheur
    player = state.to_move() #the player whose turn it is to go next
    prune = 0 #stores the number of pruned nodes
    pruned = {} #this will store the depth of the prune
    totaldepth = [0] #stores the deepest level the recursive function reached
    visited = {} #stores the number of visited nodes
    heuristicInd = 0 #index for which sort heuristic to use
    
    '''
    max_value: GoGame, Int, Int, Int, Int
      -'state' is a GoGame object representing the current state of the game board
      -'alpha' is the alpha value used for alpha-beta pruning
      -'beta' is the beta value used for alpha-beta pruning
      -'depth' is an integer that keeps track of the current depth of the alpha beta tree
      -heuristicInd is used to let the program know which heuristic to use. 
        - After one heuristic returns no results, the other will take over
      max_value is called when, on the minmax tree, we want to find the move with the lowest
        score. The successive moves are generated with the function state.successor.
        This recursively calls min_value if we have not yet reached a terminal state
    '''
    def max_value(state, alpha, beta, depth, heuristicInd):
        branches = len(state.actions())
        onbranch = 0
        
        if totaldepth[0] < depth:
            totaldepth[0] = depth
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        
        #sort by vital spots first, returns a list of actions
        tempher = heuristicInd
        
        #sorting heuristic is chosen and sorted here
        sorts = sort_fn[heuristicInd]
        sortedactions, heuristicInd = sorts(state)
        
        #use new sorted list to generate successor functions and call min_value (recursively)
        for a in sortedactions:
            if visited.get(depth) == None:
                visited[depth] = [a]
            else:
                visited[depth].append(a)
            
            onbranch += 1
            v = max(v, min_value(state.result(a),
                                 alpha, beta, depth+1, heuristicInd)) 
            if v >= beta: #pruning happens here
                if pruned.get(depth) == None:
                    pruned[depth] = branches - onbranch
                else:
                    pruned[depth] += (branches - onbranch)
                return v
            alpha = max(alpha, v)
            
        return v
        
    '''
    min_value: GoGame, Int, Int, Int, Int
      -state is a GoGame object representing the current state of the game board
      -alpha is the alpha value used for alpha-beta pruning
      -beta is the beta value used for alpha-beta pruning
      -depth is an integer that keeps track of the current depth of the alpha beta tree
      -heuristicInd is used to let the program know which heuristic to use. 
        - After one heuristic returns no results, the other will take over
      min_value is called when, on the minmax tree, we want to find the move with the lowest
        score. The successive moves are generated with the function state.successor.
        This recursively calls max_value if we have not yet reached a terminal state
    '''
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
        
        #use new sorted list to generate successor functions and call min_value (recursively)
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
    
    #argmax goes through all the possible actions and 
    #  applies the alphabeta search onto all of them
    #  and returns the move with the best score 
    heuristicInd = 0
    sorts = sort_fn[heuristicInd]
    sortedact, heuristicInd = sorts(state)
    #argmax is a fn in the utility.py and is used to call min_value on all of the
    # available moves in state. It would then return the best scoring move
    abmove = argmax(sortedact,
                  lambda a: min_value(state.result(a),
                                      -infinity, infinity, 0, heuristicInd))
                                      
    #print statements to output information on the alpha beta pruning
    print 'problem,', problemno[0], ', total tree depth,', totaldepth[0]
    for i in range(1, len(visited)):
        if (len(pruned) -1 < i):
            pruned[i] = 0
        print i, ",", len(visited[i]), ",", pruned[i]
    
    return abmove
      
# query_play: GoGame -> None
# query_player asks user for an input of int. The user will be presented with several moves
#   each of which is associated with an integer. The user inputs that integer to select that move
#   as their next play.
def query_player(state):
    #displays the current board for visualization before picking a move
    state.display()
    #"Make a move by querying standard input."
    print "Please pick the integer corresponding to your selected move: (1 to " + str(len(state.moves)) + ')'
    print ''
    counter = 0
    #prints available moves for user selection
    for i in state.moves:
        counter += 1
        print counter, ": ", i
    print ''
    # convert input to tuple and return the move to the play_game function
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

#alphabeta_player: GoGame -> (Int, Int)
# queries the alphabeta algorithm for a game move
# returns a game move in the form of a piece coordinate (x,y)
# input is game class object and a state. returns a game move of [int, int]
def alphabeta_player(state):
    return alphabeta_search(state)

#play_game: GoGame, [list of players] -> None
# This function takes a game state and alternates play between the players provided in the input
# Typically, 'alphabeta_player' and 'query_player' are used for *players
#  this represents the AI playing against a human    
def play_game(state, *players):

    #displays the state for visualization
    state.display()
    print "START!"
    moveno = 0
    
    #loops through the players to query their move and plays it into state, generating a successor state
    #The successor state is printed and used to query the players again. This goes on until a 
    # terminal state is reached.
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
    
    
    
    