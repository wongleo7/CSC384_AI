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
    cutoff_test=None
    eval_fn = None 
    player = game.to_move(state)
    
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in actions_list:
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
    # this just runs min_value over the game legal moves and returns the result
    # if tie, returns first of the list
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
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
    def __init__(self, attackpieces, defendpieces, boardwidth = 3, boardheight = 3):
        '''
            initialize all state variables here
        '''
        self.initial = Struct(player='w', moves, liberty = 0, board={}, connectedpieces)
    
    def actions(self, state):
        ''' returns the allowable moves, this is predefined???? '''
        return state.moves
    
    '''successor fn********************************************************************************'''
    def result(self, state, move):
        ''' successor function, takes a move and returns a state '''
        
    def utility(self, state, player):
        "Return the value of this final state to player."
        '''  print the board        '''
        display(self, state)
    
    '''terminal test********************************************************************************'''
    def terminal_test(self, state):
        '''checks if actions is empty. if it is empty, then we are terminal. 
        or if .................'''
        if self.actions(self, state):
            return false
        else:
            return true
        '''alternatively, 'return self.actions(self, state)' '''

    '''returns a player'''
    def to_move(self, state):
        "Return the player whose move it is in this state."
        return if_(state == 'b', 'w', 'b')

    def display(self, state):
        "Print or otherwise display the state."
        for i in self.gameBoard:
            print(i)

    def __repr__(self):
    
class connectedPieces:

'''    Variables: 
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
    

class play_go(game, *players):
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
    state = game.initial
    while True:
        for player in players:

class Player:
'''
    Variables:
        
    Function:
        Search: same as calc_move basically..
        calc_move: (Class Game) -> (int x, int y)
            - Using the heuristics and search tree in this class
                Player calculates their next best move
                And outputs an (Int x, Int y) representing their next move
                          

'''










