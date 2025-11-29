# Chess Game - Operations Runbook

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Installation](#installation)
3. [Running the Application](#running-the-application)
4. [Troubleshooting](#troubleshooting)
5. [Monitoring](#monitoring)
6. [Rollback Procedures](#rollback-procedures)
7. [Emergency Contacts](#emergency-contacts)

## Quick Reference

| Action | Command |
|--------|---------|
| Install | `pip install -e .` |
| Run | `python -m chess_game.main` |
| Test | `pytest` |
| Build Docker | `docker build -t chess-game .` |
| Run Docker | `docker-compose up chess-game` |

## Installation

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/example/chess-game.git
cd chess-game

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .

# 4. Verify installation
python -c "import chess_game; print(chess_game.__version__)"
```

### Docker Installation

```bash
# Build image
docker build -t chess-game:latest .

# Verify image
docker images | grep chess-game
```

## Running the Application

### Local Execution

```bash
# Standard run
python -m chess_game.main

# With debug output
PYTHONDONTWRITEBYTECODE=1 python -m chess_game.main

# Run legacy version
cd "Chess Game with Pygames" && python main.py
```

### Docker Execution

```bash
# Linux (with X11)
xhost +local:docker
docker run -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           chess-game:latest

# macOS (with XQuartz)
# 1. Install XQuartz: brew install --cask xquartz
# 2. Enable "Allow connections from network clients" in XQuartz preferences
# 3. Restart XQuartz
xhost +localhost
docker run -e DISPLAY=host.docker.internal:0 chess-game:latest
```

## Troubleshooting

### Common Issues

#### Issue: `pygame not found`
```bash
# Solution
pip install pygame>=2.0.0
```

#### Issue: `No display found`
```bash
# Linux: Ensure X11 is running
echo $DISPLAY  # Should output something like :0

# Docker: Enable X11 forwarding
xhost +local:docker
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix chess-game
```

#### Issue: `Image file not found`
```bash
# Verify images exist
ls -la "Chess Game with Pygames/images/"

# Expected files:
# - King.png, bishop.png, knight.png, pawn.png, rock.png, white queen.png
# - black King.png, bishop black.png, knight black.png, pawn black.png, 
#   rock black.png, black Queen.png
```

#### Issue: `Permission denied`
```bash
# Fix file permissions
chmod -R 755 .
chmod +x src/chess_game/main.py
```

#### Issue: `Port already in use` (if running server mode)
```bash
# Find process using port
lsof -i :8080
# Kill process
kill -9 <PID>
```

### Debug Mode

```bash
# Enable Python debug mode
python -v -m chess_game.main

# Enable pygame debug
export SDL_DEBUG=1
python -m chess_game.main
```

### Log Collection

```bash
# Capture output to file
python -m chess_game.main 2>&1 | tee game.log

# View recent logs
tail -100 game.log
```

## Monitoring

### Health Checks

For GUI applications, monitoring is limited to process monitoring:

```bash
# Check if process is running
pgrep -f "chess_game.main"

# Check memory usage
ps aux | grep chess_game

# Check CPU usage
top -p $(pgrep -f chess_game)
```

### Metrics to Watch

| Metric | Warning | Critical |
|--------|---------|----------|
| Memory Usage | > 500MB | > 1GB |
| CPU Usage | > 50% | > 80% |
| FPS Drop | < 30 FPS | < 15 FPS |

### Performance Profiling

```bash
# Profile the application
python -m cProfile -o profile.stats -m chess_game.main

# Analyze profile
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"
```

## Rollback Procedures

### Version Rollback

```bash
# 1. Check current version
python -c "import chess_game; print(chess_game.__version__)"

# 2. Rollback to previous version
git log --oneline -10  # Find previous commit
git checkout <commit-hash>

# 3. Reinstall
pip install -e .

# 4. Verify rollback
python -c "import chess_game; print(chess_game.__version__)"
```

### Docker Rollback

```bash
# 1. List available images
docker images chess-game --format "{{.Tag}}"

# 2. Rollback to previous version
docker run chess-game:<previous-version>

# Or using docker-compose
docker-compose down
docker-compose up -d --no-deps chess-game:<previous-version>
```

### Database Rollback

N/A - This application does not use a database.

## Emergency Contacts

| Role | Contact | Escalation |
|------|---------|------------|
| Primary On-Call | developer@example.com | Immediately |
| Backup On-Call | backup@example.com | After 15 min |
| Manager | manager@example.com | After 30 min |

## Incident Response

### Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| P1 | App won't start | < 1 hour |
| P2 | Major feature broken | < 4 hours |
| P3 | Minor bug | < 24 hours |
| P4 | Enhancement | Next sprint |

### Incident Template

```
**Incident Title:** [Brief description]
**Severity:** P1/P2/P3/P4
**Time Detected:** [ISO 8601 timestamp]
**Time Resolved:** [ISO 8601 timestamp]
**Impact:** [Description of user impact]
**Root Cause:** [What caused the issue]
**Resolution:** [How it was fixed]
**Follow-up:** [Preventive measures]
```
