# Pentago Game

A simple implementation of the board game Pentago using Python, Pygame and NumPy.

This project provides a local graphical version of Pentago with support for:
- Player vs Player
- Player vs Computer (Easy and Hard modes)
- Board rotation mechanics and sound effects

**Built with**: Python, Pygame, NumPy

**Quick demo**: run the game locally and play using the on-screen buttons.

**Requirements**
- Python 3.8+ recommended
- Pygame
- NumPy

You can install the dependencies with pip:

```bash
pip install pygame numpy
```

If you prefer a requirements file, create a `requirements.txt` with:

```
pygame
numpy
```

and then run:

```bash
pip install -r requirements.txt
```

**Run the game**

From the project root folder run:

```bash
python game.py
```

**Controls & Gameplay**
- Use the mouse to click matrix cells to place marbles.
- After placing a marble, click one of the rotate buttons (top-left/top-right/bottom-left/bottom-right) to rotate the corresponding 3x3 quadrant.
- Objective: get five marbles in a row (horizontal, vertical, or diagonal). If the board fills with no winner, the game is a stalemate.

**Game Modes**
- Player vs Player: two human players take turns.
- Player vs Computer (Easy/Hard): one human vs AI. The AI has two levels: Easy (random moves) and Hard (basic lookahead heuristics).

**Project structure**
- `game.py` — Main game implementation and UI (Pygame loop).
- `font/` — Font assets used by the game.
- `img/` — Images for the board, marbles and buttons.
- `SFX/` — Sound effects used in-game.

**Troubleshooting**
- If Pygame fails to initialize, ensure your environment has an available display (on headless servers use a virtual display).
- If sound files don't play, confirm the files exist in `SFX/` and your system audio is available.

**Credits & License**
- Author: Mohamed (project workspace)
- Sounds and images included in `img/` and `SFX/` (ensure you have the rights to redistribute if publishing).
- License: add your preferred license or state "All rights reserved".


 
#  Thanks for exploring :)