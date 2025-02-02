Welcome to 112 Ny Times Sudoku! 

Project Description:
    For Carnegie Mellon Universities 15112 Term Project, I made the game Sudoku.
Inspired from the the newYork times version of the game.

You need a few modules to run the game:
    1. cmu_graphics
    2. os 
    3. random
    4. copy

Setup:
    1. Download the follwing files and folders:
        -  cmu_cpcs_utils.py.: https://www.cs.cmu.edu/~112-n24/notes/tp/cmu_cpcs_utils.py
        -  sudoku-starter-files: https://www.cs.cmu.edu/~112-n24/notes/tp/sudoku-starter-files.zip
    2. Create folder called gameScreens that includes the following python files
        - helpScreen.py
        - main.py
        - playScreen.py
        - splashScreen.py
        - cmu_cpcs_utils.py
        - The folder for sudoku-starter-files
    3. For each file below, have the following imports:
        - main.py: 
            from cmu_graphics import *
            from helpScreen import *
            from playScreen import *
            from splashScreen import *
            from cmu_cpcs_utils import *
            import os 
            import random
            import copy
        - splashScreen.py:
            from cmu_graphics import *
            from playScreen import State 
            import copy 
            import random
        - helpScreen.py:
            from cmu_graphics import *
        - playScreen.py:
            from cmu_graphics import *
            from cmu_cpcs_utils import *
            import copy
            import random
            import math

Running the game and gameplay:
    The game should always be ran from main.py. Once you enter the game press
    press 'h' to enter the help screen which includes the rules for playing sudoku
    or select a difficulty level to start playing the game. Press 's' to switch
    to the level selection screen and press 'p' to switch to the gameScreen


