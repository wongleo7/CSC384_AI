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
    
    eval_fn = None ''' enter fn name here '''
    player = game.to_move(state)
    heuristics_fn = None
    '''
    Terminates when game.actions is empty
    Class Game needs the following functions:
        - game.result(state, a) -- successor
        - game.actions(state) -- possible moves
        - game.utility -- returns the state of the game (win/lose or tie, when game is terminal)
        
    '''
    '''
        We apply the heuristics function to every game.actions list on max_value or min_value
    '''
    def max_value(state, alpha, beta, depth):
        v = -infinity
        actions_list = heuristics_fn(game.actions(state))
        for a in actions_list:
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # this just runs min_value over the game legal moves and returns the result
    # if tie, returns first of the list
    eval_fn = (lambda state: game.utility(state, player))
    return argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a),
                                      -infinity, infinity, 0))

'''
Class Game:
    Variables: 
        connectedPiecesList: List of (Connected Pieces (white)) 
        gameBoard: (Array of (Array of Int))
        possible_moves: (Array of (array of Int x, Int y)) 
        
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
Class connectedPieces:
    Variables: 
        Int numpieces,
        Int Color (0 white, 1 black),
        Int breathingspots,
        (Array of (Array of Int)) positions,
        
    Functions:
        count_breathing_spot: null -> boolean
            - updates the count of the breathing spots for this
            - connected pieces object
            - Returns boolean depending on success (?)
        merge: (Class connectedPieces) -> connectedPieces
            - Takes another connectedPIeces object
            - and returns a connectedPieces object that
              combined both of the pieces (this and the input)
           
'''

'''
Class play_go:
    Variables:
        Player one
        Player two
        Game game
        
    Function:
        Play_game: null -> null, output to std_io
            1. Checks if everything is initialized
                - Game baord needs to be initialized and
                - Player needs to be initialized (at least 1)
            2. Loops through player AI_1 and AI_2 or
                Loops through input and player AI_1
            *. If player is null, then look for player input instead
'''

'''
Class Player:
    Variables:
        
    Function:
        Search: same as calc_move basically..
        calc_move: (Class Game) -> (int x, int y)
            - Using the heuristics and search tree in this class
                Player calculates their next best move
                And outputs an (Int x, Int y) representing their next move
                          

'''

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
        abstract

    def result(self, state, move):
        "Return the state that results from making a move from a state."
        abstract

    def utility(self, state, player):
        "Return the value of this final state to player."
        abstract

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.actions(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print state

    def __repr__(self):
        return '<%s>' % self.__class__.__name__










