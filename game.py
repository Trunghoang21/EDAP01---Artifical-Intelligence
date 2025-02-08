import math

EMPTY = 0
BLACK = 1
WHITE = 2

# Directions for possible moves (left, right, up, down, and diagonal directions)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


class OthelloGame:
    def __init__(self):
        
        self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
        self.board[3][3], self.board[3][4] = WHITE, BLACK
        self.board[4][3], self.board[4][4] = BLACK, WHITE
        self.current_player = BLACK  # Black goes first
        
        # self.board = [
        #     [WHITE, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
        #     [EMPTY, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, EMPTY],
        #     [WHITE, BLACK, WHITE, BLACK, BLACK, BLACK, BLACK, BLACK],
        #     [WHITE, WHITE, BLACK, BLACK, BLACK, WHITE, BLACK, EMPTY],
        #     [WHITE, WHITE, BLACK, BLACK, BLACK, WHITE, BLACK, BLACK],
        #     [WHITE, WHITE, WHITE, BLACK, BLACK, WHITE, EMPTY, BLACK],
        #     [EMPTY, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK, EMPTY],
        #     [WHITE, WHITE, WHITE, BLACK, BLACK, BLACK, BLACK, EMPTY]
        # ]
        # self.current_player = WHITE 

    def print_board(self):
        """Prints the current board state with indices around it."""
        print("  ", end="")
        for col in range(8):
            print(col, end=" ")
        print()

        for row in range(8):
            print(row, end=" ")
            for col in range(8):
                if self.board[row][col] == EMPTY:
                    print('.', end=" ")
                elif self.board[row][col] == BLACK:
                    print('B', end=" ")
                else:
                    print('W', end=" ")
            print()

    def get_valid_moves(self, player):
        valid_moves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == EMPTY and self.is_valid_move(r, c, player):
                    valid_moves.append((r, c))
        return valid_moves

    def is_valid_move(self, row, col, player):
        if self.board[row][col] != EMPTY:
            return False

        opponent = WHITE if player == BLACK else BLACK

        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            found_opponent = False

            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == opponent:
                    found_opponent = True
                elif self.board[r][c] == player:
                    if found_opponent:
                        return True
                    else:
                        break
                else:
                    break

                r += dr
                c += dc

        return False

    def apply_move(self, row, col, player):
        self.board[row][col] = player

        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            flip_positions = []
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == (WHITE if player == BLACK else BLACK):
                    flip_positions.append((r, c))
                elif self.board[r][c] == player:
                    for flip_r, flip_c in flip_positions:
                        self.board[flip_r][flip_c] = player
                    break
                else:
                    break

                r += dr
                c += dc

    def game_over(self):
        if not self.get_valid_moves(BLACK) and not self.get_valid_moves(WHITE):
            return True
        return False

    def get_winner(self):
        black_score = sum(row.count(BLACK) for row in self.board)
        white_score = sum(row.count(WHITE) for row in self.board)

        if black_score > white_score:
            return BLACK
        elif white_score > black_score:
            return WHITE
        return None


"""This is the Minimax search with Alpha-Beta pruning"""
def minimax(game, depth, alpha, beta, maximizing_player):
    
    if depth == 0 or game.game_over():
        return evaluate_board(game)

    if maximizing_player:
        max_eval = -math.inf
        for row, col in game.get_valid_moves(BLACK):
            new_game = OthelloGame()
            new_game.board = [row.copy() for row in game.board]
            new_game.apply_move(row, col, BLACK)
            eval = minimax(new_game, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for row, col in game.get_valid_moves(WHITE):
            new_game = OthelloGame()
            new_game.board = [row.copy() for row in game.board]
            new_game.apply_move(row, col, WHITE)
            eval = minimax(new_game, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def evaluate_board(game):
    black_score = sum(row.count(BLACK) for row in game.board)
    white_score = sum(row.count(WHITE) for row in game.board)
    return black_score - white_score


"""This is the mthod which get's the best move for the computer player using Minimax with Alpha-Beta pruning"""
def get_best_move(game):
    best_move = None
    max_eval = -math.inf

    for row, col in game.get_valid_moves(BLACK):
        new_game = OthelloGame()
        new_game.board = [row.copy() for row in game.board]
        new_game.apply_move(row, col, BLACK)
        eval = minimax(new_game, 4, -math.inf, math.inf, False)

        if eval > max_eval:
            max_eval = eval
            best_move = (row, col)

    return best_move


def play_othello():
    game = OthelloGame()

    while not game.game_over():
        game.print_board()

        if game.current_player == BLACK:  # Computer's turn (BLACK)
            print("\nComputer's Turn:")
            best_move = get_best_move(game)

            if best_move is None:
                print("Computer has no valid moves. Skipping turn.")
                game.current_player = WHITE
            else:
                row, col = best_move
                print(f"Computer plays: {row}, {col}")
                game.apply_move(row, col, BLACK)
                game.current_player = WHITE
        else:  # Human's turn (WHITE)
            print("\nYour Turn:")
            valid_moves = game.get_valid_moves(WHITE)
            if valid_moves:
                row, col = map(int, input("Enter your move (row, col): ").split())
                if (row, col) in valid_moves:
                    game.apply_move(row, col, WHITE)
                    game.current_player = BLACK
                else:
                    print("Invalid move. Try again.")
            else:
                print("No valid moves. Skipping your turn.")
                game.current_player = BLACK

    game.print_board()
    winner = game.get_winner()

    if winner == BLACK:
        print("\nComputer wins!")
    elif winner == WHITE:
        print("\nYou win!")
    else:
        print("\nIt's a tie!")


if __name__ == "__main__":
    play_othello()
