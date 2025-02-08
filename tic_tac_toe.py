from tkinter import Tk, Canvas, N, W, E, S
import numpy as np
import time
from sys import argv

class Graphics:
    def __init__(self):
        self.root = Tk()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.bind('<Destroy>', self.destroy)

        self.canvas = Canvas(self.root)
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Configure>', self.save_wh)

        self.w = 0
        self.h = 0

        # Allows for players to register callbacks for when a click happens
        self.click_callbacks = []

        self.board = np.zeros((3,3), dtype=int)

        self.running = True
        self.root.update()

    def destroy(self, event):
        self.running = False

    def save_wh(self, event):
        self.w = event.width
        self.h = event.height
        self.draw()

    def update(self):
        self.root.update()

    def register_click_callback(self, callback):
        self.click_callbacks.append(callback)

    def on_click(self, event):
        sq_w = self.w // 3
        sq_h = self.h // 3
        row = event.y // sq_h
        col = event.x // sq_w
        for f in self.click_callbacks:
            f(row, col)

    def draw(self, board = None):

        if board is not None:
            self.board = board
        else:
            board = self.board

        sq_w = self.w // 3
        sq_h = self.h // 3
        cx = sq_w // 2
        cy = sq_h // 2
        r = min(sq_w, sq_h) * 0.45
        top = cy - r
        left = cx - r
        bottom = cy + r
        right = cx + r
        self.canvas.delete('all')
        self.canvas.create_line(0, sq_h, self.w, sq_h, width=5)
        self.canvas.create_line(0, 2*sq_h, self.w, 2*sq_h, width=5)
        self.canvas.create_line(sq_w, 0, sq_w, self.h, width=5)
        self.canvas.create_line(2*sq_w, 0, 2*sq_w, self.h, width=5)

        for i in range(3):
            for j in range(3):
                val = board[i, j]
                if val == 1:
                    self.canvas.create_line(j*sq_w + left, i*sq_h + top, j*sq_w + right, i*sq_h + bottom, width=5)
                    self.canvas.create_line(j*sq_w + right, i*sq_h + top, j*sq_w + left, i*sq_h + bottom, width=5)
                elif val == -1:
                    self.canvas.create_oval(j*sq_w + left, i*sq_h + top, j*sq_w + right, i*sq_h + bottom, width=5)

        self.root.update()

def has_won(board, player):
    pieces = board == player
    return np.any(np.sum(pieces, axis=0) == 3) or \
           np.any(np.sum(pieces, axis=1) == 3) or \
           (pieces[0,0] and pieces[1,1] and pieces[2,2]) or \
           (pieces[0,2] and pieces[1,1] and pieces[2,0])

def possible_moves(board, player):
    pieces = list(zip(*np.where(board == player)))
    empty = list(zip(*np.where(board == 0)))
    
    if len(pieces) >= 3:
        moves = [
            { 'player': player, 'take': piece, 'put': slot }
            for piece in pieces
            for slot in empty
        ]
    else:
        moves = [
            { 'player': player, 'put': slot }
            for slot in empty
        ]

    return moves

def update_board(board, move):
    board = board.copy()

    if 'take' in move:
        row, col = move['take']
        board[row, col] = 0

    player = move['player']
    row, col = move['put']
    board[row, col] = player

    return board

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.winner = 0
        #self.board = np.random.choice([-1, 0, 1], (3, 3), replace=True)

    def get_board(self):
        return self.board.copy()

    def get_possible_moves(self, player):
        return possible_moves(self.board, player)

    def game_over(self):
        return self.winner != 0

    def reset(self):
        self.board[:,:] = 0
        self.winner = 0

    def make_move(self, move):
        # Move is a dict.
        # Before a player has placed 3 pieces, it is only possible to
        # place a new piece:
        # move = {
        #     'player': 1 or -1,
        #     'put': (row, col)
        # }
        #
        # After placing 3 pieces it is only possible to move a piece:
        # move = {
        #     'player': 1 or -1,
        #     'take': (row, col),
        #     'put': (row, col)
        # }

        if self.winner != 0:
            raise Exception('This game is already over!')

        player = move['player']
        put_row, put_col = move['put']
        num_pieces = np.sum(self.board == player)

        if 'take' in move:
            take_row, take_col = move['take']

            if num_pieces < 3:
                raise Exception('This player has not player 3 pieces yet!')

            val = self.board[take_row, take_col]
            if val == 0:
                raise Exception('Cannot take a piece from an empty slot!')
            if val != player:
                raise Exception('Cannot take a piece from the other player!')

            if take_row == put_row and take_col == put_col:
                raise Exception('Cannot move a marker to the same slot!')

            self.board[take_row, take_col] = 0
        
        elif num_pieces >= 3:
            raise Exception('This player has already played 3 pieces, so they cannot place a new one')

        if self.board[put_row, put_col] != 0:
            raise Exception('Cannot place a piece in a non-empty slot!')

        self.board[put_row, put_col] = player

        if has_won(self.board, player):
            self.winner = player

class HumanPlayer:
    def __init__(self, player, ui):
        self.player = player
        self.pos = None
        self.ui = ui
        ui.register_click_callback(self.click_callback)

    def click_callback(self, row, col):
        self.pos = (row, col)

    def get_click(self):
        self.pos = None
        while self.pos is None: self.ui.update()
        return self.pos

    def move(self, env):

        board = env.get_board()
        pieces = set(zip(*np.where(board == self.player)))
        empty = set(zip(*np.where(board == 0)))

        try:
            move = {
                'player': self.player
            }
            if len(pieces) >= 3:
                pos = self.get_click()
                while pos not in pieces: pos = self.get_click()
                move['take'] = pos

            pos = self.get_click()
            while pos not in empty: pos = self.get_click()
            move['put'] = pos

            env.make_move(move)
        except: pass

class RandomPlayer:
    def __init__(self, player):
        self.player = player

    def move(self, env):
        moves = env.get_possible_moves(self.player)
        move = np.random.choice(moves, 1)[0]
        env.make_move(move)

class AIOutline:
    def __init__(self, player):
        self.player = player

    def move(self, env):
        moves = env.get_possible_moves(self.player)
        scores = [np.random.random() for move in moves] # Replace with AI "magic"
        move = moves[np.argmax(scores)]
        env.make_move(move)

class MiniMax:
    def __init__(self, player):
        self.player = player

    def move(self, env):
        board = env.get_board()
        best_score = -np.inf
        best_move = None
        for move in possible_moves(board, self.player):
            new_board = update_board(board, move)
            score = self.min_player(new_board)
            if score > best_score:
                best_score = score
                best_move = move
        env.make_move(best_move)

    def min_player(self, board):
        if has_won(board, self.player): return 1
        elif has_won(board, -self.player): return -1
        scores = [self.max_player(update_board(board, move)) for move in possible_moves(board, -self.player)]
        return min(scores)

    def max_player(self, board):
        if has_won(board, self.player): return 1
        elif has_won(board, -self.player): return -1
        scores = [self.min_player(update_board(board, move)) for move in possible_moves(board, -self.player)]
        return max(scores)

class EvalMiniMax:
    def __init__(self, player, max_depth=3):
        self.player = player
        self.max_depth = max_depth
        self.piece_scores = np.array([[1, 0, 1],
                                      [0, 2, 0],
                                      [1, 0, 1]])

    def move(self, env):
        board = env.get_board()
        best_score = -np.inf
        best_move = None
        for move in possible_moves(board, self.player):
            score = self.min_player(update_board(board, move), 1)
            if score > best_score:
                best_score = score
                best_move = move
        env.make_move(best_move)

    def min_player(self, board, depth):
        if has_won(board, self.player): return 10
        elif has_won(board, -self.player): return -10
        elif depth == self.max_depth: return np.sum(self.player * board * self.piece_scores)
        scores = [self.max_player(update_board(board, move), depth+1) for move in possible_moves(board, -self.player)]
        return min(scores)

    def max_player(self, board, depth):
        if has_won(board, self.player): return 10
        elif has_won(board, -self.player): return -10
        elif depth == self.max_depth: return np.sum(self.player * board * self.piece_scores)
        scores = [self.min_player(update_board(board, move), depth+1) for move in possible_moves(board, self.player)]
        return max(scores)

class EvalAlphaBeta:
    def __init__(self, player, max_depth=3):
        self.player = player
        self.max_depth = max_depth
        self.piece_scores = np.array([[1, 0, 1],
                                      [0, 2, 0],
                                      [1, 0, 1]])

    def move(self, env):
        board = env.get_board()
        best_score = -np.inf
        best_move = None
        for move in possible_moves(board, self.player):
            score = self.min_player(update_board(board, move), best_score, np.inf, 1)
            if score > best_score:
                best_score = score
                best_move = move
        env.make_move(best_move)

    def min_player(self, board, alpha, beta, depth):
        if has_won(board, self.player): return 10
        elif has_won(board, -self.player): return -10
        elif depth == self.max_depth: return np.sum(self.player * board * self.piece_scores)
        score = np.inf
        for move in possible_moves(board, -self.player):
            score = min(score, self.max_player(update_board(board, move), alpha, beta, depth+1))
            beta = min(beta, score)
            if score <= alpha: break
        return score

    def max_player(self, board, alpha, beta, depth):
        if has_won(board, self.player): return 10
        elif has_won(board, -self.player): return -10
        elif depth == self.max_depth: return np.sum(self.player * board * self.piece_scores)
        score = -np.inf
        for move in possible_moves(board, self.player):
            score = max(score, self.max_player(update_board(board, move), alpha, beta, depth+1))
            alpha = max(alpha, score)
            if score >= beta: break
        return score

class MonteCarlo:
    def __init__(self, player, max_depth=4, n_playouts=20):
        self.player = player
        self.max_depth = max_depth
        self.n_playouts = n_playouts
        self.piece_scores = np.array([[1, 0, 1],
                                      [0, 2, 0],
                                      [1, 0, 1]])

    def move(self, env):
        board = env.get_board()
        moves = possible_moves(board, self.player)
        scores = [self.monte_carlo(update_board(board, move)) for move in moves]
        move = moves[np.argmax(scores)]
        env.make_move(move)

    def monte_carlo(self, board):
        total = 0.0
        for _ in range(self.n_playouts): total += self.playout(board)
        return total / self.n_playouts

    def playout(self, board):
        p = -self.player
        for _ in range(self.max_depth-1):
            if has_won(board, self.player): return 10
            elif has_won(board, -self.player): return -10
            move = np.random.choice(possible_moves(board, p))
            board = update_board(board, move)
            p = -p
        return np.sum(self.player * board * self.piece_scores)

def main():

    n_games = 1

    if len(argv) >= 1:
        try:
            n_games = int(argv[1])
        except: pass

    graphics = Graphics()
    env = TicTacToe()

    n_wins = {
        1: 0,
        -1: 0
    }
    
    #player1 = HumanPlayer(1, graphics)
    #player1 = RandomPlayer(1)
    #player1 = MiniMax(1)
    #player1 = EvalMiniMax(1)
    player1 = EvalAlphaBeta(1)
    #player1 = MonteCarlo(1)

    #player2 = HumanPlayer(-1, graphics)
    #player2 = RandomPlayer(-1)
    #player2 = MiniMax(-1)
    #player2 = EvalMiniMax(-1)
    #player2 = EvalAlphaBeta(-1)
    player2 = MonteCarlo(-1)

    n_played = 0
    for _ in range(n_games):
        env.reset()
        graphics.draw(env.board)
        while True:
            player1.move(env)
            if not graphics.running: break
            graphics.draw(env.board)
            if env.game_over(): break

            player2.move(env)
            if not graphics.running: break
            graphics.draw(env.board)
            if env.game_over(): break

        if isinstance(player1, HumanPlayer) or isinstance(player2, HumanPlayer):
            time.sleep(1)

        if env.winner in n_wins:
            n_wins[env.winner] += 1
            n_played += 1
        if not graphics.running: break

    print('Results:')
    print(f'x won {100.0 * n_wins[1] / n_played}%')
    print(f'o won {100.0 * n_wins[-1] / n_played}%')

    time.sleep(1)

if __name__ == '__main__': main()
