# Bad Chess Game

As the name suggests, It is a bad chess game I built. But, It's fully functional, built with Python and Pygame, featuring complete chess rules implementation, sound effects, and a standard graphical interface.

## Features
- Complete Chess Rules
- Visual Interface
- Sound Effects
- Castling, en passant, pawn promotion(only queen for now)
- Check/stalemate/ checkmate detection 
- Board flips/ Move validation/ undoing moves

## Screenshots

<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/0a6f27eb-5eb8-4722-bdf6-d73873ac58c7" />
As you can see it shows the available legal moves and captures and the king is castled



## Installation

### Prerequisites
- Python 3.6+ (Download from python.org)
- Pygame

### Setup
1. Clone this repository:
```bash
git clone https://github.com/hsikelias/BadChessEngine2.git
cd BadChessEngine2
```

2. Install Pygame:
```bash
pip install pygame
```

3. Ensure you have the required assets:
   - `images/` folder with chess piece PNG files (wp.png, wR.png, etc.)
   - `sounds/` folder with WAV sound files

## How to Play

1. Run the game:
```bash
python ChessMain.py
```

2. **Making Moves:**
   - Click on a piece to select it
   - Click on a destination square to move
   - Click the same square twice to deselect

3. **Controls:**
   - **Mouse**: Select and move pieces
   - **Z Key**: Undo last move

## Project Structure

```
Chess/
├── ChessEngine.py      # Game logic and chess rules
├── ChessMain.py        # GUI and user interface  
├── __init__.py         # Package initializer
├── images/             # Chess piece sprites
│   ├── wp.png         # White pawn
│   ├── wR.png         # White rook
│   └── ...            # Other pieces
└── sounds/             # Sound effects
    ├── move.wav
    ├── checkmate.wav
    ├── rook_sacrifice.wav
    └── ...
```

## Game Architecture

# ChessEngine.py

GameState: Manages the board, pieces, and game rules
Move: Represents individual chess moves
CastleRights: Tracks castling permissions

# ChessMain.py

SimpleChess: Main game class handling graphics and user input
Graphics: Board rendering and piece display
Input: Mouse and keyboard event handling


## Technical Implementation

- **Game Engine**: Custom chess logic with advanced features like pin detection
- **Graphics**: Pygame-based GUI with 512x512 pixel board
- **Architecture**: Clean separation between game logic and presentation
- **Move Validation**: Comprehensive legal move checking prevents illegal moves
- **Chess Notation**: Supports standard algebraic notation output


## Future plans and Contributing

Potential improvements you could add:

AI opponent
Online multiplayer
Move history display
Time controls
Tournament mode
Better graphics and animations
Save/load game functionality


Feel free to fork this project and submit pull requests for improvements!

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with Python and Pygame* 🐍♟️
