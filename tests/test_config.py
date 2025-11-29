"""Tests for chess game configuration."""

import pytest
from chess_game.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_SIZE, SQUARE_SIZE, FPS,
    COLORS, FONT_SIZES, PIECE_SIZE, PIECE_ORDER, GameState,
    STATUS_MESSAGES, PROMOTION_PIECES
)


class TestWindowConfig:
    """Tests for window configuration."""
    
    def test_window_dimensions(self) -> None:
        """Test window dimensions are reasonable."""
        assert WINDOW_WIDTH >= 800
        assert WINDOW_HEIGHT >= 800
    
    def test_board_size(self) -> None:
        """Test board size is correct."""
        assert BOARD_SIZE == SQUARE_SIZE * 8
    
    def test_fps(self) -> None:
        """Test FPS is reasonable."""
        assert 30 <= FPS <= 120


class TestColors:
    """Tests for color configuration."""
    
    def test_basic_colors_exist(self) -> None:
        """Test basic colors are defined."""
        assert "white" in COLORS
        assert "black" in COLORS
        assert "light_square" in COLORS
        assert "dark_square" in COLORS
    
    def test_colors_are_valid_rgb(self) -> None:
        """Test all colors are valid RGB tuples."""
        for name, color in COLORS.items():
            assert isinstance(color, tuple)
            assert len(color) == 3
            for value in color:
                assert 0 <= value <= 255


class TestFontSizes:
    """Tests for font size configuration."""
    
    def test_font_sizes_exist(self) -> None:
        """Test font sizes are defined."""
        assert "small" in FONT_SIZES
        assert "medium" in FONT_SIZES
        assert "large" in FONT_SIZES
    
    def test_font_sizes_are_positive(self) -> None:
        """Test font sizes are positive integers."""
        for name, size in FONT_SIZES.items():
            assert isinstance(size, int)
            assert size > 0


class TestGameState:
    """Tests for game state enumeration."""
    
    def test_game_states_defined(self) -> None:
        """Test all game states are defined."""
        assert hasattr(GameState, "WHITE_SELECT")
        assert hasattr(GameState, "WHITE_MOVE")
        assert hasattr(GameState, "BLACK_SELECT")
        assert hasattr(GameState, "BLACK_MOVE")
        assert hasattr(GameState, "GAME_OVER")
        assert hasattr(GameState, "PAWN_PROMOTION")


class TestStatusMessages:
    """Tests for status messages."""
    
    def test_status_messages_for_all_states(self) -> None:
        """Test status messages exist for game states."""
        assert GameState.WHITE_SELECT in STATUS_MESSAGES
        assert GameState.WHITE_MOVE in STATUS_MESSAGES
        assert GameState.BLACK_SELECT in STATUS_MESSAGES
        assert GameState.BLACK_MOVE in STATUS_MESSAGES


class TestPromotionPieces:
    """Tests for promotion pieces."""
    
    def test_promotion_pieces_defined(self) -> None:
        """Test promotion pieces are defined."""
        assert len(PROMOTION_PIECES) == 4
        assert "queen" in PROMOTION_PIECES
        assert "rook" in PROMOTION_PIECES
        assert "bishop" in PROMOTION_PIECES
        assert "knight" in PROMOTION_PIECES
    
    def test_no_pawn_or_king_in_promotion(self) -> None:
        """Test pawn and king are not promotion options."""
        assert "pawn" not in PROMOTION_PIECES
        assert "king" not in PROMOTION_PIECES


class TestPieceOrder:
    """Tests for piece order."""
    
    def test_all_pieces_in_order(self) -> None:
        """Test all piece types are in order list."""
        assert "pawn" in PIECE_ORDER
        assert "queen" in PIECE_ORDER
        assert "king" in PIECE_ORDER
        assert "knight" in PIECE_ORDER
        assert "rook" in PIECE_ORDER
        assert "bishop" in PIECE_ORDER
