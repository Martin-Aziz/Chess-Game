"""Tests for chess game pieces module."""

import pytest
from chess_game.pieces import Piece, PieceType, PieceColor, Move


class TestPieceType:
    """Tests for PieceType enum."""
    
    def test_piece_types_exist(self) -> None:
        """Test all piece types are defined."""
        assert PieceType.PAWN.value == "pawn"
        assert PieceType.KNIGHT.value == "knight"
        assert PieceType.BISHOP.value == "bishop"
        assert PieceType.ROOK.value == "rook"
        assert PieceType.QUEEN.value == "queen"
        assert PieceType.KING.value == "king"


class TestPieceColor:
    """Tests for PieceColor enum."""
    
    def test_colors_exist(self) -> None:
        """Test both colors are defined."""
        assert PieceColor.WHITE.value == "white"
        assert PieceColor.BLACK.value == "black"
    
    def test_opposite_color(self) -> None:
        """Test opposite color method."""
        assert PieceColor.WHITE.opposite() == PieceColor.BLACK
        assert PieceColor.BLACK.opposite() == PieceColor.WHITE


class TestPiece:
    """Tests for Piece class."""
    
    def test_piece_creation(self) -> None:
        """Test piece can be created."""
        piece = Piece(PieceType.PAWN, PieceColor.WHITE, (0, 1))
        assert piece.piece_type == PieceType.PAWN
        assert piece.color == PieceColor.WHITE
        assert piece.position == (0, 1)
        assert piece.has_moved is False
    
    def test_piece_position_properties(self) -> None:
        """Test x and y properties."""
        piece = Piece(PieceType.KNIGHT, PieceColor.BLACK, (3, 4))
        assert piece.x == 3
        assert piece.y == 4
    
    def test_piece_move_to(self) -> None:
        """Test moving a piece."""
        piece = Piece(PieceType.ROOK, PieceColor.WHITE, (0, 0))
        piece.move_to((0, 4))
        assert piece.position == (0, 4)
        assert piece.has_moved is True
    
    def test_is_pawn(self) -> None:
        """Test is_pawn method."""
        pawn = Piece(PieceType.PAWN, PieceColor.WHITE, (0, 1))
        knight = Piece(PieceType.KNIGHT, PieceColor.WHITE, (1, 0))
        assert pawn.is_pawn() is True
        assert knight.is_pawn() is False
    
    def test_is_king(self) -> None:
        """Test is_king method."""
        king = Piece(PieceType.KING, PieceColor.WHITE, (4, 0))
        queen = Piece(PieceType.QUEEN, PieceColor.WHITE, (3, 0))
        assert king.is_king() is True
        assert queen.is_king() is False
    
    def test_is_rook(self) -> None:
        """Test is_rook method."""
        rook = Piece(PieceType.ROOK, PieceColor.WHITE, (0, 0))
        bishop = Piece(PieceType.BISHOP, PieceColor.WHITE, (2, 0))
        assert rook.is_rook() is True
        assert bishop.is_rook() is False
    
    def test_piece_str(self) -> None:
        """Test string representation."""
        piece = Piece(PieceType.QUEEN, PieceColor.BLACK, (3, 7))
        assert "black" in str(piece).lower()
        assert "queen" in str(piece).lower()


class TestMove:
    """Tests for Move class."""
    
    def test_move_creation(self) -> None:
        """Test move can be created."""
        piece = Piece(PieceType.PAWN, PieceColor.WHITE, (4, 1))
        move = Move(piece=piece, from_pos=(4, 1), to_pos=(4, 3))
        assert move.piece == piece
        assert move.from_pos == (4, 1)
        assert move.to_pos == (4, 3)
        assert move.captured_piece is None
        assert move.is_castling is False
    
    def test_move_with_capture(self) -> None:
        """Test move with capture."""
        attacker = Piece(PieceType.PAWN, PieceColor.WHITE, (4, 4))
        target = Piece(PieceType.PAWN, PieceColor.BLACK, (5, 5))
        move = Move(
            piece=attacker, 
            from_pos=(4, 4), 
            to_pos=(5, 5), 
            captured_piece=target
        )
        assert move.captured_piece == target
    
    def test_algebraic_notation_pawn(self) -> None:
        """Test algebraic notation for pawn move."""
        piece = Piece(PieceType.PAWN, PieceColor.WHITE, (4, 2))
        move = Move(piece=piece, from_pos=(4, 1), to_pos=(4, 2))
        notation = move.to_algebraic()
        assert "e2" in notation
        assert "e3" in notation
    
    def test_algebraic_notation_knight(self) -> None:
        """Test algebraic notation for knight move."""
        piece = Piece(PieceType.KNIGHT, PieceColor.WHITE, (5, 2))
        move = Move(piece=piece, from_pos=(6, 0), to_pos=(5, 2))
        notation = move.to_algebraic()
        assert notation[0] == "N"
    
    def test_algebraic_notation_capture(self) -> None:
        """Test algebraic notation for capture."""
        attacker = Piece(PieceType.BISHOP, PieceColor.WHITE, (4, 4))
        target = Piece(PieceType.PAWN, PieceColor.BLACK, (4, 4))
        move = Move(
            piece=attacker, 
            from_pos=(2, 2), 
            to_pos=(4, 4), 
            captured_piece=target
        )
        notation = move.to_algebraic()
        assert "x" in notation
    
    def test_algebraic_notation_kingside_castling(self) -> None:
        """Test algebraic notation for kingside castling."""
        king = Piece(PieceType.KING, PieceColor.WHITE, (6, 0))
        move = Move(
            piece=king, 
            from_pos=(4, 0), 
            to_pos=(6, 0), 
            is_castling=True
        )
        assert move.to_algebraic() == "O-O"
    
    def test_algebraic_notation_queenside_castling(self) -> None:
        """Test algebraic notation for queenside castling."""
        king = Piece(PieceType.KING, PieceColor.WHITE, (2, 0))
        move = Move(
            piece=king, 
            from_pos=(4, 0), 
            to_pos=(2, 0), 
            is_castling=True
        )
        assert move.to_algebraic() == "O-O-O"
    
    def test_algebraic_notation_promotion(self) -> None:
        """Test algebraic notation for pawn promotion."""
        piece = Piece(PieceType.PAWN, PieceColor.WHITE, (4, 7))
        move = Move(
            piece=piece, 
            from_pos=(4, 6), 
            to_pos=(4, 7), 
            is_promotion=True,
            promotion_piece=PieceType.QUEEN
        )
        notation = move.to_algebraic()
        assert "=Q" in notation
