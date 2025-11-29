"""Main game logic and loop for Chess Game."""

import pygame
import sys
from typing import Optional, Tuple, List

from chess_game.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_SIZE, SQUARE_SIZE, FPS, GameState
)
from chess_game.board import Board
from chess_game.pieces import Piece, PieceType, PieceColor
from chess_game.renderer import Renderer


class ChessGame:
    """Main chess game class."""
    
    def __init__(self) -> None:
        """Initialize the chess game."""
        pygame.init()
        
        self.screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        pygame.display.set_caption("Chess Game")
        
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.renderer = Renderer(self.screen)
        
        # Game state
        self.game_state = GameState.WHITE_SELECT
        self.current_color = PieceColor.WHITE
        self.selected_piece: Optional[Piece] = None
        self.valid_moves: List[Tuple[int, int]] = []
        self.game_over = False
        self.winner: Optional[str] = None
        self.game_over_reason = ""
        
        # Promotion state
        self.promotion_pending = False
        self.promotion_piece: Optional[Piece] = None
        self.promotion_position: Optional[Tuple[int, int]] = None
        
        self.running = True
    
    def reset(self) -> None:
        """Reset the game to initial state."""
        self.board.reset()
        self.game_state = GameState.WHITE_SELECT
        self.current_color = PieceColor.WHITE
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False
        self.winner = None
        self.game_over_reason = ""
        self.promotion_pending = False
        self.promotion_piece = None
        self.promotion_position = None
    
    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle mouse click events."""
        x, y = pos
        
        # Check for forfeit button
        if x >= BOARD_SIZE and y >= BOARD_SIZE:
            self._handle_forfeit()
            return
        
        # Ignore clicks outside the board
        if x >= BOARD_SIZE or y >= BOARD_SIZE:
            return
        
        # Convert to board coordinates
        board_x = x // SQUARE_SIZE
        board_y = y // SQUARE_SIZE
        click_pos = (board_x, board_y)
        
        # Handle based on game state
        if self.game_state in (GameState.WHITE_SELECT, GameState.BLACK_SELECT):
            self._handle_piece_selection(click_pos)
        elif self.game_state in (GameState.WHITE_MOVE, GameState.BLACK_MOVE):
            self._handle_move_selection(click_pos)
    
    def _handle_piece_selection(self, pos: Tuple[int, int]) -> None:
        """Handle piece selection."""
        piece = self.board.get_piece_at(pos)
        
        if piece and piece.color == self.current_color:
            self.selected_piece = piece
            self.valid_moves = self.board.get_legal_moves(piece)
            
            if self.current_color == PieceColor.WHITE:
                self.game_state = GameState.WHITE_MOVE
            else:
                self.game_state = GameState.BLACK_MOVE
    
    def _handle_move_selection(self, pos: Tuple[int, int]) -> None:
        """Handle move destination selection."""
        if pos in self.valid_moves and self.selected_piece:
            # Check if this is a pawn promotion
            promotion_row = 7 if self.current_color == PieceColor.WHITE else 0
            if self.selected_piece.is_pawn() and pos[1] == promotion_row:
                self.promotion_pending = True
                self.promotion_piece = self.selected_piece
                self.promotion_position = pos
                self.game_state = GameState.PAWN_PROMOTION
                return
            
            # Execute the move
            self._execute_move(pos)
        else:
            # Check if clicking on another piece of same color
            piece = self.board.get_piece_at(pos)
            if piece and piece.color == self.current_color:
                self.selected_piece = piece
                self.valid_moves = self.board.get_legal_moves(piece)
            else:
                # Deselect
                self.selected_piece = None
                self.valid_moves = []
                if self.current_color == PieceColor.WHITE:
                    self.game_state = GameState.WHITE_SELECT
                else:
                    self.game_state = GameState.BLACK_SELECT
    
    def _execute_move(
        self, pos: Tuple[int, int], 
        promotion_type: Optional[PieceType] = None
    ) -> None:
        """Execute a move and update game state."""
        if not self.selected_piece:
            return
        
        # Make the move
        self.board.make_move(self.selected_piece, pos, promotion_type)
        
        # Check for checkmate/stalemate
        opponent = self.current_color.opposite()
        
        if self.board.is_checkmate(opponent):
            self.game_over = True
            self.winner = self.current_color.value.capitalize()
            self.game_over_reason = "checkmate"
        elif self.board.is_stalemate(opponent):
            self.game_over = True
            self.winner = "Draw"
            self.game_over_reason = "stalemate"
        
        # Switch turns
        self.current_color = opponent
        self.selected_piece = None
        self.valid_moves = []
        
        if self.current_color == PieceColor.WHITE:
            self.game_state = GameState.WHITE_SELECT
        else:
            self.game_state = GameState.BLACK_SELECT
    
    def _handle_forfeit(self) -> None:
        """Handle forfeit button click."""
        self.game_over = True
        self.winner = self.current_color.opposite().value.capitalize()
        self.game_over_reason = "forfeit"
    
    def handle_promotion_click(self, pos: Tuple[int, int]) -> None:
        """Handle click during pawn promotion."""
        # Get the clickable areas from the renderer
        areas = self.renderer.draw_promotion_dialog(
            self.current_color, 
            self.promotion_position or (0, 0)
        )
        
        for rect, piece_type in areas:
            if rect.collidepoint(pos):
                self._execute_move(self.promotion_position or (0, 0), piece_type)
                self.promotion_pending = False
                self.promotion_piece = None
                self.promotion_position = None
                break
    
    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_over:
                    continue
                
                if self.promotion_pending:
                    self.handle_promotion_click(event.pos)
                else:
                    self.handle_click(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.game_over:
                    self.reset()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_u:  # Undo
                    if not self.game_over:
                        move = self.board.undo_last_move()
                        if move:
                            self.current_color = move.piece.color
                            self.selected_piece = None
                            self.valid_moves = []
                            if self.current_color == PieceColor.WHITE:
                                self.game_state = GameState.WHITE_SELECT
                            else:
                                self.game_state = GameState.BLACK_SELECT
    
    def render(self) -> None:
        """Render the game."""
        self.screen.fill((0, 0, 0))
        
        # Draw board
        self.renderer.draw_board()
        
        # Draw pieces
        self.renderer.draw_pieces(self.board.pieces, self.selected_piece)
        
        # Draw valid moves
        if self.valid_moves and not self.promotion_pending:
            self.renderer.draw_valid_moves(
                self.valid_moves, 
                self.board.pieces,
                self.current_color
            )
        
        # Draw captured pieces
        self.renderer.draw_captured_pieces(
            self.board.captured_white,
            self.board.captured_black
        )
        
        # Draw check indicator
        king = self.board.get_king(self.current_color)
        is_in_check = self.board.is_in_check(self.current_color)
        self.renderer.draw_check_indicator(king, is_in_check)
        
        # Draw status bar
        self.renderer.draw_status_bar(self.game_state, self.current_color)
        
        # Draw move history
        move_strings = [str(m) for m in self.board.move_history]
        self.renderer.draw_move_history(move_strings)
        
        # Draw promotion dialog if needed
        if self.promotion_pending and self.promotion_position:
            self.renderer.draw_promotion_dialog(
                self.current_color, 
                self.promotion_position
            )
        
        # Draw game over screen
        if self.game_over and self.winner:
            self.renderer.draw_game_over(self.winner, self.game_over_reason)
        
        # Update display
        pygame.display.flip()
    
    def run(self) -> None:
        """Run the main game loop."""
        while self.running:
            self.clock.tick(FPS)
            self.renderer.update_flash()
            
            self.handle_events()
            self.render()
        
        pygame.quit()


def main() -> None:
    """Entry point for the chess game."""
    game = ChessGame()
    game.run()


if __name__ == "__main__":
    main()
