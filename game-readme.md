# Terminal Collection Game

A simple terminal-based game where you collect items while avoiding enemies. Navigate through a randomly generated world, collect $ symbols for points, and try to avoid the enemies (E) that chase you!

## Features

- Terminal-based gameplay using curses
- Random world generation with obstacles
- Collectible items that give points
- Enemy AI that follows the player
- High score system
- Consistent frame rate for smooth gameplay

## Requirements

The game requires Python 3.x and the following built-in libraries:
- curses (included with Python on Unix systems, requires `windows-curses` on Windows)
- random (built-in)
- time (built-in)

For Windows users, install the required curses library:
```bash
pip install windows-curses
```

## Installation

1. Clone this repository or download the game files:
```bash
git clone <repository-url>
```

2. Navigate to the game directory:
```bash
cd terminal-collection-game
```

## How to Play

1. Run the game:
```bash
python new_game.py
```

2. Controls:
   - W: Move up
   - A: Move left
   - S: Move down
   - D: Move right
   - Q: Quit game

3. Game Elements:
   - P: Player character
   - $: Collectible items (10 points each)
   - E: Enemies (avoid these!)
   - .: Obstacles (can't move through these)

4. Objective:
   - Collect as many $ symbols as possible
   - Avoid enemies (E)
   - Try to beat the high score!

## Game Features

### Scoring System
- Each collected $ gives you 10 points
- Your high score is saved between games
- Try to beat your previous high score!

### Enemy AI
- Enemies will slowly chase the player
- They move randomly but tend to follow your position
- Getting caught by an enemy ends the game

### World Generation
- Random obstacles are generated each game
- Food items appear randomly and expire over time
- New food spawns to replace expired items

## Development

The game is built using Python's curses library for terminal manipulation. Key components:

- `Game` class: Main game logic and state management
- Terminal rendering using curses
- Frame rate control for consistent game speed
- High score system using file I/O

## File Structure

- `new_game.py`: Main game file containing all game logic
- `score.txt`: Generated file that stores the high score
