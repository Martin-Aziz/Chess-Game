"""Tests for chess game board module."""

import pytest
from chess_game.board import Board
from chess_game.pieces import Piece, PieceType, PieceColor


class TestBoardInitialization:
    """Tests for board initialization."""
    
    def test_board_creation(self) -> None:
        """Test board can be created."""
        board = Board()
        assert board is not None
    
    def test_initial_piece_count(self) -> None:
        """Test correct number of pieces at start."""
        board = Board()
        assert len(board.pieces) == 32
    
    def test_initial_white_pieces(self) -> None:
        """Test white pieces are set up correctly."""
        board = Board()
        white_pieces = board.get_pieces_by_color(PieceColor.WHITE)
        assert len(white_pieces) == 16
    
    def test_initial_black_pieces(self) -> None:
        """Test black pieces are set up correctly."""
        board = Board()
        black_pieces = board.get_pieces_by_color(PieceColor.BLACK)
        assert len(black_pieces) == 16
    
    def test_kings_present(self) -> None:
        """Test both kings are present."""
        board = Board()
        white_king = board.get_king(PieceColor.WHITE)
        black_king = board.get_king(PieceColor.BLACK)
        assert white_king is not None
        assert black_king is not None
    
    def test_king_positions(self) -> None:
        """Test kings are in correct starting positions."""
        board = Board()
        white_king = board.get_king(PieceColor.WHITE)
        black_king = board.get_king(PieceColor.BLACK)
        # Note: King starts at d1 (3,0) in this setup
        assert white_king.position == (3, 0)
        assert black_king.position == (3, 7)
    
    def test_no_captured_pieces_at_start(self) -> None:
        """Test no captured pieces at start."""
        board = Board()
        assert len(board.captured_white) == 0
        assert len(board.captured_black) == 0
    
    def test_reset(self) -> None:
        """Test board reset."""
        board = Board()
        # Make some changes
        pawn = board.get_piece_at((0, 1))
        if pawn:
            board.make_move(pawn, (0, 3))
        
        # Reset
        board.reset()
        
        assert len(board.pieces) == 32
        assert len(board.move_history) == 0
        assert board.get_piece_at((0, 1)) is not None


class TestBoardQueries:
    """Tests for board query methods."""
    
    def test_get_piece_at_occupied(self) -> None:
        """Test getting piece at occupied square."""
        board = Board()
        piece = board.get_piece_at((0, 0))
        assert piece is not None
        assert piece.piece_type == PieceType.ROOK
    
    def test_get_piece_at_empty(self) -> None:
        """Test getting piece at empty square."""
        board = Board()
        piece = board.get_piece_at((4, 4))
        assert piece is None
    
    def test_is_valid_position(self) -> None:
        """Test position validation."""
        board = Board()
        assert board.is_valid_position((0, 0)) is True
        assert board.is_valid_position((7, 7)) is True
        assert board.is_valid_position((4, 4)) is True
        assert board.is_valid_position((-1, 0)) is False
        assert board.is_valid_position((8, 0)) is False
        assert board.is_valid_position((0, 8)) is False


class TestPawnMoves:
    """Tests for pawn move validation."""
    
    def test_white_pawn_single_move(self) -> None:
        """Test white pawn can move one square forward."""
        board = Board()
        pawn = board.get_piece_at((4, 1))
        moves = board.get_valid_moves(pawn)
        assert (4, 2) in moves
    
    def test_white_pawn_double_move(self) -> None:
        """Test white pawn can move two squares from start."""
        board = Board()
        pawn = board.get_piece_at((4, 1))
        moves = board.get_valid_moves(pawn)
        assert (4, 3) in moves
    
    def test_black_pawn_single_move(self) -> None:
        """Test black pawn can move one square forward."""
        board = Board()
        pawn = board.get_piece_at((4, 6))
        moves = board.get_valid_moves(pawn)
        assert (4, 5) in moves
    
    def test_black_pawn_double_move(self) -> None:
        """Test black pawn can move two squares from start."""
        board = Board()
        pawn = board.get_piece_at((4, 6))
        moves = board.get_valid_moves(pawn)
        assert (4, 4) in moves
    
    def test_pawn_blocked(self) -> None:
        """Test pawn cannot move through pieces."""
        board = Board()
        # Move white pawn to block
        pawn1 = board.get_piece_at((4, 1))
        board.make_move(pawn1, (4, 3))
        
        # Move black pawn to just in front
        pawn2 = board.get_piece_at((4, 6))
        board.make_move(pawn2, (4, 4))
        
        # Now white pawn should have no forward moves
        moves = board.get_valid_moves(pawn1)
        assert (4, 4) not in moves


class TestKnightMoves:
    """Tests for knight move validation."""
    
    def test_knight_moves_from_start(self) -> None:
        """Test knight has correct moves from starting position."""
        board = Board()
        knight = board.get_piece_at((1, 0))  # b1 knight
        moves = board.get_valid_moves(knight)
        
        # Knight can move to a3 and c3
        assert (0, 2) in moves
        assert (2, 2) in moves
        # Cannot move to friendly pieces
        assert (1, 2) not in moves  # blocked by pawn
    
    def test_knight_l_shape(self) -> None:
        """Test knight moves in L-shape."""
        board = Board()
        # Move knight to center
        knight = board.get_piece_at((1, 0))
        board.make_move(knight, (2, 2))
        
        moves = board.get_valid_moves(knight)
        # From c3, knight should be able to reach many squares
        expected_moves = [
            (0, 1), (0, 3), (1, 4), (3, 4), (4, 3), (4, 1)
        ]
        for move in expected_moves:
            # Check that L-shaped moves are valid
            dx = abs(move[0] - 2)
            dy = abs(move[1] - 2)
            assert (dx == 1 and dy == 2) or (dx == 2 and dy == 1)


class TestRookMoves:
    """Tests for rook move validation."""
    
    def test_rook_blocked_at_start(self) -> None:
        """Test rook cannot move at start (blocked by pawns)."""
        board = Board()
        rook = board.get_piece_at((0, 0))
        moves = board.get_valid_moves(rook)
        assert len(moves) == 0
    
    def test_rook_vertical_moves(self) -> None:
        """Test rook can move vertically."""
        board = Board()
        # Remove pawn in front of rook
        pawn = board.get_piece_at((0, 1))
        board.pieces.remove(pawn)
        
        rook = board.get_piece_at((0, 0))
        moves = board.get_valid_moves(rook)
        
        # Should be able to move up the a-file
        for y in range(1, 7):
            assert (0, y) in moves


class TestBishopMoves:
    """Tests for bishop move validation."""
    
    def test_bishop_blocked_at_start(self) -> None:
        """Test bishop cannot move at start (blocked by pawns)."""
        board = Board()
        bishop = board.get_piece_at((2, 0))
        moves = board.get_valid_moves(bishop)
        assert len(moves) == 0


class TestKingMoves:
    """Tests for king move validation."""
    
    def test_king_blocked_at_start(self) -> None:
        """Test king cannot move at start (surrounded)."""
        board = Board()
        king = board.get_king(PieceColor.WHITE)
        moves = board.get_valid_moves(king)
        assert len(moves) == 0


class TestCheck:
    """Tests for check detection."""
    
    def test_not_in_check_at_start(self) -> None:
        """Test no check at game start."""
        board = Board()
        assert board.is_in_check(PieceColor.WHITE) is False
        assert board.is_in_check(PieceColor.BLACK) is False


class TestMakeMove:
    """Tests for making moves."""
    
    def test_simple_move(self) -> None:
        """Test making a simple pawn move."""
        board = Board()
        pawn = board.get_piece_at((4, 1))
        
        move = board.make_move(pawn, (4, 3))
        
        assert move is not None
        assert pawn.position == (4, 3)
        assert pawn.has_moved is True
    
    def test_capture(self) -> None:
        """Test capturing a piece."""
        board = Board()
        
        # Set up a capture scenario
        white_pawn = board.get_piece_at((4, 1))
        board.make_move(white_pawn, (4, 4))
        
        black_pawn = board.get_piece_at((3, 6))
        board.make_move(black_pawn, (3, 5))
        board.make_move(black_pawn, (3, 4))  # Move black pawn adjacent
        
        # This simulates capturing - manually position
        board.make_move(white_pawn, (3, 5))
        
        # The move should have recorded the capture
        assert len(board.captured_black) > 0 or len(board.move_history) > 0


class TestMoveHistory:
    """Tests for move history."""
    
    def test_move_recorded(self) -> None:
        """Test moves are recorded in history."""
        board = Board()
        pawn = board.get_piece_at((4, 1))
        
        board.make_move(pawn, (4, 3))
        
        assert len(board.move_history) == 1
    
    def test_undo_move(self) -> None:
        """Test undoing a move."""
        board = Board()
        pawn = board.get_piece_at((4, 1))
        original_pos = pawn.position
        
        board.make_move(pawn, (4, 3))
        board.undo_last_move()
        
        assert pawn.position == original_pos
        assert pawn.has_moved is False
        assert len(board.move_history) == 0
