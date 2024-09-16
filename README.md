# Bust The Ghost

Bust The Ghost is an interactive game that challenges players to locate a hidden ghost on a grid using probabilistic inference. This project was developed as part of the Intro to AI (CSC 4301) course.

## Game Description

In Bust The Ghost, players attempt to locate a ghost hidden within a 9x12 grid. The game uses a probabilistic model to provide feedback on the ghost's location, updating probabilities based on the player's actions.

### Key Features:
- Interactive 9x12 grid
- Color-coded feedback system
- Probabilistic inference using Bayesian updating
- Limited number of "bust" attempts
- Credit system for actions

## How to Run

1. Ensure you have Python 3.x installed on your system.
2. Install the required dependencies:
   ```
   pip install PyQt5 numpy
   ```
3. Navigate to the project directory:
   ```
   cd path/to/Bust-The-Ghost
   ```
4. Run the main script:
   ```
   python main.py
   ```

## How to Play

1. Click on grid cells to receive color-coded feedback:
   - Red: Very close to the ghost
   - Orange: Close to the ghost
   - Yellow: Moderately far from the ghost
   - Green: Far from the ghost
2. Use the "Peep" checkbox to view probability distributions across the grid.
3. When you think you've located the ghost, enter the X and Y coordinates and click "Bust".
4. You have a limited number of "bust" attempts and credits, so choose wisely!

## Implementation Details

- The game uses Bayesian inference to update probabilities based on sensor readings.
- The Chebyshev distance is used to determine proximity to the ghost.
- PyQt5 is used for the graphical user interface.
- Numpy is used for efficient probability calculations.

## Files Description

- `main.py`: Entry point of the application
- `gui.py`: Contains the GUI implementation using PyQt5
- `game_logic.py`: Implements the core game logic and probabilistic inference
- `config.py`: Stores game configuration parameters

## Authors

- Omar Laaziri
