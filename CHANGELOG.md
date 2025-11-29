# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2024-XX-XX

### Added
- **Modular Architecture**: Refactored monolithic code into separate modules
  - `game.py`: Main game loop and event handling
  - `board.py`: Board logic and move validation
  - `pieces.py`: Piece definitions and move representation
  - `renderer.py`: All Pygame rendering
  - `config.py`: Configuration constants
- **En Passant**: Implemented en passant pawn capture
- **Castling**: Implemented kingside and queenside castling
- **Checkmate Detection**: Automatic detection of checkmate
- **Stalemate Detection**: Automatic detection of stalemate
- **Move History**: Algebraic notation move history
- **Undo Move**: Press 'U' to undo last move
- **Legal Move Filtering**: Moves that leave king in check are now filtered out
- **Test Suite**: Added comprehensive unit tests
  - `test_pieces.py`: Tests for piece classes
  - `test_board.py`: Tests for board logic
  - `test_config.py`: Tests for configuration
- **CI/CD Pipeline**: GitHub Actions workflow for testing and deployment
- **Docker Support**: Dockerfile and docker-compose for containerization
- **Documentation**: 
  - Updated README with quick start guide
  - Architecture documentation
  - Operations runbook
  - This changelog

### Changed
- **Board Colors**: Updated to classic wood tones
- **Visual Feedback**: Improved move indicators (dots for moves, rings for captures)
- **Status Bar**: Enhanced status messages
- **Game Over Screen**: Added semi-transparent overlay with restart instructions

### Fixed
- **Game Over Flag**: Fixed issue where `game_over` flag was never set to `True`
- **Relative Paths**: Fixed image loading to use absolute paths
- **Selection Logic**: Fixed piece selection and deselection behavior

### Security
- Added `.gitignore` to prevent sensitive data commits
- Non-root user in Docker container
- Dependency vulnerability scanning in CI

## [0.1.0] - Initial Release

### Features
- Basic chess game with Pygame
- All piece movements (pawn, knight, bishop, rook, queen, king)
- Pawn promotion
- Check indication (flashing king)
- Captured pieces display
- Forfeit option
- Game restart

### Known Issues
- En passant not implemented
- Castling not implemented
- Checkmate/stalemate not detected
- No move history
- No undo functionality
