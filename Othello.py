from constants import BOARD_SIZE, EMPTY, BLACK, WHITE, DIRECTIONS
import numpy as np

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


    def print_board(self,valid_moves = []):
        #print the board
        print(valid_moves)
        print("  ", end="")
        for s in range(BOARD_SIZE):
            print(f"{s+1} ", end="")
        print()
        for i in range(BOARD_SIZE):
            print(f"{i+1} ", end="")  # Row label
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
            self.current_player = WHITE
        else:
            self.current_player = BLACK

        while not self.game_end:
            valid_moves = self.get_valid_moves()
            self.print_board(valid_moves)
            print(f'{"White(0)" if self.current_player == WHITE else "Black(X)"} player\'s turn')
            move = input("Enter the move: ")
            if move == "quit":
                print("Game Over")
                print("--------------")
                break

            try:
                x, y = map(int, move.split())
                x = x -1;  y = y -1
                if (x, y) not in valid_moves:
                    print("You must choose a valid move")
                    print("--------------")
                    continue

            except: 
                print("Invalid Move, choose again")
                print("-----------------")
                continue
        
            if not self.check_input(x, y):
                print("Invalid Move, choose again")
                print("-----------------")
                continue
            self.set_dish(x, y)
            self.current_player = -self.current_player

    def check_input(self, x, y):
        if not (0 <= x < BOARD_SIZE or 0 <= y < BOARD_SIZE):
            return False  
        elif self.board[x][y] != EMPTY:
            return False
        return True
    
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
                

if __name__ == "__main__":
    game = Othello()
    game.game()