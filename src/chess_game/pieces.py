"""Piece definitions and types for Chess Game."""

from enum import Enum
from dataclasses import dataclass
from typing import Tuple, Optional


class PieceType(Enum):
    """Enumeration of chess piece types."""
    PAWN = "pawn"
    KNIGHT = "knight"
    BISHOP = "bishop"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"


class PieceColor(Enum):
    """Enumeration of piece colors."""
    WHITE = "white"
    BLACK = "black"
    
    def opposite(self) -> "PieceColor":
        """Return the opposite color."""
        return PieceColor.BLACK if self == PieceColor.WHITE else PieceColor.WHITE


@dataclass
class Piece:
    """Represents a chess piece on the board."""
    piece_type: PieceType
    color: PieceColor
    position: Tuple[int, int]
    has_moved: bool = False
    
    @property
    def x(self) -> int:
        """Get the x coordinate."""
        return self.position[0]
    
    @property
    def y(self) -> int:
        """Get the y coordinate."""
        return self.position[1]
    
    def move_to(self, new_position: Tuple[int, int]) -> None:
        """Move the piece to a new position."""
        self.position = new_position
        self.has_moved = True
    
    def is_pawn(self) -> bool:
        """Check if this is a pawn."""
        return self.piece_type == PieceType.PAWN
    
    def is_king(self) -> bool:
        """Check if this is a king."""
        return self.piece_type == PieceType.KING
    
    def is_rook(self) -> bool:
        """Check if this is a rook."""
        return self.piece_type == PieceType.ROOK
    
    def __str__(self) -> str:
        """String representation of the piece."""
        return f"{self.color.value} {self.piece_type.value} at {self.position}"
    
    def __repr__(self) -> str:
        """Debug representation of the piece."""
        return f"Piece({self.piece_type.value}, {self.color.value}, {self.position})"


@dataclass
class Move:
    """Represents a chess move."""
    piece: Piece
    from_pos: Tuple[int, int]
    to_pos: Tuple[int, int]
    captured_piece: Optional[Piece] = None
    is_castling: bool = False
    is_en_passant: bool = False
    is_promotion: bool = False
    promotion_piece: Optional[PieceType] = None
    
    def to_algebraic(self) -> str:
        """Convert move to algebraic notation."""
        files = "abcdefgh"
        ranks = "12345678"
        
        piece_symbol = ""
        if self.piece.piece_type != PieceType.PAWN:
            # Knight uses 'N' to avoid confusion with King 'K'
            if self.piece.piece_type == PieceType.KNIGHT:
                piece_symbol = "N"
            else:
                piece_symbol = self.piece.piece_type.value[0].upper()
            if piece_symbol == "K" and self.is_castling:
                # Castling notation
                if self.to_pos[0] > self.from_pos[0]:
                    return "O-O"  # Kingside
                else:
                    return "O-O-O"  # Queenside
        
        from_square = f"{files[self.from_pos[0]]}{ranks[self.from_pos[1]]}"
        to_square = f"{files[self.to_pos[0]]}{ranks[self.to_pos[1]]}"
        
        capture = "x" if self.captured_piece else ""
        
        promotion = ""
        if self.is_promotion and self.promotion_piece:
            promotion = f"={self.promotion_piece.value[0].upper()}"
        
        return f"{piece_symbol}{from_square}{capture}{to_square}{promotion}"
    
    def __str__(self) -> str:
        """String representation of the move."""
        return self.to_algebraic()
