# Chess Game

A fully-featured chess game built with Python and Pygame.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

## Features

- ✅ Complete chess rules implementation
- ✅ All piece movements (pawn, knight, bishop, rook, queen, king)
- ✅ Pawn promotion with piece selection
- ✅ Castling (kingside and queenside)
- ✅ En passant capture
- ✅ Check detection with visual indicator
- ✅ Checkmate and stalemate detection
- ✅ Move history with algebraic notation
- ✅ Undo move functionality
- ✅ Captured pieces display
- ✅ Forfeit option
- ✅ Game restart

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/example/chess-game.git
cd chess-game

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Running the Game

```bash
# Option 1: Run as module
python -m chess_game.main

# Option 2: Run the legacy version
cd "Chess Game with Pygames"
python main.py

# Option 3: Use the console script (after pip install -e .)
chess-game
```

## Controls

| Action | Control |
|--------|---------|
| Select piece | Left click on piece |
| Move piece | Left click on highlighted square |
| Undo move | Press `U` |
| Restart game | Press `Enter` (after game over) |
| Forfeit | Click `FORFEIT` button |
| Quit | Press `Escape` or close window |

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional)
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=chess_game --cov-report=html

# Run specific test file
pytest tests/test_board.py -v
```

### Code Quality

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Lint
flake8 src tests

# Type check
mypy src
```

## Docker

### Build and Run

```bash
# Build image
docker build -t chess-game .

# Run (requires X11 display)
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix chess-game

# Using docker-compose
docker-compose up chess-game
```

### Run Tests in Docker

```bash
docker-compose --profile test up test
```

## Project Structure

```
chess-game/
├── src/
│   └── chess_game/
│       ├── __init__.py      # Package initialization
│       ├── main.py          # Entry point
│       ├── game.py          # Main game loop
│       ├── board.py         # Board logic and move validation
│       ├── pieces.py        # Piece definitions
│       ├── renderer.py      # Pygame rendering
│       ├── config.py        # Configuration constants
│       └── assets/          # Images and sounds
├── tests/
│   ├── test_board.py        # Board tests
│   ├── test_pieces.py       # Piece tests
│   └── test_config.py       # Config tests
├── Chess Game with Pygames/ # Legacy version
│   ├── main.py
│   └── images/
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml          # Project configuration
├── Dockerfile              # Container definition
├── docker-compose.yml      # Container orchestration
└── README.md               # This file
```

## Architecture

The game follows a modular architecture:

- **Game Layer** (`game.py`): Main game loop, event handling, state management
- **Board Layer** (`board.py`): Chess logic, move validation, check/checkmate detection
- **Pieces Layer** (`pieces.py`): Piece definitions, move representation
- **Renderer Layer** (`renderer.py`): All Pygame rendering, UI components
- **Config Layer** (`config.py`): Constants, colors, dimensions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Pygame](https://www.pygame.org/) - Game development library
- Chess piece images from the original project