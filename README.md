# Tic-Tac-Toe

A simple command-line Tic-Tac-Toe game written in Python.

## Getting Started

### Requirements

- Python 3.7+

### Running the game

```bash
python -m src.tic_tac_toe
```

### Playing

Follow the prompts to make moves. The board positions are numbered 1 through 9:
```
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9
```

### Game Modes

You can play either human vs human or human vs a computer bot. When playing against the bot you'll be asked to choose a skill level:

- **Beginner** – picks moves at random.
- **Intermediate** – tries to win in one move or block you, otherwise plays randomly.
- **Expert** – uses the minimax algorithm for an optimal strategy.

You can also choose whether you or the bot goes first.

When a player wins the game, a simple ASCII firework animation plays to celebrate the victory in terminal mode. The graphical interface uses its own visual effects.

### Graphics

The game now launches a window using **pygame**. Moves are made by clicking cells. The board uses bold lines and bright, cartoonish colours. To install the GUI dependencies:

```bash
pip install pygame
```

If `pygame` is not available the game will fall back to the text-based interface.

To start the game (GUI preferred):

```bash
python -m src.tic_tac_toe
```

When pygame is installed, the initial configuration menu appears inside the
window. You can now **click** options with the mouse instead of using the
keyboard.  Items highlight when hovered so it's clear what will be chosen.
Simply click the desired mode, skill level, and whether you go first; the
interface stays entirely within the window.

Once the game starts, the cell under the cursor highlights yellow (if it's
empty and it's your turn), making it obvious where the next piece will land.

## License

This project is licensed under the MIT License.
