import numpy as np
import random
import pygame
import sys
import math
import tkinter as tk


# Global Variables

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4
#-----------------------------------------------------------------------------



def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, maximizing_player):
    valid_locations = get_valid_locations(board)
    terminal_node = is_terminal_node(board)

    if depth == 0 or terminal_node:
        if terminal_node:
            if winning_move(board, 2):
                return (None, 100000000000000)
            elif winning_move(board, 1):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, 2))

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 2)
            new_score = minimax(temp_board, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 1)
            new_score = minimax(temp_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

#------------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def minimax_ap(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    terminal_node = is_terminal_node(board)

    if depth == 0 or terminal_node:
        if terminal_node:
            if winning_move(board, 2):
                return (None, 100000000000000)
            elif winning_move(board, 1):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, 2))

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 2)
            new_score = minimax_ap(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 1)
            new_score = minimax_ap(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


# ------------------------------------------------------------------------------


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()
#------------------------------------------------------------------------------------



# Make the Board



board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)



#----------------------------------------------------------------------------------
# player vs minmax alpha pruning

def playeralphapruning(Diff):
    turn = random.randint(PLAYER, AI)
    game_over=False
    if(Diff=="Easy"):
        Difficulty=2
    elif(Diff=="Medium"):
        Difficulty=3
    else:
        Difficulty=5
            
    while not game_over:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
    
            pygame.display.update()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
    
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)
    
                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True
    
                        turn += 1
                        turn = turn % 2
    
                        print_board(board)
                        draw_board(board)
    
        if turn == AI and not game_over:

            # move_start_time = time.time()
    
            col, minimax_score = minimax_ap(board, Difficulty, -math.inf, math.inf, True)
    
            # elapsed_time = time.time() - move_start_time

    
            if is_valid_location(board, col):
                # pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
    
                if winning_move(board, AI_PIECE):
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True
    
                print_board(board)
                draw_board(board)
    
                turn += 1
                turn = turn % 2
    
        if game_over:
            pygame.time.wait(3000)
#----------------------------------------------------------------------------------------------------------
# player vs minmax

def playerminmax(Diff):
    turn = random.randint(PLAYER, AI)
    game_over=False
    if(Diff=="Easy"):
        Difficulty=2
    elif(Diff=="Medium"):
        Difficulty=3
    else:
        Difficulty=5
                
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx=event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
    
            pygame.display.update()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
    
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)
    
                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True
    
                        turn += 1
                        turn = turn % 2
    
                        print_board(board)
                        draw_board(board)
    
        if turn == AI and not game_over:

            # move_start_time=time.time()
            col, minimax_score = minimax(board, Difficulty, True)
            # elapsed_time = time.time() - move_start_time

        
            if is_valid_location(board, col):
                # pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
        
                if winning_move(board, AI_PIECE):
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True
        
                print_board(board)
                draw_board(board)
        
                turn += 1
                turn = turn % 2
        
        if game_over:
            pygame.time.wait(300)

# ----------------------------------------------------------------------------------------------------------------------
# player vs player

def pvp():
    turn = random.randint(PLAYER, AI)
    game_over=False

    while not game_over:
    
    	for event in pygame.event.get():
    		if event.type == pygame.QUIT:
    			sys.exit()
    
    		if event.type == pygame.MOUSEMOTION:
    			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
    			posx = event.pos[0]
    			if turn == 0:
    				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
    			else: 
    				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
    		pygame.display.update()
    
    		if event.type == pygame.MOUSEBUTTONDOWN:
    			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

    			if turn == 0:
    				posx = event.pos[0]
    				col = int(math.floor(posx/SQUARESIZE))
    
    				if is_valid_location(board, col):
    					row = get_next_open_row(board, col)
    					drop_piece(board, row, col, 1)
    
    					if winning_move(board, 1):
    						label = myfont.render("Player 1 wins!!", 1, RED)
    						screen.blit(label, (40,10))
    						game_over = True
    
    
    			else:				
    				posx = event.pos[0]
    				col = int(math.floor(posx/SQUARESIZE))
    
    				if is_valid_location(board, col):
    					row = get_next_open_row(board, col)
    					drop_piece(board, row, col, 2)
    
    					if winning_move(board, 2):
    						label = myfont.render("Player 2 wins!!", 1, YELLOW)
    						screen.blit(label, (40,10))
    						game_over = True
    
    			print_board(board)
    			draw_board(board)
    
    			turn += 1
    			turn = turn % 2
    
    			if game_over:
    				pygame.time.wait(3000)
            
        
#---------------------------------------------------------------------------------------------------- 
# minmax vs minmax

def minmax_vs_minmax(diff1,diff2):
    turn = random.randint(PLAYER, AI)
    game_over=False    
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
        if turn == PLAYER:
            #move_start_time = time.time()
            if diff1=="Easy":
                col, minimax_score = minimax(board, 1, True)
            elif diff1 == "Medium":
                col, minimax_score = minimax(board, 3, True)
            elif diff1 == "Hard":
                col, minimax_score = minimax(board, 5, True)
    
               # elapsed_time = time.time() - move_start_time
        else:
            #move_start_time = time.time()
            #minimax_scores_g.append(elapsed_time)
            if diff2=="Easy":
                col, minimax_score = minimax(board, 1, False)
            elif diff2 == "Medium":
                col, minimax_score = minimax(board, 3, False)
            elif diff2 == "Hard":
                col, minimax_score = minimax(board, 5, False)
                    
        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, turn+1 )
    
            if winning_move(board, turn + 1):
                label = myfont.render(f"AI {turn+1 } wins!", 1, YELLOW if turn == AI else RED)
                screen.blit(label, (40, 10))
                game_over = True
            elif is_terminal_node(board):  # Check for a draw
                label = myfont.render("Draw!", 1, YELLOW if turn == AI else RED)
                screen.blit(label, (150, 10))
                game_over = True
    
            print_board(board)
            draw_board(board)
    
            turn += 1
            turn %= 2
    
        if game_over:
            pygame.time.wait(3000)                
                
#------------------------------------------------------------------------------------------
# minmax Alpha Pruning vs minmax Alpha Pruning 


def minmaxap_vs_minmaxap(diff1,diff2):
    turn = random.randint(PLAYER, AI)
    game_over=False    
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
        if turn == PLAYER:
            #move_start_time = time.time()
            if diff1=="Easy":
                col, minimax_score = minimax_ap(board, -math.inf, math.inf, 1, True)
            elif diff1 == "Medium":
                col, minimax_score = minimax_ap(board, -math.inf, math.inf, 3, True)
            elif diff1 == "Hard":
                col, minimax_score = minimax_ap(board, -math.inf, math.inf, 5, True)
    
               # elapsed_time = time.time() - move_start_time
        else:
            #move_start_time = time.time()
            #minimax_scores_g.append(elapsed_time)
            if diff2=="Easy":
                col, minimax_score = minimax_ap(board,-math.inf, math.inf,  1, False)
            elif diff2 == "Medium":
                col, minimax_score = minimax_ap(board, -math.inf, math.inf, 3, False)
            elif diff2 == "Hard":
                col, minimax_score = minimax_ap(board, -math.inf, math.inf, 5, False)
                    
        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, turn+1 )
    
            if winning_move(board, turn + 1):
                label = myfont.render(f"AI {turn+1 } wins!", 1, YELLOW if turn == AI else RED)
                screen.blit(label, (40, 10))
                game_over = True
            elif is_terminal_node(board):  # Check for a draw
                label = myfont.render("Draw!", 1, YELLOW if turn == AI else RED)
                screen.blit(label, (150, 10))
                game_over = True
    
            print_board(board)
            draw_board(board)
    
            turn += 1
            turn %= 2
    
        if game_over:
            pygame.time.wait(3000)                
                
#------------------------------------------------------------------------------------------
# minmax  vs minmax Alpha Pruning 


def minmax_vs_minmaxap(diff1,diff2):
    turn = random.randint(PLAYER, AI)
    game_over=False    
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
        if turn == PLAYER:
            #move_start_time = time.time()
            if diff1=="Easy":
                col, minimax_score = minimax(board, 1, True)
            elif diff1 == "Medium":
                col, minimax_score = minimax(board, 3, True)
            elif diff1 == "Hard":
                col, minimax_score = minimax(board, 5, True)
    
               # elapsed_time = time.time() - move_start_time
        else:
            #move_start_time = time.time()
            #minimax_scores_g.append(elapsed_time)
            if diff2=="Easy":
                col, minimax_score = minimax_ap(board, 1, -math.inf, math.inf, False)
            elif diff2 == "Medium":
                col, minimax_score = minimax_ap(board, 3, -math.inf, math.inf, False)
            elif diff2 == "Hard":
                col, minimax_score = minimax_ap(board, 5, -math.inf, math.inf, False)
                    
        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, turn+1 )
    
            if winning_move(board, turn + 1):
                label = myfont.render(f"AI {turn+1 } wins!", 1, YELLOW if turn == AI else RED)
                screen.blit(label, (40, 10))
                game_over = True
            elif is_terminal_node(board):  # Check for a draw
                label = myfont.render("Draw!", 1, YELLOW if turn == AI else RED)
                screen.blit(label, (150, 10))
                game_over = True
    
            print_board(board)
            draw_board(board)
    
            turn += 1
            turn %= 2
    
        if game_over:
           pygame.time.wait(300)      

#----------------------------------------------------------------------------------------

# main menu

import tkinter as tk

# def start_game():
#     algorithm = algorithm_var.get()
#     difficulty = difficulty_var.get()
#     run_game(algorithm, difficulty)


def player_vs_minmax_Alpha_pruning_call():
    game_options_window = tk.Toplevel(window)
    game_options_window.title("Game Options")



    difficulty_label = tk.Label(game_options_window, text="Ai Difficulty:")
    difficulty_label.pack()

    difficulty_var = tk.StringVar(value="Easy")
    difficulty_option1 = tk.Radiobutton(game_options_window, text="Easy", variable=difficulty_var, value="Easy")
    difficulty_option2 = tk.Radiobutton(game_options_window, text="Medium", variable=difficulty_var, value="Medium")
    difficulty_option3 = tk.Radiobutton(game_options_window, text="Hard", variable=difficulty_var, value="Hard")
    difficulty_option1.pack()
    difficulty_option2.pack()
    difficulty_option3.pack()
    
    
    start_button = tk.Button(game_options_window, text="Start Game",command=lambda: playeralphapruning(difficulty_var.get()))
    start_button.pack()





def player_vs_minmax_call():
    game_options_window = tk.Toplevel(window)
    game_options_window.title("Game Options")
    difficulty_label = tk.Label(game_options_window, text="Ai Difficulty:")
    difficulty_label.pack()

    difficulty_var = tk.StringVar(value="Easy")
    difficulty_option1 = tk.Radiobutton(game_options_window, text="Easy", variable=difficulty_var, value="Easy")
    difficulty_option2 = tk.Radiobutton(game_options_window, text="Medium", variable=difficulty_var, value="Medium")
    difficulty_option3 = tk.Radiobutton(game_options_window, text="Hard", variable=difficulty_var, value="Hard")
    difficulty_option1.pack()
    difficulty_option2.pack()
    difficulty_option3.pack()
    # Start button
    start_button = tk.Button(game_options_window, text="Start Game",command=lambda: playerminmax(difficulty_var.get()))
    start_button.pack()


def Player_vs_Player_call():
    pvp()

def minmax_vs_minmax_call():
    game_options_window = tk.Toplevel(window)
    game_options_window.title("Game Options")
    difficulty_label = tk.Label(game_options_window, text="minmax_1 Difficulty:")
    difficulty_label.pack()

    difficulty_var_1 = tk.StringVar(value="Easy")
    difficulty1_option1 = tk.Radiobutton(game_options_window, text="Easy", variable=difficulty_var_1, value="Easy")
    difficulty1_option2 = tk.Radiobutton(game_options_window, text="Medium", variable=difficulty_var_1, value="Medium")
    difficulty1_option3 = tk.Radiobutton(game_options_window, text="Hard", variable=difficulty_var_1, value="Hard")
    difficulty1_option1.pack()
    difficulty1_option2.pack()
    difficulty1_option3.pack()
    # Start butt
    
    difficulty_label = tk.Label(game_options_window, text="minmax_2 Difficulty:")
    difficulty_label.pack()

    difficulty_var_2 = tk.StringVar(value="Easy")
    difficulty2_option1 = tk.Radiobutton(game_options_window, text="Easy", variable=difficulty_var_2, value="Easy")
    difficulty2_option2 = tk.Radiobutton(game_options_window, text="Medium", variable=difficulty_var_2, value="Medium")
    difficulty2_option3 = tk.Radiobutton(game_options_window, text="Hard", variable=difficulty_var_2, value="Hard")
    difficulty2_option1.pack()
    difficulty2_option2.pack()
    difficulty2_option3.pack()
    # Start button
    start_button = tk.Button(game_options_window, text="Start Game",command=lambda: minmax_vs_minmax(difficulty_var_1.get(),difficulty_var_2.get()))
    start_button.pack()



def minmaxap_vs_minmaxap_call():
    game_options_window = tk.Toplevel(window)
    game_options_window.title("Game Options")
    difficulty_label = tk.Label(game_options_window, text="minmaxAP_1 Difficulty:")
    difficulty_label.pack()

    difficulty_var_1 = tk.StringVar(value="Easy")
    difficulty1_option1 = tk.Radiobutton(game_options_window, text="Easy", variable=difficulty_var_1, value="Easy")
    difficulty1_option2 = tk.Radiobutton(game_options_window, text="Medium", variable=difficulty_var_1, value="Medium")
    difficulty1_option3 = tk.Radiobutton(game_options_window, text="Hard", variable=difficulty_var_1, value="Hard")
    difficulty1_option1.pack()
    difficulty1_option2.pack()
    difficulty1_option3.pack()
    # Start butt
    
    difficulty_label = tk.Label(game_options_window, text="minmaxAP_2 Difficulty:")
    difficulty_label.pack()

    difficulty_var_2 = tk.StringVar(value="Easy")
    difficulty2_option1 = tk.Radiobutton(game_options_window, text="Easy", variable=difficulty_var_2, value="Easy")
    difficulty2_option2 = tk.Radiobutton(game_options_window, text="Medium", variable=difficulty_var_2, value="Medium")
    difficulty2_option3 = tk.Radiobutton(game_options_window, text="Hard", variable=difficulty_var_2, value="Hard")
    difficulty2_option1.pack()
    difficulty2_option2.pack()
    difficulty2_option3.pack()
    # Start button
    start_button = tk.Button(game_options_window, text="Start Game",command=lambda: minmaxap_vs_minmaxap(difficulty_var_1.get(),difficulty_var_2.get()))
    start_button.pack()



def minmax_vs_minmaxap_call():
    game_options_window = tk.Toplevel(window)
    game_options_window.title("Game Options")
    difficulty_label = tk.Label(game_options_window, text="minmax Difficulty:")
    difficulty_label.pack()

    difficulty_var_1 = tk.StringVar(value="Easy")
    difficulty1_option1 = tk.Radiobutton(game_options_window, text="Easy", variable=difficulty_var_1, value="Easy")
    difficulty1_option2 = tk.Radiobutton(game_options_window, text="Medium", variable=difficulty_var_1, value="Medium")
    difficulty1_option3 = tk.Radiobutton(game_options_window, text="Hard", variable=difficulty_var_1, value="Hard")
    difficulty1_option1.pack()
    difficulty1_option2.pack()
    difficulty1_option3.pack()
    # Start butt
    
    difficulty_label = tk.Label(game_options_window, text="minmaxAP Difficulty:")
    difficulty_label.pack()

    difficulty_var_2 = tk.StringVar(value="Easy")
    difficulty2_option1 = tk.Radiobutton(game_options_window, text="Easy", variable=difficulty_var_2, value="Easy")
    difficulty2_option2 = tk.Radiobutton(game_options_window, text="Medium", variable=difficulty_var_2, value="Medium")
    difficulty2_option3 = tk.Radiobutton(game_options_window, text="Hard", variable=difficulty_var_2, value="Hard")
    difficulty2_option1.pack()
    difficulty2_option2.pack()
    difficulty2_option3.pack()
    # Start button
    start_button = tk.Button(game_options_window, text="Start Game",command=lambda: minmax_vs_minmaxap(difficulty_var_1.get(),difficulty_var_2.get()))
    start_button.pack()





# Create the main window
window = tk.Tk()
window.title("Game Modes")

button_font = ("Arial", 12)  
window.geometry("500x400")
button_style = {
    "font": button_font,
    "bg": "#4CAF50",
    "fg": "white",   
    "relief": tk.RAISED,
    "borderwidth": 2,
    "width": 20,
    "height": 2
}

ai_vs_ai_button = tk.Button(window, text="player vs minmax_AP", command=player_vs_minmax_Alpha_pruning_call , **button_style)
ai_vs_ai_button.pack()

ai_vs_player_button = tk.Button(window, text="player vs minmax", command=player_vs_minmax_call, **button_style)
ai_vs_player_button.pack()

player_vs_player_button = tk.Button(window, text="Player vs Player", command=Player_vs_Player_call, **button_style)
player_vs_player_button.pack()

player_vs_player_button = tk.Button(window, text="minmax vs minmax", command=minmax_vs_minmax_call, **button_style)
player_vs_player_button.pack()

player_vs_player_button = tk.Button(window, text="minmax_AP vs minmax_AP", command=minmaxap_vs_minmaxap_call, **button_style)
player_vs_player_button.pack()

player_vs_player_button = tk.Button(window, text="minmax vs minmax_AP", command=minmax_vs_minmaxap_call, **button_style)
player_vs_player_button.pack()

window.mainloop()
