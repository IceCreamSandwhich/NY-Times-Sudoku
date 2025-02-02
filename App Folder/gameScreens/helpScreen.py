from cmu_graphics import *

##################################
# helpScreen
##################################
def helpScreen_onAppStart(app):
    app.label = '''How to play Sudoku\n
Fill each 3 x 3 set with numbers 1–9.\n
Tap a cell in any set, then select a number.\n
Fill cells until the board is complete. Numbers in sets, rows or columns cannot repeat.\n
Note: Each number can only appear on the board 9 times.\n
Play modes and tips\n
Normal mode: Add 1 number to a cell.\n
Candidate mode: Add several numbers to a cell (for multiple options).\n
Need a clue? Tap -> "Hint" to see the next logical cell to solve.\n
Choose from 5 levels — easy, medium, hard, expert and evil. To change levels, tap "s".
'''
def helpScreen_onKeyPress(app, key):
    if key == 'p': setActiveScreen('playScreen')
    if key == 's': setActiveScreen('splashScreen')

def helpScreen_redrawAll(app):
    drawLabel('Here are some Helpful Tips!', app.width/2, 10, size = 16)
    i = 0
    for line in app.label.split('\n'):
        cx = app.width/2
        cy = 50 + i*10
        i += 1
        b = True if i == 0 else False 
        drawLabel(line, cx, cy, bold = b, size = 14)
    
