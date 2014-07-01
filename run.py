"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import gui

import game_board as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 100    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
#Players are PLAYERX and PLAYERO.
def mc_trial(board, player):
    """
    This function runs a single random 
    trial with the game board.
    """
    
    while board.check_win() == None:
        empty = board.get_empty_squares()
        choice = random.choice(empty)
        board.move(choice[0], choice[1], player)
        
        if player == 2:
            player = 3
        else:
            player = 2
    
    return None

def mc_update_scores(scores, board, player):
    """
    This function updates the scoreboard
    based on which moves worked and which
    didn't.
    """
    
    winner = board.check_win()
    if winner == 4: # if it's a draw, don't score
        return None
    
    for row in range(0,board.get_dim()):
        for col in range(0,board.get_dim()):
            position = board.square(row, col)
            
            if position == 2: # player x, or computer
                if winner == 2:
                    scores[row][col] += MCMATCH
                else:
                    scores[row][col] -= MCMATCH
            elif position == 3: #player o, or other
                if winner == 3:
                    scores[row][col] += MCOTHER
                else:
                    scores[row][col] -= MCOTHER
            
                
def get_best_move(board, scores):
    """
    This function picks the best move 
    from a list of possible choices.
    """
    empty = board.get_empty_squares()
    choose = []
    
    max_score = None

    for tile in range(0, len(empty)):
        row = empty[tile][0]
        col = empty[tile][1]
        
        if scores[row][col] > max_score:
            choose = []
            choose.append((empty[tile][0], empty[tile][1]))
            max_score = scores[row][col]
        
        if scores[row][col] == max_score:
            choose.append((empty[tile][0], empty[tile][1]))
    
    return random.choice(choose)

    
def mc_move(board, player, trials):
    """
    When this function is called, 
    it submits the machine's move.
    """
    scores = [[0 for dummy_row in range(0, board.get_dim())] for dummy_col in range(0, board.get_dim())]
    for dummy_trial in range(0, trials):
        
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
    
    move = get_best_move(board, scores)
    
    return (move[0], move[1])


#provided.play_game(mc_move, NTRIALS, False)        
gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
