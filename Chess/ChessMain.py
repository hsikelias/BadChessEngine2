import pygame as p
import os
import sys
import ChessEngine

# initializes pygame mixer
p.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
p.mixer.init()
p.init()

# board settings
BOARD_SIZE = 640
WINDOW_WIDTH = BOARD_SIZE
WINDOW_HEIGHT = BOARD_SIZE

DIMENSION = 8
SQ_SIZE = BOARD_SIZE // DIMENSION
MAX_FPS = 60


COLORS = {
    'light_square': p.Color("#f0d9b4"),
    'dark_square': p.Color("#b58863"),
    'light_highlight': p.Color("#ffff7f"),
    'dark_highlight': p.Color("#ffdd7f"),
    'last_move_light': p.Color("#cdd26a"),
    'last_move_dark': p.Color("#aaa23a"),
    'check_square': p.Color("#ff6b6b"),
    'valid_move': p.Color("#00aa00"),
}

IMAGES = {}
SOUNDS = {}


class SimpleChess:

    def __init__(self):
        self.screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        p.display.set_caption("Simple Chess")
        self.clock = p.time.Clock()

        # Game state
        self.gs = ChessEngine.GameState()
        self.valid_moves = self.gs.getValidMoves()
        self.move_made = False

        # UI state
        self.sq_selected = ()
        self.player_clicks = []
        self.last_move = None
        self.show_valid_moves = True
        self.board_flipped = False

        # Load resources
        self.load_images()
        self.load_sounds()

    def load_images(self):
        """Load piece images with fallbacks"""
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']

        for piece in pieces:
            try:
                img_path = os.path.join("images", f"{piece}.png")
                if os.path.exists(img_path):
                    IMAGES[piece] = p.transform.scale(p.image.load(img_path), (SQ_SIZE, SQ_SIZE))
                else:
                    self.create_piece(piece)
            except Exception:
                self.create_piece(piece)

    def create_piece(self, piece):
        """Create simple piece graphics"""
        surf = p.Surface((SQ_SIZE, SQ_SIZE), p.SRCALPHA)

        if piece[0] == 'w':
            main_color = p.Color("#ffffff")
            border_color = p.Color("#cccccc")
        else:
            main_color = p.Color("#2c2c2c")
            border_color = p.Color("#1a1a1a")

        center = SQ_SIZE // 2

        # Draw based on piece type
        if piece[1] == 'p':  # Pawn
            points = [(center, center - 15), (center - 8, center + 15), (center + 8, center + 15)]
            p.draw.polygon(surf, main_color, points)
            p.draw.polygon(surf, border_color, points, 2)
            p.draw.circle(surf, main_color, (center, center - 10), 8)
            p.draw.circle(surf, border_color, (center, center - 10), 8, 2)

        elif piece[1] == 'K':  # King
            p.draw.circle(surf, main_color, (center, center), 18)
            p.draw.circle(surf, border_color, (center, center), 18, 3)
            crown_points = [(center - 12, center - 12), (center - 6, center - 20),
                           (center, center - 15), (center + 6, center - 20), (center + 12, center - 12)]
            p.draw.polygon(surf, main_color, crown_points)
            p.draw.polygon(surf, border_color, crown_points, 2)

        elif piece[1] == 'Q':  # Queen
            p.draw.circle(surf, main_color, (center, center), 16)
            p.draw.circle(surf, border_color, (center, center), 16, 3)
            for i in range(5):
                angle = (i * 72 - 90) * 3.14159 / 180
                x = center + int(12 * p.math.cos(angle))
                y = center - 5 + int(12 * p.math.sin(angle))
                p.draw.circle(surf, main_color, (x, y), 3)

        elif piece[1] == 'R':  # Rook
            rect = p.Rect(center - 12, center - 8, 24, 16)
            p.draw.rect(surf, main_color, rect)
            p.draw.rect(surf, border_color, rect, 2)
            for i in range(3):
                x = center - 8 + i * 8
                p.draw.rect(surf, main_color, (x, center - 15, 4, 7))

        elif piece[1] == 'B':  # Bishop
            p.draw.circle(surf, main_color, (center, center), 14)
            p.draw.circle(surf, border_color, (center, center), 14, 2)
            points = [(center - 8, center - 8), (center, center - 18), (center + 8, center - 8)]
            p.draw.polygon(surf, main_color, points)
            p.draw.polygon(surf, border_color, points, 2)

        elif piece[1] == 'N':  # Knight
            p.draw.circle(surf, main_color, (center, center), 15)
            p.draw.circle(surf, border_color, (center, center), 15, 2)
            p.draw.circle(surf, main_color, (center - 8, center - 8), 4)
            p.draw.circle(surf, main_color, (center + 8, center - 8), 4)

        # Add piece letter
        font = p.font.Font(None, 24)
        text = font.render(piece[1], True, border_color)
        text_rect = text.get_rect(center=(center, center + 5))
        surf.blit(text, text_rect)

        IMAGES[piece] = surf

    def load_sounds(self):
        """Load sound effects"""
        sound_files = {
            'move': 'move.wav',
            'capture': 'capture.wav',
            'check': 'check.wav',
            'checkmate': 'checkmate.wav',
            'castle': 'castle.wav',
            'promotion': 'promotion.wav',
        }

        for sound_name, filename in sound_files.items():
            try:
                sound_path = os.path.join("sounds", filename)
                if os.path.exists(sound_path):
                    SOUNDS[sound_name] = p.mixer.Sound(sound_path)
            except Exception:
                pass

    def handle_events(self):
        """Handle pygame events"""
        for event in p.event.get():
            if event.type == p.QUIT:
                return False

            elif event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_click(event.pos)

            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:  # Z key for undo
                    self.undo_move()
                elif event.key == p.K_n:  # N key for new game
                    self.new_game()
                elif event.key == p.K_f:  # F key to flip board
                    self.flip_board()

        return True

    def handle_click(self, pos):
        """Handle mouse clicks on board"""
        col = pos[0] // SQ_SIZE
        row = pos[1] // SQ_SIZE

        # Handle board flipping
        if self.board_flipped:
            row = 7 - row
            col = 7 - col

        if 0 <= row < 8 and 0 <= col < 8:
            if self.sq_selected == (row, col):
                # Deselect if clicking same square
                self.sq_selected = ()
                self.player_clicks = []
            else:
                self.sq_selected = (row, col)
                self.player_clicks.append(self.sq_selected)

            if len(self.player_clicks) == 2:
                self.attempt_move()

    def attempt_move(self):
        """Try to make a move"""
        if len(self.player_clicks) == 2:
            start_sq, end_sq = self.player_clicks[0], self.player_clicks[1]
            piece_moved = self.gs.board[start_sq[0]][start_sq[1]]

            # Check for castling
            if piece_moved[1] == 'K' and abs(end_sq[1] - start_sq[1]) == 2:
                for move in self.valid_moves:
                    if move.isCastleMove and move.startRow == start_sq[0] and move.startCol == start_sq[1] and move.endRow == end_sq[0] and move.endCol == end_sq[1]:
                        self.make_move(move)
                        return

            # All other moves
            move = ChessEngine.Move(start_sq, end_sq, self.gs.board)
            for valid_move in self.valid_moves:
                if move == valid_move:
                    self.make_move(valid_move)
                    return

            # Invalid move - keep second click as selection
            self.player_clicks = [self.sq_selected]

    def make_move(self, move):
        """Execute a move"""
        self.gs.makeMove(move)
        self.last_move = move
        self.move_made = True
        self.sq_selected = ()
        self.player_clicks = []
        self.play_sound(move)

    def play_sound(self, move):
        """Play appropriate sound for move"""
        if self.gs.checkMate:
            sound = SOUNDS.get('checkmate')
        elif self.gs.inCheck():
            sound = SOUNDS.get('check')
        elif move.isCastleMove:
            sound = SOUNDS.get('castle')
        elif move.isPawnPromotion:
            sound = SOUNDS.get('promotion')
        elif move.pieceCaptured != '--':
            sound = SOUNDS.get('capture')
        else:
            sound = SOUNDS.get('move')

        if sound:
            sound.play()

    def undo_move(self):
        """Undo last move"""
        if self.gs.moveLog:
            self.gs.undoMove()
            self.move_made = True
            self.sq_selected = ()
            self.player_clicks = []
            self.last_move = self.gs.moveLog[-1] if self.gs.moveLog else None

    def flip_board(self):
        """Flip board orientation"""
        self.board_flipped = not self.board_flipped
        self.sq_selected = ()
        self.player_clicks = []
        print(f"Board flipped - {'Black' if self.board_flipped else 'White'} perspective")

    def new_game(self):
        """Start new game"""
        self.gs = ChessEngine.GameState()
        self.valid_moves = self.gs.getValidMoves()
        self.sq_selected = ()
        self.player_clicks = []
        self.last_move = None
        self.move_made = True

    def draw_board(self):
        """Draw the chess board"""
        for row in range(8):
            for col in range(8):
                # Handle board flipping for display
                display_row = 7 - row if self.board_flipped else row
                display_col = 7 - col if self.board_flipped else col

                # Base square color
                is_light = (display_row + display_col) % 2 == 0
                base_color = COLORS['light_square'] if is_light else COLORS['dark_square']

                # Highlight colors (using actual board coordinates)
                square_pos = (row, col)
                if (self.last_move and
                    (square_pos == (self.last_move.startRow, self.last_move.startCol) or
                     square_pos == (self.last_move.endRow, self.last_move.endCol))):
                    color = COLORS['last_move_light'] if is_light else COLORS['last_move_dark']
                elif self.sq_selected == square_pos:
                    color = COLORS['light_highlight'] if is_light else COLORS['dark_highlight']
                elif (self.gs.inCheck() and
                      square_pos == (self.gs.whiteKingLocation if self.gs.whiteToMove else self.gs.blackKingLocation)):
                    color = COLORS['check_square']
                else:
                    color = base_color

                # Draw square (using display coordinates)
                rect = p.Rect(display_col * SQ_SIZE, display_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                p.draw.rect(self.screen, color, rect)

    def draw_pieces(self):
        """Draw chess pieces"""
        for row in range(8):
            for col in range(8):
                piece = self.gs.board[row][col]
                if piece != "--":
                    # Handle board flipping for piece display
                    display_row = 7 - row if self.board_flipped else row
                    display_col = 7 - col if self.board_flipped else col

                    piece_rect = p.Rect(display_col * SQ_SIZE, display_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                    self.screen.blit(IMAGES[piece], piece_rect)

    def draw_highlights(self):
        """Draw valid move indicators"""
        if not self.show_valid_moves or not self.sq_selected:
            return

        for move in self.valid_moves:
            if (move.startRow == self.sq_selected[0] and
                move.startCol == self.sq_selected[1]):

                # Handle board flipping for move highlights
                display_row = 7 - move.endRow if self.board_flipped else move.endRow
                display_col = 7 - move.endCol if self.board_flipped else move.endCol

                center_x = display_col * SQ_SIZE + SQ_SIZE // 2
                center_y = display_row * SQ_SIZE + SQ_SIZE // 2

                if move.pieceCaptured != "--":
                    # Capture indicator - ring
                    p.draw.circle(self.screen, COLORS['valid_move'],
                                (center_x, center_y), SQ_SIZE // 2 - 3, 4)
                else:
                    # Regular move - dot
                    p.draw.circle(self.screen, COLORS['valid_move'],
                                (center_x, center_y), 8)

    def draw_everything(self):
        """Draw complete game state"""
        self.screen.fill(p.Color("#312e2b"))
        self.draw_board()
        self.draw_pieces()
        self.draw_highlights()

    def run(self):
        """Main game loop"""
        running = True
        print("Simple Chess started!")
        print("Controls: Click to move pieces, Z to undo, N for new game, F to flip board")

        while running:
            running = self.handle_events()

            if self.move_made:
                self.valid_moves = self.gs.getValidMoves()
                self.move_made = False

                # Print game status
                if self.gs.checkMate:
                    winner = "Black" if self.gs.whiteToMove else "White"
                    print(f"Checkmate! {winner} wins!")
                elif self.gs.staleMate:
                    print("Stalemate!")
                elif self.gs.inCheck():
                    print("Check!")

            self.draw_everything()
            self.clock.tick(MAX_FPS)
            p.display.flip()

        p.quit()
        sys.exit()


def main():
    """Main function"""
    os.makedirs("images", exist_ok=True)
    os.makedirs("sounds", exist_ok=True)

    game = SimpleChess()
    game.run()


if __name__ == "__main__":
    main()