# Chess Game - Architecture Documentation

## Overview

This document describes the architecture of the Chess Game application, a Python-based chess implementation using Pygame for graphics.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Chess Game Application                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │
│  │   Game Layer    │───▶│   Board Layer   │───▶│  Pieces Layer   │  │
│  │   (game.py)     │    │   (board.py)    │    │  (pieces.py)    │  │
│  └────────┬────────┘    └─────────────────┘    └─────────────────┘  │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────┐    ┌─────────────────┐                         │
│  │ Renderer Layer  │◀───│  Config Layer   │                         │
│  │  (renderer.py)  │    │  (config.py)    │                         │
│  └────────┬────────┘    └─────────────────┘                         │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────┐                                                │
│  │     Pygame      │                                                │
│  │   (Graphics)    │                                                │
│  └─────────────────┘                                                │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Game Layer (`game.py`)

**Responsibilities:**
- Main game loop management
- Event handling (mouse clicks, keyboard input)
- Game state management (turn tracking, game over detection)
- Coordination between Board and Renderer

**Key Classes:**
- `ChessGame`: Main game class

**State Machine:**
```
WHITE_SELECT ──▶ WHITE_MOVE ──▶ BLACK_SELECT ──▶ BLACK_MOVE ──▶ (loop)
                     │                               │
                     ▼                               ▼
               PAWN_PROMOTION                  PAWN_PROMOTION
                     │                               │
                     ▼                               ▼
                 GAME_OVER ◀────────────────────────┘
```

### 2. Board Layer (`board.py`)

**Responsibilities:**
- Board state management (piece positions)
- Move validation for all piece types
- Special move handling (castling, en passant, promotion)
- Check, checkmate, and stalemate detection
- Move history and undo functionality

**Key Classes:**
- `Board`: Main board class

**Move Validation Flow:**
```
get_valid_moves() ──▶ _get_[piece]_moves() ──▶ filter by is_valid_position()
                                                         │
                                                         ▼
get_legal_moves() ◀── filter by _move_is_legal() ◀── returns moves
```

### 3. Pieces Layer (`pieces.py`)

**Responsibilities:**
- Piece type definitions (enum)
- Piece color definitions (enum)
- Piece data class with position and state
- Move representation and algebraic notation

**Key Classes:**
- `PieceType`: Enum for piece types
- `PieceColor`: Enum for colors (with `opposite()` method)
- `Piece`: Dataclass for piece state
- `Move`: Dataclass for move representation

### 4. Renderer Layer (`renderer.py`)

**Responsibilities:**
- Board rendering (squares, grid)
- Piece rendering (images, highlighting)
- UI elements (status bar, buttons)
- Visual feedback (valid moves, check indicator)
- Game over screen
- Pawn promotion dialog

**Key Classes:**
- `Renderer`: Main rendering class

### 5. Config Layer (`config.py`)

**Responsibilities:**
- Window dimensions and constants
- Color definitions
- Font sizes
- Asset paths
- Game state constants
- Status messages

## Data Flow

### Move Execution Flow

```
1. User clicks on piece
   │
   ▼
2. game.handle_click() identifies piece
   │
   ▼
3. board.get_legal_moves(piece) calculates valid moves
   │
   ▼
4. renderer.draw_valid_moves() displays options
   │
   ▼
5. User clicks destination
   │
   ▼
6. board.make_move() executes move
   │
   ▼
7. board.is_checkmate() / is_stalemate() checks game state
   │
   ▼
8. game.current_color switches
```

### Render Loop

```
game.render()
    │
    ├──▶ renderer.draw_board()
    ├──▶ renderer.draw_pieces()
    ├──▶ renderer.draw_valid_moves()
    ├──▶ renderer.draw_captured_pieces()
    ├──▶ renderer.draw_check_indicator()
    ├──▶ renderer.draw_status_bar()
    ├──▶ renderer.draw_move_history()
    ├──▶ renderer.draw_promotion_dialog() (if needed)
    └──▶ renderer.draw_game_over() (if needed)
```

## Design Patterns

### 1. State Pattern
Game states are managed through the `GameState` enum, with different behavior for each state.

### 2. Command Pattern
Moves are encapsulated in `Move` objects, enabling undo functionality.

### 3. Single Responsibility
Each module has a single, well-defined responsibility.

### 4. Dependency Injection
The `Renderer` receives the pygame `screen` object, making it testable.

## File Structure

```
src/chess_game/
├── __init__.py          # Package exports
├── main.py              # Entry point
├── game.py              # ChessGame class (350 lines)
├── board.py             # Board class (450 lines)
├── pieces.py            # Piece classes (150 lines)
├── renderer.py          # Renderer class (300 lines)
├── config.py            # Constants (120 lines)
└── assets/
    ├── images/          # Piece images
    └── sounds/          # Sound effects (future)
```

## Future Improvements

1. **AI Opponent**: Implement minimax with alpha-beta pruning
2. **Network Play**: Add multiplayer over network
3. **Game Persistence**: Save/load games in PGN format
4. **Sound Effects**: Add audio feedback
5. **Themes**: Customizable board and piece themes
6. **Analysis Mode**: Position analysis and move suggestions

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pygame | ≥2.0.0 | Graphics, input, window management |
| pytest | ≥7.0.0 | Testing (dev) |
| black | ≥23.0.0 | Code formatting (dev) |
| mypy | ≥1.0.0 | Type checking (dev) |
