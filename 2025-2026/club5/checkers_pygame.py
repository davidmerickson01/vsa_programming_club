import pygame
import sys

# chatgpt prompt
# create a Checkers game using pygame and python. it should have two
# players that take turns. each player should make two choices: which
# piece to move and where to move it too. if you make a wrong move,
# it should disallow it. it should have a counter that shows the
# number of moves, and a status bar that declares a winner. it should
# also include a different graphic for regular pieces and for kings

pygame.init()

# Constants
WIDTH, HEIGHT = 640, 720
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (180, 180, 180)
GOLD = (255, 215, 0)

FONT = pygame.font.SysFont(None, 28)
BIG_FONT = pygame.font.SysFont(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

# --------------------------------------------------

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def draw(self):
        x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 2 - 8

        pygame.draw.circle(screen, self.color, (x, y), radius)

        if self.king:
            pygame.draw.circle(screen, GOLD, (x, y), radius - 8, 4)

# --------------------------------------------------

class Board:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row][col] = Piece(row, col, RED)
                    elif row > 4:
                        self.board[row][col] = Piece(row, col, BLUE)

    def draw(self):
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else GRAY
                pygame.draw.rect(
                    screen,
                    color,
                    (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                )

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    piece.draw()

    def move(self, piece, row, col):
        self.board[piece.row][piece.col] = None
        piece.row, piece.col = row, col
        self.board[row][col] = piece

        if piece.color == RED and row == ROWS - 1:
            piece.king = True
        if piece.color == BLUE and row == 0:
            piece.king = True

    def remove(self, piece):
        self.board[piece.row][piece.col] = None

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_all_pieces(self, color):
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    pieces.append(piece)
        return pieces

# --------------------------------------------------

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = RED
        self.selected = None
        self.valid_moves = {}
        self.move_count = 0
        self.winner = None

    def draw_status(self):
        pygame.draw.rect(screen, BLACK, (0, WIDTH, WIDTH, 80))

        if self.winner:
            text = BIG_FONT.render(f"{'Red' if self.winner == RED else 'Blue'} Wins!", True, WHITE)
        else:
            text = FONT.render(
                f"Turn: {'Red' if self.turn == RED else 'Blue'} | Moves: {self.move_count}",
                True,
                WHITE,
            )

        screen.blit(text, (20, WIDTH + 25))

    def select(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected:
            if (row, col) in self.valid_moves:
                self.board.move(self.selected, row, col)
                captured = self.valid_moves[(row, col)]
                if captured:
                    self.board.remove(captured)
                self.change_turn()
                self.move_count += 1
            self.selected = None
            self.valid_moves = {}
        else:
            if piece and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.get_valid_moves(piece)

    def get_valid_moves(self, piece):
        moves = {}
        directions = []

        if piece.color == RED or piece.king:
            directions.append((1, -1))
            directions.append((1, 1))
        if piece.color == BLUE or piece.king:
            directions.append((-1, -1))
            directions.append((-1, 1))

        for dr, dc in directions:
            r, c = piece.row + dr, piece.col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if self.board.get_piece(r, c) is None:
                    moves[(r, c)] = None
                else:
                    jump_r, jump_c = r + dr, c + dc
                    if (
                        0 <= jump_r < ROWS
                        and 0 <= jump_c < COLS
                        and self.board.get_piece(jump_r, jump_c) is None
                        and self.board.get_piece(r, c).color != piece.color
                    ):
                        moves[(jump_r, jump_c)] = self.board.get_piece(r, c)

        return moves

    def change_turn(self):
        self.turn = BLUE if self.turn == RED else RED
        self.check_winner()

    def check_winner(self):
        if not self.board.get_all_pieces(RED):
            self.winner = BLUE
        elif not self.board.get_all_pieces(BLUE):
            self.winner = RED

# --------------------------------------------------

def get_row_col(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def main():
    clock = pygame.time.Clock()
    game = Game()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game.winner:
                row, col = get_row_col(pygame.mouse.get_pos())
                if row < ROWS:
                    game.select(row, col)

        game.board.draw()
        game.draw_status()
        pygame.display.flip()

if __name__ == "__main__":
    main()
