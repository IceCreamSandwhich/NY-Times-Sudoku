from cmu_graphics import *
from cmu_cpcs_utils import *
import copy
import random
import math
class State: #Manges the state of the game and gamePlayLogic 
    def __init__(self, board):
        self.board = board
        #Drawing values 
        self.boardRows, self.boardCols = len(self.board), len(self.board[0])
        self.boardWidth = 400
        self.boardHeight = 400
        self.resizeAmount = 0.2
        self.boardLeft = app.width*self.resizeAmount- self.boardWidth*self.resizeAmount
        self.boardTop = app.width*self.resizeAmount- self.boardHeight*self.resizeAmount
        self.cellBorderWidth = 1
        self.boardRight = self.boardLeft + self.boardWidth 
        self.boardBottom = self.boardHeight + self.boardTop
        self.opacity = 100
        
        #GamePlay values
        self.mutableCells = self.getMutables()#set of vals on boards that can be changed 
        self.legalValues = self.getLegalVals()#Dictionary of legal values for each mutable cell on the board
        self.ogLegals = copy.deepcopy(self.legalValues)
        self.selectedCell = (0,0)
        self.incorrectCells = set()
        self.gameOver = False
        app.stepsPerSecond = 10  
                
    def __repr__(self):
        return f'GameState --> difficulty: {app.mode}'
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        return isinstance(other, State) and self.board == other.board
    
    def getMutables(self): #needs to only be done once for the og board that is first passed in. consider this more 
        rows, cols = len(self.board), len(self.board[0])
        s = set()
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] == 0: s.add((row,col))
        return s 
    
    def getLegalVals(self):
        sudokuPossiblities = {1,2,3,4,5,6,7,8,9}
        legals = dict()
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                cell = (row, col)
                if cell in self.mutableCells:
                    takenVals = set()
                    for location in self.getCellRegions(cell):
                        x,y = location
                        if self.board[x][y] != 0:
                            takenVals.add(self.board[x][y])
                    actualLegals = sudokuPossiblities - takenVals 
                    legals[cell] = actualLegals
        return legals
    
    def getCellRegions(self, t:tuple):
        sameRow = self.getRowRegion(t)
        sameCols = self.getColRegion(t)
        same3x3 = self.get3x3Region(t)
        return sameRow|sameCols|same3x3

    def getRowRegion(self, t):
        currRow, currCol = t
        s = set()
        for col in range(self.boardCols):
            s.add((currRow, col))
        return s
    
    def getColRegion(self,t):
        currRow, currCol = t
        s = set()
        for row in range(self.boardCols):
            s.add((row, currCol))
        return s
        
    def get3x3Region(self,t):
        currRow, currCol = t
        s = set()
        startRow, startCol = (currRow // 3) * 3, (currCol // 3) * 3
        for i in range(3):
            for j in range(3):
                cell = (startRow + i, startCol + j) 
                s.add(cell)
        return s
        
    ###################
    # Game State changing Logic 
    ###################
    def moveSelection(self, drow, dcol):
        if self.selectedCell != None:
            selectedRow, selectedCol = self.selectedCell
            newSelectedRow = (selectedRow + drow) % self.boardRows
            newSelectedCol = (selectedCol + dcol) % self.boardCols
            self.selectedCell = (newSelectedRow, newSelectedCol)
            
    def clickChangeSelection(self, app, mouseX, mouseY):
        selectedCell = self.getCell(mouseX, mouseY)
        if selectedCell != None:
            self.selectedCell = selectedCell
    
    def set(self, app, value: int): #takes a tuple of position on board allows player to change it and updates legalsValues dict 
        row, col = self.selectedCell
        curr = self.board[row][col]
        if  (row,col) in self.mutableCells:
            if not app.candidateMode:
                self.board[row][col] = value               
                self.removeLegals(row, col, value)
                #Logic behind deciding which player input cells are incorrect     
                if self.board[row][col] != app.solvedBoard[row][col]:
                    self.incorrectCells.add((row, col))
                if self.board[row][col] == app.solvedBoard[row][col] and (row,col) in self.incorrectCells:
                    self.incorrectCells.remove((row,col))
                if self.board[row][col] == app.solvedBoard[row][col]:# make the cell Immutable
                    self.mutableCells.remove((row, col))
                    del (self.legalValues[(row,col)])    
            else: #in candidate mode
                cell = (row, col)
                legalSet = self.legalValues[cell]
                if cell in self.legalValues: #mutable cell, that has an existing legal
                    if value not in legalSet:
                        self.legalValues[cell].add(value)
                    else:
                        self.legalValues[cell].remove(value)
                    # self.removeLegals(row, col, value)
    
    def removeLegals(self, row, col, legal): 
        if not app.candidateMode:
            if app.autoMode:
                cellNeighbors = self.getCellRegions((row, col))
                for cell in cellNeighbors:
                    if cell in self.legalValues and legal in self.legalValues[cell]: 
                        self.legalValues[cell].remove(legal)
            if not app.autoMode: #else normal legals
                cell = (row, col)
                if cell in self.legalValues and legal in self.legalValues[cell]:
                    self.legalValues[cell].remove(legal)
        
        else: #in candidate Mode
            cell = (row, col)
            if cell in self.legalValues:
                self.legalValues[cell].remove(legal)

                
    def resetLegals(self, row, col, value): #reset the legals on backspace/delete
        if not app.candidateMode:
            if app.autoMode: #could not quite get this working
                self.resetAllLegals()            
            else:
                cell = (row,col)
                if cell in self.legalValues: #check if the cell is legal
                    #generate valid legals for a given cell and only add the potential value if its within the valid legals
                    takenVals = set()
                    sudokuPossiblities = {1,2,3,4,5,6,7,8,9}
                    for location in self.getCellRegions(cell):
                        x,y = location
                        if self.board[x][y] != 0:
                            takenVals.add(self.board[x][y])
                    actualLegals = sudokuPossiblities - takenVals 
                    if value in actualLegals:
                        self.legalValues[cell].add(value)

    def delete(self):  # deletes vals from mutableCells
        row, col = self.selectedCell
        if not app.candidateMode:
            if app.autoMode == True:
                value = self.board[row][col] 
                if value != 0 and (row, col) in self.mutableCells:
                    self.board[row][col] = 0
                    self.resetAllLegals()
                    if (row, col) in self.incorrectCells:
                        self.incorrectCells.remove((row, col))
            else:
                value = self.board[row][col] 
                if value != 0 and (row, col) in self.mutableCells:
                    self.board[row][col] = 0
                    self.resetLegals(row, col, value)
                    if (row, col) in self.incorrectCells:
                        self.incorrectCells.remove((row, col))
    def resetAllLegals(self):
        self.legalValues = copy.copy(self.ogLegals)
        
    def getCell(self, x, y):
        dx = x - self.boardLeft
        dy = y - self.boardTop
        cellWidth, cellHeight = self.getCellSize()
        row = math.floor(dy / cellHeight)
        col = math.floor(dx / cellWidth)
        if self.onBoard(row,col):
            return (row, col)
        else:
            return None             
    
    def checkGameOver(self):
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                if self.board[row][col] != app.solvedBoard[row][col]:
                    return False
        return True
    
    def onBoard(self, row, col):
        return (0 <= row < 9) and (0 <= col < 9)
    
    #####################
    #drawing Methods
    #####################
    def draw(self):
        self.drawBoard(self)
        self.drawBoardBorder(self)    
    def drawBoard(self):
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                self.drawCell(app, row, col)
        self.draw3x3Blocks(app) 
    def drawBoardBorder(self):
        # draw the board outline (with double-thickness):
        drawRect(self.boardLeft, self.boardTop, self.boardWidth, self.boardHeight,
                fill=None, border='black',
                borderWidth=3*self.cellBorderWidth) 
    def draw3x3Blocks(self, app):
        cellWidth, cellHeight = self.getCellSize()
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                cx = self.boardLeft + j * cellWidth
                cy = self.boardTop + i * cellHeight
                drawRect(cx, cy, cellWidth*3, cellHeight*3, 
                        fill=None, border='black', borderWidth=2)    
    def drawCell(self, app, row, col):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellWidth, cellHeight = self.getCellSize() 
        if (row, col) == self.selectedCell:
            color = 'gold'
        else:
            if self.board[row][col] != 0 and (row, col) not in self.mutableCells:
                color = 'lightgray'  
            else: color = None
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
                fill=color, border='gray',
                borderWidth = self.cellBorderWidth, opacity = self.opacity)
        if self.board[row][col] != 0:
            drawLabel(self.board[row][col], cellLeft + cellWidth//2, cellTop + cellHeight//2, size=16, opacity = self.opacity)
        self.drawLegals((row, col))
        self.drawRedDots(app, row, col)
        self.drawHint(app,row,col)
        
    def drawHint(self, app, row, col):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellWidth, cellHeight = self.getCellSize()
        if app.drawHint == True:
            app.UiButtons[1].fill = 'lightBlue'
            if (row,col) == minimumLegals(app.currState, app.currState.board):
                cx = cellLeft + cellWidth * 0.85  # Slightly offset from the right edge
                cy = cellTop + cellHeight * 0.85  # Slightly offset from the bottom edge
                radius = 5
                drawCircle(cx, cy, radius, fill='lightBlue')
        else: app.UiButtons[1].fill = None   
              
    def drawRedDots(self, app, row, col):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellWidth, cellHeight = self.getCellSize()
        if (row, col) in self.incorrectCells:
            cx = cellLeft + cellWidth * 0.85  # Slightly offset from the right edge
            cy = cellTop + cellHeight * 0.85  # Slightly offset from the bottom edge
            radius = 5
            drawCircle(cx, cy, radius, fill='red')  
    
    def getCellLeftTop(self, row, col):
        cellWidth, cellHeight = self.getCellSize()
        cellLeft = self.boardLeft + col * cellWidth
        cellTop = self.boardTop + row * cellHeight
        return (cellLeft, cellTop)
    
    def getCellSize(self):
        cellWidth = self.boardWidth / self.boardCols
        cellHeight = self.boardHeight / self.boardRows
        return (cellWidth, cellHeight)
    
    def drawLegals(self, t:tuple):
        row, col = t
        if t in self.legalValues:
            valsToBeDrawn = self.legalValues[t]
            left, top = self.getCellLeftTop(row, col)
            width, height = self.getCellSize()
            offSet = width // 6
            smallerLeft, smallerTop = left + offSet, top + offSet + 3
            smallerWidth, smallerHeight = width - 2 * offSet, height - 2 * offSet
            for i in valsToBeDrawn:  # Draw only the legal values
                if i % 3 == 1:  # Drawing 1, 4, 7
                    cx = smallerLeft
                    cy = smallerTop + ((i - 1) // 3) * (smallerHeight // 3 + 2)
                elif i % 3 == 2:  # Drawing 2, 5, 8
                    cx = smallerLeft + smallerWidth // 2
                    cy = smallerTop + ((i - 1) // 3) * (smallerHeight // 3 + 2)
                elif i % 3 == 0:  # Drawing 3, 6, 9
                    cx = smallerLeft + smallerWidth
                    cy = smallerTop + ((i // 3 - 1) * (smallerHeight // 3 + 2))
                drawLabel(i, cx, cy, size=int(width * 0.2), opacity = self.opacity)
                
#######################################################
#General App level functions outside of oop
#######################################################

#HintSettingLogic
def doHint(app):
    result = minimumLegals(app.currState, app.currState.board)
    if result is not None:
        row, col = result
        answer = app.solvedBoard[row][col]
        app.currState.selectedCell = (row, col)
        app.currState.set(app, int(answer))

def minimumLegals(state, board):
    if not app.gameOver:
        bestCount = 1000000
        bestRowCol = None
        dic = state.legalValues
        for t, legals in dic.items(): #use automatic legals
            legalCount = len(legals)
            if legalCount < bestCount and legalCount != 0:
                bestCount = legalCount
                bestRowCol = t
        return bestRowCol
    return None

#backTracking Board Solver
def solveSudoku(state):
    return solveSudokuHelper(copy.deepcopy(state), copy.deepcopy(app.currState.board))
    
def solveSudokuHelper(state, b):
    if fullBoard(b) and isLegalSudoku(b):  # Base case: board is full and legal
        return b
    else:
        result = minimumLegals(state, b)
        if result == None: return None
        row, col = result
        legalSet = state.legalValues.get((row,col))
        oldLegs = copy.copy(legalSet)
        for val in legalSet:
            b[row][col] = val
            state.legalValues[(row,col)] = set()
            if isLegalSudoku(b):
                sol = solveSudokuHelper(state, b)
                if sol is not None:
                    return sol
            # Undo the move here if nothing good is found
            b[row][col] = 0
            state.legalValues[(row,col)] = oldLegs
        return None

def fullBoard(board):
    for row in board:
        if 0 in row: return False
    return True
            
def isLegalSudoku(grid):
    #legal checks
    rows, cols = len(grid), len(grid[0])
    if rows != cols:
        return False
    if (rows !=9) and (cols!=9):
        return False
    return rowsAreLegal(grid) and colsAreLegal(grid) and blocksAreLegal(grid)  

def rowsAreLegal(grid): #if all rows are legal
    for rowList in grid:
        if not areLegalValues(rowList):
            return False
    return True
        
def colsAreLegal(grid): #all cols are legal
    rows, cols = len(grid), len(grid[0])
    for col in range(cols):
        colList = [grid[row][col] for row in range(rows)]
        if not areLegalValues(colList): return False 
    return True
    
def blocksAreLegal(grid): # all blocks are legal
    rows, cols = len(grid), len(grid[0])
    blocks = rows
    blockSize = int(blocks ** 0.5)
    for blockNum in range(rows):
        startRow = blockNum // blockSize * blockSize
        startCol = blockNum % blockSize * blockSize
        blockList = []
        for row in range(startRow, startRow + blockSize):
            for col in range(startCol, startCol + blockSize):
                blockList.append(grid[row][col])
        if not areLegalValues(blockList):
            return False
    return True
                
def areLegalValues(values):
    n = len(values)
    for value in values:
        if type(value) != int:
            return False
        if (value < 0) or (value > n):
            return False
        if (value > 0) and values.count(value) != 1:
            return False
    return True


######################################################## 
#playScreen MVC Functions
#######################################################
def playScreen_onAppStart(app):
    app.gameStates = []
    app.stepsPerSecond = 1
    app.gameOver = False
    app.autoMode = False
    app.candidateMode = False
    app.revealBoard = False
    app.counter = 0
    app.autoSolve = False
    
def playScreen_onScreenActivate(app):
    app.solvedBoard = solveSudoku(app.currState)

def playScreen_onKeyPress(app, key):
    #Debugging purposes:
    if key == 'escape' and app.drawHint == True: doHint(app)
    if key == 'y': app.candidateMode = not app.candidateMode
    if key == 'h': setActiveScreen('helpScreen')
    if key == 's': setActiveScreen('splashScreen')
    if key == 'm':  # Toggle manual mode for legals
        app.autoMode = not app.autoMode
    if key == 'c': app.autoSolve = True

    if key == 'r' and app.gameOver == True: setActiveScreen('splashScreen')

        
    if key == 'left':    app.currState.moveSelection(0, -1)
    elif key == 'right': app.currState.moveSelection(0, +1)
    elif key == 'up':    app.currState.moveSelection(-1, 0)
    elif key == 'down':  app.currState.moveSelection(+1, 0)
    if key in '123456789' and not app.gameOver:
        app.currState.set(app, int(key))
        app.gameStates.append(copy.deepcopy(app.currState.board)) #save state to gameStates for undo/redo s
        #check if its an incorrect value
    if (key == 'backspace' or key == 'delete') and not app.gameOver:
        app.currState.delete()
        app.gameStates.append(copy.deepcopy(app.currState.board))
    
def playScreen_onMousePress(app, mouseX, mouseY):
    app.currState.clickChangeSelection(app, mouseX, mouseY)
    for button in app.UiButtons:
        button.doKeypadLogic(app, mouseX, mouseY)
        button.doHintLogic(app,mouseX,mouseY)
        button.doAutoManualLogic(app, mouseX, mouseY)
        button.doCandidateMoveLogic(app,mouseX,mouseY)

def resetButtonDefaults(app):
    for button in app.UiButtons: #logic to reset button defaults (colors)
        if str(button.label) in ['1','2','3','4','5','6','7','8','9']:
            if app.counter % 10 == 0:
                    button.color = button.colorList[button.buttonIndex]
        if button.label == 'Hint': pass 
        
def playScreen_onStep(app):
    app.counter += 1
    if app.counter > 1000:
        app.counter = 0
    resetButtonDefaults(app)
    if app.currState.checkGameOver() == True:
        app.gameOver = True 
    if app.autoSolve == True:
        doHint(app)

def playScreen_redrawAll(app):
    app.currState.drawBoard()
    app.currState.drawBoardBorder()
    for button in app.UiButtons:
        button.draw()
    #Draw candidateMode next to checkBox and a checkMark on top
    drawLabel('Candidate Mode', (app.UiButtons[-1].left + app.UiButtons[-1].width*6), (app.UiButtons[-1].top + app.UiButtons[-1].height//2))
    if app.candidateMode == True:
            checkMark = chr(0x2713)
            drawLabel(checkMark, (app.UiButtons[-1].left + app.UiButtons[-1].width//2), (app.UiButtons[-1].top + app.UiButtons[-1].height//2), font='symbols')
    drawLabel('Sudoku!', app.width//2, 0+20, size = 16)
    if app.gameOver:
        drawGameOver(app)

def drawGameOver(app):
    app.currState.opacity = 15
    drawRect(app.width//2, app.width//2-app.width//6, 350, 200, border = 'black', fill = 'white', align = 'center')
    drawLabel('You Won! press r to play again', app.width//2, app.width//2- 100, size = 20)
