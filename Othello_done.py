from constants import BOARD_SIZE, EMPTY, BLACK, WHITE, DIRECTIONS
import numpy as np
import random
import copy 
class Othello:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))
        ## initialize the board
        self.board[3][3] = WHITE
        self.board[4][4] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.current_player = BLACK
        self.game_end = False
        self.ai_player = None  # AI player (BLACK or WHITE)
        # change the parameter to True when testing the algorithm. 
        self.auto_player = False


    def print_board(self,valid_moves = []):
        #print the board
        print(f'Valid moves: {valid_moves}')
        print("  ", end="")
        for s in range(BOARD_SIZE):
            print(f"{s} ", end="")
        print()
        for i in range(BOARD_SIZE):
            print(f"{i} ", end="")  # Row label
            for j in range(BOARD_SIZE):
                if self.board[i][j] == EMPTY:
                    if (i, j) in valid_moves:
                        print("* ", end="") # Valid move for the current player
                    else: 
                        print(". ", end="")  # Empty cell
                elif self.board[i][j] == BLACK:
                    print("X ", end="")  # Black piece
                elif self.board[i][j] == WHITE:
                    print("0 ", end="")  # White piece
            print()  # Newline after each row
    
    def game(self):
        user_input = input("choose the 0 for White or X for Black: ")
        if user_input == "0":
            self.current_player = BLACK
            self.ai_player = BLACK
        else:
            self.current_player = BLACK
            self.ai_player = WHITE

        while not self.game_end:
            valid_moves = self.get_valid_moves()
            # check for the end game condition.
            if not valid_moves:
                print(f'No valid moves for the {"White(0)" if self.current_player == WHITE else "Black(X)"} player')
                self.current_player = -self.current_player
                if not self.get_valid_moves():
                    self.game_end = True
                    print("The game ends")
                    continue
            self.print_board(valid_moves)
            
            print(f'{"White(0)" if self.current_player == WHITE else "Black(X)"} player\'s turn')
            if self.current_player == self.ai_player:
                x, y = self.get_best_move()
                print(f"AI chooses: {x}, {y}") 
            else:
                x, y = self.human_input()
                if x is None or y is None:
                    continue
            self.set_dish(x, y)
            self.current_player = -self.current_player
        self.declare_winner()
        self.print_board()

    def declare_winner(self):
        """Declare the winner of the game"""
        black_score = np.sum(self.board == BLACK)
        white_score = np.sum(self.board == WHITE)
    
        print("\nFinal Scores:")
        print(f"Black (X): {black_score}")
        print(f"White (O): {white_score}")
    
        if black_score > white_score:
            print("Black (X) Wins!")
        elif white_score > black_score:
            print("White (O) Wins!")
        else:
            print("It's a Tie!")
        
    
    def is_valid_move(self, row, cow):

        opponent = WHITE if self.current_player == BLACK else BLACK

        for dr, dc in DIRECTIONS:
            r = row + dr 
            c = cow + dc
            found_opponent = False

            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if self.board[r][c] == opponent:
                    found_opponent = True
                elif self.board[r][c] == self.current_player:
                    if found_opponent:
                        return True
                    else:
                        break
                else:
                    break
                r += dr 
                c += dc
        return False
    
    # the function check for valid moves for the current player. 
    def get_valid_moves(self):
        valid_moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == EMPTY and self.is_valid_move(r, c):
                    valid_moves.append((r, c))
        return valid_moves
    
    # set the dish on the board, and flip the opponent's dish
    def set_dish(self, row, col):
        self.board[row][col] = self.current_player
        for dr, dc in DIRECTIONS:
            r = row + dr
            c = col + dc
            flip_positions = []
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if self.board[r][c] == (WHITE if self.current_player == BLACK else BLACK):
                    flip_positions.append((r, c))
                    r += dr
                    c += dc
                elif self.board[r][c] == self.current_player:
                    for flip_r, flip_c in flip_positions:
                        self.board[flip_r][flip_c] = self.current_player
                    break
                else:
                    break
    
    def get_best_move(self):
        """ Return a random move for the AI player"""

        _, best_move = self.minimax(5, float('-inf'), float('inf'), True)
        return best_move
    
    def minimax(self, depth, alpha, beta, maximizing):
        """ Minimax Algorithm with Alpha-Beta Pruning """
        valid_moves = self.get_valid_moves()

        #  Base Case (Stop when depth reaches 0 or no moves left)
        if depth == 0 or not valid_moves:
            return self.evaluate_board(), None

        if maximizing:  #AI's Turn (Maximizing Player)
            best_score = float('-inf')
            best_move = None
            for move in valid_moves:
                game_copy = copy.deepcopy(self)  #Copy the entire game state
                game_copy.set_dish(move[0], move[1])  # Simulate AI move
                game_copy.current_player = - self.current_player  # Switch player
                score, _ = game_copy.minimax(depth - 1, alpha, beta, False)  # Opponent's turn

                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  #Alpha-Beta Pruning 

            return best_score, best_move

        else:  #  Opponent's Turn (Minimizing Player)
            best_score = float('inf')
            best_move = None
            for move in valid_moves:
                game_copy = copy.deepcopy(self)  # Copy game state
                game_copy.set_dish(move[0], move[1])  # Simulate opponent's move
                game_copy.current_player = -self.current_player  # Switch player
                score, _ = game_copy.minimax(depth - 1, alpha, beta, True)  

                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  #Alpha-Beta Pruning

            return best_score, best_move


    def evaluate_board(self):
        """Evaluate the board for the AI player"""
        return np.sum(self.board == self.ai_player) - np.sum(self.board == -self.ai_player)
    

    def human_input(self):
        """ Get the human player's input"""
        valid_moves = self.get_valid_moves()
        if self.auto_player:
            print(f'Valid moves: {valid_moves}')
            x, y = random.choice(valid_moves)
            print(f'Auto player chooses: {x} {y}')
            return x, y
        
        move = input("Enter move (row col) or 'quit' to exit: ")
        if move.lower() == "quit":
            print("Game Over")
            exit()
        try:
            x, y = map(int, move.split())
            if (x, y) not in valid_moves:
                print("Invalid move, try again.")
                return (None, None)
            if not (0 <= x < BOARD_SIZE or 0 <= y < BOARD_SIZE):
                return (None, None)  
            elif self.board[x][y] != EMPTY:
                return (None, None)
        except:
            print("Invalid input, try again.")
            return (None, None)
        return x, y

if __name__ == "__main__":
    game = Othello()
    game.game()