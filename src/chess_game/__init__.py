"""Chess Game - A Python chess implementation using Pygame."""

__version__ = "0.5.0"
__author__ = "Chess Game Contributors"

from chess_game.game import ChessGame
from chess_game.board import Board
from chess_game.pieces import Piece, PieceType, PieceColor

__all__ = ["ChessGame", "Board", "Piece", "PieceType", "PieceColor"]
