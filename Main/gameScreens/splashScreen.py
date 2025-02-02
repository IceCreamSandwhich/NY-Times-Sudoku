from cmu_graphics import *
from playScreen import State, minimumLegals
import copy 
import random

#################################
# splashScreen
#################################
class Button:
    def __init__(self, left, top, width, height, label, index):
        self.left = left
        self.top = top
        self.width, self.height = width, height
        self.label = label
        self.buttonIndex = index
        self.colorList = ['green', 'orange', 'red', 'purple', 'black']
        self.color = self.colorList[self.buttonIndex % len(self.colorList)]
        self.fill = None
        if self.label == 'x':
            self.size = 20
        else: self.size = 12 
        
    def draw(self):
        drawRect(self.left, self.top, self.width, self.height, fill=self.fill, border=self.color)
        if self.label == 'Candidate Mode':
            if app.candidateMode:
                drawLabel(app.checkMark, self.left + self.width // 2, self.top + self.height // 2, fill ='black', size=32,font = 'symbols')
        else:
            drawLabel(self.label, self.left + self.width // 2, self.top + self.height // 2, fill=f'{self.color}', size = 16)
        

    def doCandidateMoveLogic(self, app, mouseX, mouseY):
        if self.intersecting(app, mouseX, mouseY):
            if self.label == 'Candidate Mode':
                app.candidateMode = True
                self.fill ='plum'
                self.label = app.checkMark
            elif self.label == app.checkMark:
                app.candidateMode = False
                self.label = 'Candidate Mode'
                self.fill = None


    #Hint button Press logic        
    def doHintLogic(self, app, mouseX, mouseY):
        result = minimumLegals(app.currState, app.currState.board)
        if result == None: return None
        row, col = result
        if self.intersecting(app,mouseX,mouseY):
            if self.label == 'Hint':
                if app.drawHint == False:
                    app.currState.selectedCell = (row, col)
                app.drawHint = not app.drawHint
                
                
    #Toggling Auto and Manual Modes
    def doAutoManualLogic(self, app, mouseX, mouseY):
        color = rgb(255, 0, 255) #rose color
        if self.intersecting(app, mouseX, mouseY):
            if self.label == 'Normal':
                app.autoMode = True
                self.fill = color
                self.label = 'Auto'
                app.currState.resetAllLegals()
            elif self.label == 'Auto': 
                app.autoMode = False
                self.label = 'Normal'
                self.fill = None

    #Key Pad Logic 
    def doKeypadLogic(self, app, mouseX, mouseY):
        validLabels = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        if self.intersecting(app, mouseX, mouseY):
            if str(self.label) in validLabels:
                self.color = 'plum'
                app.currState.set(app, self.label)
            elif self.label == 'x':
                app.currState.delete() 
    
    def intersecting(self, app, mouseX, mouseY):
        return (self.left <= mouseX <= self.left + self.width and 
                self.top <= mouseY <= self.top + self.height)
    
    def setGameBoard(self, app):
        buttonNames = ['easy', 'normal', 'hard', 'expert', 'evil']
        if self.label in buttonNames:    
            app.mode = self.buttonIndex
            selectRandomBoard(app, app.mode)
        setActiveScreen('playScreen')
            
    def __repr__(self):
        return f'{self.label} button'
        
    def doMusicAndTwirl(self):
        ''' music based on difficulty level '''
        if self.intersecting:
            self.playMusic()

        #Changing Screens logic:
    def BackgroundLogic(self, app, mouseX, mouseY):
        if self.intersecting(app, mouseX, mouseY):
            app.highlightedButton = self.label
            app.drawBackground = True
        else:
            if app.highlightedButton == self.label:
                app.drawBackground = False
                app.highlightedButton = None

    def drawBackground(self, app):
        if self.label == app.highlightedButton:
            if self.label == 'easy':
                drawImage(app.easyBackground, 0, 0)
            elif self.label == 'normal':
                drawImage(app.mediumBackground, 0, 0)
            elif self.label == 'hard':
                drawImage(app.hardBackground, 0, 0)
            elif self.label == 'expert':
                drawImage(app.expertBackground, 0, 0)
            elif self.label == 'evil':
                drawImage(app.evilBackground, 0, 0)
                
    def playMusic(self):
        pass

##########
#Functions outside of button class
##########
def convertStrToBoard(data:str):
    board = []
    for line in data.splitlines():
        temp = []
        for val in line:
            if not val.isspace():
                temp.append(int(val))
        board.append(temp)
    return board

#Create all of my uiShapes
def createButtons(app):
    buttonList = []
    right = app.currState.boardLeft + app.currState.boardWidth
    top = app.currState.boardTop
    offSet = 30 
    buttonWidth, buttonHeight = 75, 50
    normalButton = Button(right+offSet, top, buttonWidth, buttonHeight, 'Normal', 4)
    nW = (right+offSet + buttonWidth)
    hintButton = Button((nW + 5), top, buttonWidth, buttonHeight, 'Hint', 4) 
    buttonList.append(normalButton)
    buttonList.append(hintButton) 
    
    #drawing numberPad
    nums = [[1,2,3],[4,5,6],[7,8,9]]
    space = 10
    tOffSet = (top + buttonHeight + space)
    LoffSet = right + offSet
    buttonWidth = 45
    buttonHeight = 45
    for row in range(len(nums)):
        for col in range(len(nums[0])):
            T = tOffSet + (buttonHeight + space) * row
            L = LoffSet + (buttonWidth + space) * col
            button = Button(L,T,buttonHeight, buttonWidth, nums[row][col],4)
            buttonList.append(button)
    deleteButton = Button(LoffSet, (top + buttonHeight + space) + (space*4 +buttonHeight*3), (buttonWidth + space) * 3, buttonHeight, 'x', 4)
    buttonList.append(deleteButton)
    
    candidateModeButton = Button(LoffSet, (top + buttonHeight*2 + space*2) + (space*4 + buttonHeight*3), 10, 10, 'Candidate Mode', 4)
    buttonList.append(candidateModeButton)
    return buttonList     

def selectRandomBoard(app, mode):
    # Randomly select a board of the specified difficulty
    app.candidateBoard = random.choice(app.boardLevels[mode])
    app.ogGamePlayBoard = convertStrToBoard(app.candidateBoard)
    app.currState = State(copy.deepcopy(app.ogGamePlayBoard))
    app.UiButtons = createButtons(app)
    
def makeScreenButton(app):
    offSet = app.width//10
    size = app.width // 6
    left = 0 + offSet//2
    top = app.height - app.height // 2 - 50
    buttons = [
        Button(left, top, size, size, 'easy', 0), 
        Button(left + size + 10, top, size, size, 'normal', 1),
        Button(left + size*2 + 10*2, top, size, size, 'hard', 2),
        Button(left + size*3 + 10*3, top, size, size, 'expert', 3),
        Button(left + size*4 + 10*4, top, size, size, 'evil', 4)
    ]
    return buttons

#################################
# app variables 
#################################
def splashScreen_onScreenActivate(app):
    width, height = 800, 600
    app.buttons = makeScreenButton(app)
    app.checkMark = chr(0x2713)
    app.drawBackground = False
    app.highlightedButton = None
    app.music.play(loop = True)
    
 
def splashScreen_onAppStart(app):
    app.drawHint = False

def splashScreen_onMousePress(app, mouseX, mouseY):
    for button in app.buttons:
        if button.intersecting(app, mouseX, mouseY):
            button.setGameBoard(app)
            
def splashScreen_onMouseMove(app,mouseX,mouseY):
    for b in app.buttons:
        b.BackgroundLogic(app,mouseX,mouseY)

def splashScreen_onKeyPress(app, key):
    if key == 'p': setActiveScreen('playScreen')
    elif key == 'h': setActiveScreen('helpScreen')

def splashScreen_redrawAll(app):
    if app.drawBackground and app.highlightedButton:
        for button in app.buttons:
            button.drawBackground(app)
    for button in app.buttons:
        button.draw()  
            