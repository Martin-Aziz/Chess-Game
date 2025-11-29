"""Board logic and move validation for Chess Game."""

from typing import List, Tuple, Optional, Set
from chess_game.pieces import Piece, PieceType, PieceColor, Move


class Board:
    """Represents the chess board and handles move validation."""
    
    def __init__(self) -> None:
        """Initialize the board with starting positions."""
        self.pieces: List[Piece] = []
        self.captured_white: List[Piece] = []
        self.captured_black: List[Piece] = []
        self.move_history: List[Move] = []
        self.en_passant_target: Optional[Tuple[int, int]] = None
        self._setup_initial_position()
    
    def _setup_initial_position(self) -> None:
        """Set up the initial chess position."""
        self.pieces = []
        
        # White pieces (bottom of board, y=0 and y=1)
        back_row = [
            PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.KING,
            PieceType.QUEEN, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK
        ]
        
        for x, piece_type in enumerate(back_row):
            self.pieces.append(Piece(piece_type, PieceColor.WHITE, (x, 0)))
        
        for x in range(8):
            self.pieces.append(Piece(PieceType.PAWN, PieceColor.WHITE, (x, 1)))
        
        # Black pieces (top of board, y=7 and y=6)
        for x, piece_type in enumerate(back_row):
            self.pieces.append(Piece(piece_type, PieceColor.BLACK, (x, 7)))
        
        for x in range(8):
            self.pieces.append(Piece(PieceType.PAWN, PieceColor.BLACK, (x, 6)))
    
    def reset(self) -> None:
        """Reset the board to initial state."""
        self.captured_white = []
        self.captured_black = []
        self.move_history = []
        self.en_passant_target = None
        self._setup_initial_position()
    
    def get_piece_at(self, position: Tuple[int, int]) -> Optional[Piece]:
        """Get the piece at a given position."""
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None
    
    def get_pieces_by_color(self, color: PieceColor) -> List[Piece]:
        """Get all pieces of a given color."""
        return [p for p in self.pieces if p.color == color]
    
    def get_king(self, color: PieceColor) -> Optional[Piece]:
        """Get the king of a given color."""
        for piece in self.pieces:
            if piece.is_king() and piece.color == color:
                return piece
        return None
    
    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        """Check if a position is within the board."""
        x, y = position
        return 0 <= x <= 7 and 0 <= y <= 7
    
    def get_all_positions(self, color: PieceColor) -> Set[Tuple[int, int]]:
        """Get all positions occupied by pieces of a color."""
        return {p.position for p in self.pieces if p.color == color}
    
    def get_valid_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        """Get all valid moves for a piece."""
        if piece.piece_type == PieceType.PAWN:
            return self._get_pawn_moves(piece)
        elif piece.piece_type == PieceType.KNIGHT:
            return self._get_knight_moves(piece)
        elif piece.piece_type == PieceType.BISHOP:
            return self._get_bishop_moves(piece)
        elif piece.piece_type == PieceType.ROOK:
            return self._get_rook_moves(piece)
        elif piece.piece_type == PieceType.QUEEN:
            return self._get_queen_moves(piece)
        elif piece.piece_type == PieceType.KING:
            return self._get_king_moves(piece)
        return []
    
    def _get_pawn_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        """Get valid moves for a pawn."""
        moves = []
        x, y = piece.position
        direction = 1 if piece.color == PieceColor.WHITE else -1
        start_row = 1 if piece.color == PieceColor.WHITE else 6
        promotion_row = 7 if piece.color == PieceColor.WHITE else 0
        
        friends = self.get_all_positions(piece.color)
        enemies = self.get_all_positions(piece.color.opposite())
        all_pieces = friends | enemies
        
        # Single move forward
        forward = (x, y + direction)
        if self.is_valid_position(forward) and forward not in all_pieces:
            moves.append(forward)
            
            # Double move from starting position
            if y == start_row:
                double_forward = (x, y + 2 * direction)
                if double_forward not in all_pieces:
                    moves.append(double_forward)
        
        # Diagonal captures
        for dx in [-1, 1]:
            capture_pos = (x + dx, y + direction)
            if self.is_valid_position(capture_pos):
                if capture_pos in enemies:
                    moves.append(capture_pos)
                # En passant
                elif capture_pos == self.en_passant_target:
                    moves.append(capture_pos)
        
        return moves
    
    def _get_knight_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        """Get valid moves for a knight."""
        moves = []
        x, y = piece.position
        friends = self.get_all_positions(piece.color)
        
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        
        for dx, dy in knight_moves:
            new_pos = (x + dx, y + dy)
            if self.is_valid_position(new_pos) and new_pos not in friends:
                moves.append(new_pos)
        
        return moves
    
    def _get_sliding_moves(
        self, piece: Piece, directions: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """Get moves for sliding pieces (bishop, rook, queen)."""
        moves = []
        x, y = piece.position
        friends = self.get_all_positions(piece.color)
        enemies = self.get_all_positions(piece.color.opposite())
        
        for dx, dy in directions:
            for distance in range(1, 8):
                new_pos = (x + dx * distance, y + dy * distance)
                
                if not self.is_valid_position(new_pos):
                    break
                
                if new_pos in friends:
                    break
                
                moves.append(new_pos)
                
                if new_pos in enemies:
                    break
        
        return moves
    
    def _get_bishop_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        """Get valid moves for a bishop."""
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._get_sliding_moves(piece, directions)
    
    def _get_rook_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        """Get valid moves for a rook."""
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return self._get_sliding_moves(piece, directions)
    
    def _get_queen_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        """Get valid moves for a queen."""
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        return self._get_sliding_moves(piece, directions)
    
    def _get_king_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        """Get valid moves for a king."""
        moves = []
        x, y = piece.position
        friends = self.get_all_positions(piece.color)
        
        # Regular king moves
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_pos = (x + dx, y + dy)
                if self.is_valid_position(new_pos) and new_pos not in friends:
                    moves.append(new_pos)
        
        # Castling
        if not piece.has_moved and not self.is_in_check(piece.color):
            # Kingside castling
            kingside_rook = self.get_piece_at((7, y))
            if (kingside_rook and kingside_rook.is_rook() and 
                kingside_rook.color == piece.color and not kingside_rook.has_moved):
                # Check if squares between king and rook are empty
                if (self.get_piece_at((5, y)) is None and 
                    self.get_piece_at((6, y)) is None):
                    # Check if king doesn't pass through check
                    if not self._is_square_attacked((5, y), piece.color.opposite()):
                        moves.append((6, y))
            
            # Queenside castling
            queenside_rook = self.get_piece_at((0, y))
            if (queenside_rook and queenside_rook.is_rook() and 
                queenside_rook.color == piece.color and not queenside_rook.has_moved):
                # Check if squares between king and rook are empty
                if (self.get_piece_at((1, y)) is None and 
                    self.get_piece_at((2, y)) is None and 
                    self.get_piece_at((3, y)) is None):
                    # Check if king doesn't pass through check
                    if not self._is_square_attacked((3, y), piece.color.opposite()):
                        moves.append((2, y))
        
        return moves
    
    def _is_square_attacked(
        self, position: Tuple[int, int], by_color: PieceColor
    ) -> bool:
        """Check if a square is attacked by any piece of the given color."""
        for piece in self.get_pieces_by_color(by_color):
            # Get raw moves without checking for check (to avoid recursion)
            if piece.piece_type == PieceType.PAWN:
                # Pawns attack diagonally
                x, y = piece.position
                direction = 1 if piece.color == PieceColor.WHITE else -1
                attack_positions = [(x - 1, y + direction), (x + 1, y + direction)]
                if position in attack_positions:
                    return True
            elif piece.piece_type == PieceType.KING:
                # King attacks adjacent squares
                x, y = piece.position
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        if (x + dx, y + dy) == position:
                            return True
            else:
                moves = self.get_valid_moves(piece)
                if position in moves:
                    return True
        return False
    
    def is_in_check(self, color: PieceColor) -> bool:
        """Check if the king of the given color is in check."""
        king = self.get_king(color)
        if not king:
            return False
        return self._is_square_attacked(king.position, color.opposite())
    
    def is_checkmate(self, color: PieceColor) -> bool:
        """Check if the given color is in checkmate."""
        if not self.is_in_check(color):
            return False
        
        # Check if any move can get out of check
        for piece in self.get_pieces_by_color(color):
            for move in self.get_valid_moves(piece):
                if self._move_is_legal(piece, move):
                    return False
        return True
    
    def is_stalemate(self, color: PieceColor) -> bool:
        """Check if the given color is in stalemate."""
        if self.is_in_check(color):
            return False
        
        # Check if any legal move exists
        for piece in self.get_pieces_by_color(color):
            for move in self.get_valid_moves(piece):
                if self._move_is_legal(piece, move):
                    return False
        return True
    
    def _move_is_legal(self, piece: Piece, to_pos: Tuple[int, int]) -> bool:
        """Check if a move would leave the king in check."""
        # Simulate the move
        original_pos = piece.position
        captured = self.get_piece_at(to_pos)
        
        # Make the move temporarily
        piece.position = to_pos
        if captured:
            self.pieces.remove(captured)
        
        # Check if the king is in check after the move
        in_check = self.is_in_check(piece.color)
        
        # Undo the move
        piece.position = original_pos
        if captured:
            self.pieces.append(captured)
        
        return not in_check
    
    def get_legal_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        """Get all legal moves for a piece (excluding moves that leave king in check)."""
        valid_moves = self.get_valid_moves(piece)
        return [move for move in valid_moves if self._move_is_legal(piece, move)]
    
    def make_move(
        self, piece: Piece, to_pos: Tuple[int, int], 
        promotion_type: Optional[PieceType] = None
    ) -> Optional[Move]:
        """Execute a move on the board."""
        from_pos = piece.position
        captured = self.get_piece_at(to_pos)
        
        # Check for special moves
        is_castling = False
        is_en_passant = False
        is_promotion = False
        
        # En passant capture
        if piece.is_pawn() and to_pos == self.en_passant_target:
            is_en_passant = True
            direction = 1 if piece.color == PieceColor.WHITE else -1
            captured_pawn_pos = (to_pos[0], to_pos[1] - direction)
            captured = self.get_piece_at(captured_pawn_pos)
            if captured:
                self.pieces.remove(captured)
                if captured.color == PieceColor.WHITE:
                    self.captured_white.append(captured)
                else:
                    self.captured_black.append(captured)
        
        # Castling
        if piece.is_king() and abs(to_pos[0] - from_pos[0]) == 2:
            is_castling = True
            # Move the rook
            if to_pos[0] > from_pos[0]:  # Kingside
                rook = self.get_piece_at((7, from_pos[1]))
                if rook:
                    rook.move_to((5, from_pos[1]))
            else:  # Queenside
                rook = self.get_piece_at((0, from_pos[1]))
                if rook:
                    rook.move_to((3, from_pos[1]))
        
        # Regular capture
        if captured and not is_en_passant:
            self.pieces.remove(captured)
            if captured.color == PieceColor.WHITE:
                self.captured_white.append(captured)
            else:
                self.captured_black.append(captured)
        
        # Update en passant target
        self.en_passant_target = None
        if piece.is_pawn() and abs(to_pos[1] - from_pos[1]) == 2:
            direction = 1 if piece.color == PieceColor.WHITE else -1
            self.en_passant_target = (from_pos[0], from_pos[1] + direction)
        
        # Move the piece
        piece.move_to(to_pos)
        
        # Pawn promotion
        promotion_row = 7 if piece.color == PieceColor.WHITE else 0
        if piece.is_pawn() and to_pos[1] == promotion_row:
            is_promotion = True
            if promotion_type:
                piece.piece_type = promotion_type
        
        # Create and record the move
        move = Move(
            piece=piece,
            from_pos=from_pos,
            to_pos=to_pos,
            captured_piece=captured,
            is_castling=is_castling,
            is_en_passant=is_en_passant,
            is_promotion=is_promotion,
            promotion_piece=promotion_type
        )
        self.move_history.append(move)
        
        return move
    
    def undo_last_move(self) -> Optional[Move]:
        """Undo the last move made."""
        if not self.move_history:
            return None
        
        move = self.move_history.pop()
        
        # Restore piece position
        move.piece.position = move.from_pos
        move.piece.has_moved = len([m for m in self.move_history 
                                    if m.piece == move.piece]) > 0
        
        # Restore captured piece
        if move.captured_piece:
            self.pieces.append(move.captured_piece)
            if move.captured_piece.color == PieceColor.WHITE:
                self.captured_white.remove(move.captured_piece)
            else:
                self.captured_black.remove(move.captured_piece)
        
        # Undo castling
        if move.is_castling:
            if move.to_pos[0] > move.from_pos[0]:  # Kingside
                rook = self.get_piece_at((5, move.from_pos[1]))
                if rook:
                    rook.position = (7, move.from_pos[1])
                    rook.has_moved = False
            else:  # Queenside
                rook = self.get_piece_at((3, move.from_pos[1]))
                if rook:
                    rook.position = (0, move.from_pos[1])
                    rook.has_moved = False
        
        # Undo promotion
        if move.is_promotion:
            move.piece.piece_type = PieceType.PAWN
        
        # Restore en passant target
        if len(self.move_history) > 0:
            last_move = self.move_history[-1]
            if (last_move.piece.is_pawn() and 
                abs(last_move.to_pos[1] - last_move.from_pos[1]) == 2):
                direction = 1 if last_move.piece.color == PieceColor.WHITE else -1
                self.en_passant_target = (
                    last_move.from_pos[0], 
                    last_move.from_pos[1] + direction
                )
            else:
                self.en_passant_target = None
        else:
            self.en_passant_target = None
        
        return move
