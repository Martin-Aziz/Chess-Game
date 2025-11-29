"""Configuration constants for the Chess Game."""

from pathlib import Path
from typing import Dict, Tuple, List

# Window configuration
WINDOW_WIDTH: int = 1000
WINDOW_HEIGHT: int = 900
BOARD_SIZE: int = 800
SQUARE_SIZE: int = 100
FPS: int = 60

# Colors (RGB tuples)
COLORS: Dict[str, Tuple[int, int, int]] = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "light_square": (240, 217, 181),  # Classic light wood
    "dark_square": (181, 136, 99),     # Classic dark wood
    "light_gray": (211, 211, 211),
    "dark_gray": (128, 128, 128),
    "gold": (255, 215, 0),
    "blue": (0, 0, 255),
    "green": (0, 128, 0),
    "red": (255, 0, 0),
    "dark_red": (139, 0, 0),
    "dark_blue": (0, 0, 139),
    "highlight_white": (100, 100, 255),
    "highlight_black": (100, 255, 100),
    "valid_move": (0, 200, 0),
    "capture_move": (200, 0, 0),
    "check_warning": (255, 100, 100),
}

# Font configuration
FONT_SIZES: Dict[str, int] = {
    "small": 20,
    "medium": 40,
    "large": 50,
}

# Piece configuration
PIECE_SIZE: int = 80
PIECE_SIZE_SMALL: int = 45
PAWN_SIZE: int = 65

# Asset paths (relative to package)
PACKAGE_DIR: Path = Path(__file__).parent
ASSETS_DIR: Path = PACKAGE_DIR / "assets"
IMAGES_DIR: Path = ASSETS_DIR / "images"
SOUNDS_DIR: Path = ASSETS_DIR / "sounds"

# Legacy images directory (for backward compatibility)
LEGACY_IMAGES_DIR: Path = Path(__file__).parent.parent.parent.parent / "Chess Game with Pygames" / "images"

# Piece image mapping (standardized names)
PIECE_IMAGES: Dict[str, str] = {
    "white_king": "king.png",
    "white_queen": "white queen.png",
    "white_rook": "rock.png",
    "white_bishop": "bishop.png",
    "white_knight": "knight.png",
    "white_pawn": "pawn.png",
    "black_king": "black king.png",
    "black_queen": "black Queen.png",
    "black_rook": "rock black.png",
    "black_bishop": "bishop black.png",
    "black_knight": "knight black.png",
    "black_pawn": "pawn black.png",
}

# Initial board setup
INITIAL_WHITE_PIECES: List[str] = [
    'rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'
]

INITIAL_WHITE_POSITIONS: List[Tuple[int, int]] = [
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)
]

INITIAL_BLACK_PIECES: List[str] = [
    'rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'
]

INITIAL_BLACK_POSITIONS: List[Tuple[int, int]] = [
    (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)
]

# Game state constants
class GameState:
    """Enumeration for game states."""
    WHITE_SELECT = 0
    WHITE_MOVE = 1
    BLACK_SELECT = 2
    BLACK_MOVE = 3
    GAME_OVER = 4
    PAWN_PROMOTION = 5

# Status messages
STATUS_MESSAGES: Dict[int, str] = {
    GameState.WHITE_SELECT: "White: Select a Piece to Move!",
    GameState.WHITE_MOVE: "White: Select a Destination!",
    GameState.BLACK_SELECT: "Black: Select a Piece to Move!",
    GameState.BLACK_MOVE: "Black: Select a Destination!",
    GameState.GAME_OVER: "Game Over!",
    GameState.PAWN_PROMOTION: "Select a piece for promotion!",
}

# Promotion pieces
PROMOTION_PIECES: List[str] = ['queen', 'rook', 'bishop', 'knight']

# Piece ordering for display
PIECE_ORDER: List[str] = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
