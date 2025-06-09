# ✂️ Rock Paper Scissors Game

A Python implementation of the classic Rock Paper Scissors game with a tournament-style scoring system.

## 🎮 Game Features

- **Best of 3 rounds** - First to win 3 rounds wins the match
- **Live scoreboard** - Track your wins and losses across multiple matches
- **Input validation** - Handles invalid inputs gracefully
- **Play again option** - Continue playing multiple matches
- **Clean terminal interface** - Simple and intuitive gameplay

## 🚀 How to Play

### Prerequisites
- Python 3.6 or higher

### Running the Game
1. Navigate to the game directory:
   ```bash
   cd r-p-s-game
   ```

2. Run the game:
   ```bash
   python main.py
   ```

### Gameplay
1. Enter your choice when prompted:
   - `r` for Rock 🪨
   - `p` for Paper 📄
   - `s` for Scissors ✂️

2. The game will show:
   - Your choice vs Computer's choice
   - Round result (Win/Lose/Draw)

3. First to win 3 rounds wins the match

4. After each match, the scoreboard updates showing:
   - Total matches won by you
   - Total matches won by computer
   - Last match result

5. Choose to play again or exit

## 🏗️ Project Structure

```
r-p-s-game/
├── config.py      # Game configuration and rules
├── game.py        # Core game logic and functions
└── main.py        # Entry point to start the game
```

## 🎯 Game Rules

- **Rock** beats **Scissors**
- **Paper** beats **Rock** 
- **Scissors** beats **Paper**
- Same choices result in a **Draw**

## 🔧 Code Structure

### `config.py`
- Defines valid game choices
- Contains winning rules logic
- Maintains global scoreboard

### `game.py`
- `get_user_choice()` - Handles user input with validation
- `get_system_choice()` - Generates random computer choice
- `find_winner()` - Determines round winner based on rules
- `update_scoreboard()` - Updates and displays match results
- `play()` - Main game loop for a single match
- `play_again()` - Handles replay functionality

### `main.py`
- Entry point that starts the game

## 🎨 Sample Gameplay

```
Please enter you're choice (r, p, s): r
user: r    system: s    result: You win
Please enter you're choice (r, p, s): p
user: p    system: r    result: You win
Please enter you're choice (r, p, s): s
user: s    system: p    result: You win

##############################
## user: 1                  ##
## system: 0                ##
## last game: You win       ##
##############################

Do you want to play again!?: y
```

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📧 Contact

**Email:** aliranjbar.net1@gmail.com

---
*Have fun playing! 🎮*