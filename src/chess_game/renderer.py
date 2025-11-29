"""Rendering and UI components for Chess Game."""

import pygame
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from chess_game.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_SIZE, SQUARE_SIZE,
    COLORS, FONT_SIZES, PIECE_SIZE, PIECE_SIZE_SMALL, PAWN_SIZE,
    PIECE_IMAGES, PIECE_ORDER, LEGACY_IMAGES_DIR, IMAGES_DIR,
    STATUS_MESSAGES, PROMOTION_PIECES, GameState
)
from chess_game.pieces import Piece, PieceType, PieceColor


class Renderer:
    """Handles all rendering for the chess game."""
    
    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize the renderer."""
        self.screen = screen
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.piece_images: Dict[str, pygame.Surface] = {}
        self.piece_images_small: Dict[str, pygame.Surface] = {}
        self._init_fonts()
        self._load_images()
        self.flash_counter = 0
    
    def _init_fonts(self) -> None:
        """Initialize fonts for rendering."""
        for name, size in FONT_SIZES.items():
            self.fonts[name] = pygame.font.Font('freesansbold.ttf', size)
    
    def _load_images(self) -> None:
        """Load piece images from assets."""
        # Try new assets directory first, fall back to legacy
        image_dirs = [IMAGES_DIR, LEGACY_IMAGES_DIR]
        
        for color in ["white", "black"]:
            for piece_type in PieceType:
                key = f"{color}_{piece_type.value}"
                image_name = PIECE_IMAGES.get(key)
                
                if not image_name:
                    continue
                
                # Try each directory
                for img_dir in image_dirs:
                    image_path = img_dir / image_name
                    if image_path.exists():
                        try:
                            image = pygame.image.load(str(image_path))
                            
                            # Determine size based on piece type
                            if piece_type == PieceType.PAWN:
                                size = PAWN_SIZE
                            else:
                                size = PIECE_SIZE
                            
                            self.piece_images[key] = pygame.transform.scale(
                                image, (size, size)
                            )
                            self.piece_images_small[key] = pygame.transform.scale(
                                image, (PIECE_SIZE_SMALL, PIECE_SIZE_SMALL)
                            )
                            break
                        except pygame.error as e:
                            print(f"Warning: Could not load image {image_path}: {e}")
    
    def update_flash(self) -> None:
        """Update the flash counter for animations."""
        self.flash_counter = (self.flash_counter + 1) % 30
    
    def draw_board(self) -> None:
        """Draw the chess board."""
        for row in range(8):
            for col in range(8):
                # Alternate colors
                if (row + col) % 2 == 0:
                    color = COLORS["light_square"]
                else:
                    color = COLORS["dark_square"]
                
                pygame.draw.rect(
                    self.screen, color,
                    [col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE]
                )
        
        # Draw grid lines
        for i in range(9):
            pygame.draw.line(
                self.screen, COLORS["black"],
                (0, i * SQUARE_SIZE), (BOARD_SIZE, i * SQUARE_SIZE), 2
            )
            pygame.draw.line(
                self.screen, COLORS["black"],
                (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, BOARD_SIZE), 2
            )
    
    def draw_status_bar(self, game_state: int, current_color: PieceColor) -> None:
        """Draw the status bar at the bottom."""
        # Background
        pygame.draw.rect(
            self.screen, COLORS["dark_gray"],
            [0, BOARD_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT - BOARD_SIZE]
        )
        pygame.draw.rect(
            self.screen, COLORS["gold"],
            [0, BOARD_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT - BOARD_SIZE], 5
        )
        
        # Side panel
        pygame.draw.rect(
            self.screen, COLORS["gold"],
            [BOARD_SIZE, 0, WINDOW_WIDTH - BOARD_SIZE, BOARD_SIZE], 5
        )
        
        # Status message
        message = STATUS_MESSAGES.get(game_state, "")
        text = self.fonts["large"].render(message, True, COLORS["black"])
        self.screen.blit(text, (20, BOARD_SIZE + 20))
        
        # Forfeit button
        forfeit_text = self.fonts["medium"].render("FORFEIT", True, COLORS["black"])
        self.screen.blit(forfeit_text, (BOARD_SIZE + 10, BOARD_SIZE + 30))
    
    def draw_piece(self, piece: Piece, selected: bool = False) -> None:
        """Draw a single piece on the board."""
        key = f"{piece.color.value}_{piece.piece_type.value}"
        image = self.piece_images.get(key)
        
        if image:
            x = piece.x * SQUARE_SIZE
            y = piece.y * SQUARE_SIZE
            
            # Center the piece in the square
            offset_x = (SQUARE_SIZE - image.get_width()) // 2
            offset_y = (SQUARE_SIZE - image.get_height()) // 2
            
            self.screen.blit(image, (x + offset_x, y + offset_y))
        
        if selected:
            color = COLORS["highlight_white"] if piece.color == PieceColor.WHITE else COLORS["highlight_black"]
            pygame.draw.rect(
                self.screen, color,
                [piece.x * SQUARE_SIZE + 1, piece.y * SQUARE_SIZE + 1, 
                 SQUARE_SIZE - 2, SQUARE_SIZE - 2], 3
            )
    
    def draw_pieces(
        self, pieces: List[Piece], selected_piece: Optional[Piece] = None
    ) -> None:
        """Draw all pieces on the board."""
        for piece in pieces:
            is_selected = selected_piece == piece
            self.draw_piece(piece, selected=is_selected)
    
    def draw_valid_moves(
        self, moves: List[Tuple[int, int]], 
        pieces: List[Piece],
        current_color: PieceColor
    ) -> None:
        """Draw indicators for valid moves."""
        enemy_positions = {p.position for p in pieces if p.color != current_color}
        
        for move in moves:
            x = move[0] * SQUARE_SIZE + SQUARE_SIZE // 2
            y = move[1] * SQUARE_SIZE + SQUARE_SIZE // 2
            
            if move in enemy_positions:
                # Capture indicator (red ring)
                pygame.draw.circle(
                    self.screen, COLORS["capture_move"], (x, y), 
                    SQUARE_SIZE // 2 - 5, 4
                )
            else:
                # Move indicator (green dot)
                pygame.draw.circle(
                    self.screen, COLORS["valid_move"], (x, y), 10
                )
    
    def draw_captured_pieces(
        self, 
        captured_white: List[Piece], 
        captured_black: List[Piece]
    ) -> None:
        """Draw captured pieces on the side panel."""
        # Captured by white (black pieces)
        for i, piece in enumerate(captured_white):
            key = f"{piece.color.value}_{piece.piece_type.value}"
            image = self.piece_images_small.get(key)
            if image:
                col = i % 4
                row = i // 4
                self.screen.blit(
                    image, 
                    (BOARD_SIZE + 10 + col * 45, 10 + row * 45)
                )
        
        # Captured by black (white pieces)
        offset_y = 400  # Start lower for black's captures
        for i, piece in enumerate(captured_black):
            key = f"{piece.color.value}_{piece.piece_type.value}"
            image = self.piece_images_small.get(key)
            if image:
                col = i % 4
                row = i // 4
                self.screen.blit(
                    image, 
                    (BOARD_SIZE + 10 + col * 45, offset_y + row * 45)
                )
    
    def draw_check_indicator(
        self, 
        king: Optional[Piece], 
        is_in_check: bool
    ) -> None:
        """Draw a flashing indicator when king is in check."""
        if not king or not is_in_check:
            return
        
        if self.flash_counter < 15:
            color = COLORS["dark_red"] if king.color == PieceColor.WHITE else COLORS["dark_blue"]
            pygame.draw.rect(
                self.screen, color,
                [king.x * SQUARE_SIZE + 1, king.y * SQUARE_SIZE + 1,
                 SQUARE_SIZE - 2, SQUARE_SIZE - 2], 5
            )
    
    def draw_game_over(self, winner: str, reason: str = "checkmate") -> None:
        """Draw the game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(COLORS["black"])
        overlay.set_alpha(150)
        self.screen.blit(overlay, (0, 0))
        
        # Game over box
        box_width, box_height = 450, 150
        box_x = (BOARD_SIZE - box_width) // 2
        box_y = (BOARD_SIZE - box_height) // 2
        
        pygame.draw.rect(
            self.screen, COLORS["black"],
            [box_x, box_y, box_width, box_height]
        )
        pygame.draw.rect(
            self.screen, COLORS["gold"],
            [box_x, box_y, box_width, box_height], 3
        )
        
        # Winner text
        winner_text = self.fonts["large"].render(
            f"{winner} wins!", True, COLORS["white"]
        )
        text_x = box_x + (box_width - winner_text.get_width()) // 2
        self.screen.blit(winner_text, (text_x, box_y + 20))
        
        # Reason text
        reason_text = self.fonts["small"].render(
            f"by {reason}", True, COLORS["light_gray"]
        )
        text_x = box_x + (box_width - reason_text.get_width()) // 2
        self.screen.blit(reason_text, (text_x, box_y + 70))
        
        # Restart instruction
        restart_text = self.fonts["small"].render(
            "Press ENTER to restart", True, COLORS["white"]
        )
        text_x = box_x + (box_width - restart_text.get_width()) // 2
        self.screen.blit(restart_text, (text_x, box_y + 110))
    
    def draw_promotion_dialog(
        self, color: PieceColor, position: Tuple[int, int]
    ) -> List[Tuple[pygame.Rect, PieceType]]:
        """Draw pawn promotion selection dialog and return clickable areas."""
        # Dialog background
        dialog_width = len(PROMOTION_PIECES) * 100 + 20
        dialog_x = (BOARD_SIZE - dialog_width) // 2
        dialog_y = BOARD_SIZE // 2 - 60
        
        pygame.draw.rect(
            self.screen, COLORS["black"],
            [dialog_x, dialog_y, dialog_width, 120]
        )
        pygame.draw.rect(
            self.screen, COLORS["gold"],
            [dialog_x, dialog_y, dialog_width, 120], 3
        )
        
        # Title
        title = self.fonts["small"].render("Choose promotion piece:", True, COLORS["white"])
        self.screen.blit(title, (dialog_x + 10, dialog_y + 5))
        
        # Piece options
        clickable_areas = []
        for i, piece_name in enumerate(PROMOTION_PIECES):
            piece_type = PieceType(piece_name)
            key = f"{color.value}_{piece_name}"
            image = self.piece_images.get(key)
            
            piece_x = dialog_x + 20 + i * 100
            piece_y = dialog_y + 35
            
            rect = pygame.Rect(piece_x, piece_y, PIECE_SIZE, PIECE_SIZE)
            clickable_areas.append((rect, piece_type))
            
            # Highlight on hover
            mouse_pos = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, COLORS["gold"], rect, 2)
            
            if image:
                self.screen.blit(image, (piece_x, piece_y))
        
        return clickable_areas
    
    def draw_move_history(
        self, moves: List[str], 
        x: int = BOARD_SIZE + 10, 
        y: int = 250
    ) -> None:
        """Draw the move history on the side panel."""
        title = self.fonts["small"].render("Move History:", True, COLORS["black"])
        self.screen.blit(title, (x, y))
        
        # Show last 10 moves
        display_moves = moves[-10:] if len(moves) > 10 else moves
        for i, move in enumerate(display_moves):
            move_text = self.fonts["small"].render(
                f"{len(moves) - len(display_moves) + i + 1}. {move}", 
                True, COLORS["black"]
            )
            self.screen.blit(move_text, (x, y + 25 + i * 20))
