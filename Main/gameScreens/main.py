from cmu_graphics import *
from helpScreen import *
from playScreen import *
from splashScreen import *
from cmu_cpcs_utils import *
import os 
import random
import copy
from PIL import Image
import os, pathlib
''' Citations: 
    - CMU CS Academy for cell selection code and blocks are legal function
    - 15112 TP Resources for randomBoard Selection generation and screen switching music and images
    - W3 Schools (https://www.w3schools.com/python/ref_dictionary_items.asp)
        for learning about d.items()
    - ChatGPT for red cirlce dot placement math 
    - PicMonkey for pink color RGB (https://www.picmonkey.com/colors/pink)
    - easyMode background: https://www.crossroadsinitiative.com/media/articles/heavens-green-pastures/
    - normalMode background: https://www.godaddy.com/domainsearch/find?domainToCheck=dragoart.com&isc=GPPTCOM&itc=parkedpage_landers&key=parkweb&tmskey=dpp_dbs&utm_campaign=x_dom-auctions_parkedpages_x_x_invest_b_001&utm_medium=parkedpages&utm_source=godaddy
    - hardMode background: https://teamoyeniyi.com/2015/03/11/hey-doctors-heres-a-new-medical-condition-tough-cookie-syndrome/
    - expertMode background: https://www.pinterest.com/pin/300474606370071009/
    - evilMode background: https://playground.com/search?q=angry+evil+king+on+epic+throne
    - background Music: https://freepd.com/
'''
##################################
# App & boardConversion Logic
##################################
def readFile(path):
    with open(path,'r') as f:
        return f.read()

def getBoardsFromFile(path): #gives you 2dList of boardLevels as multiLine Strings from the tp starter files (path)
    easyBoards = []
    mediumBoards = []
    hardBoards = []
    expertBoards = []
    evilBoards = []
    for filename in os.listdir(path):
        if filename.startswith('easy'):
            # ptf = 'sudoku-starter-files\tp-starter-files\boards\easy-01.png.txt'
            pathToFile = f'..\\sudoku-starter-files\\tp-starter-files\\boards\\{filename}'
            fileContents = readFile(pathToFile)
            easyBoards.append(fileContents)
        elif filename.startswith('medium'):
            pathToFile = f'..\\sudoku-starter-files\\tp-starter-files\\boards\\{filename}'
            fileContents = readFile(pathToFile)
            mediumBoards.append(fileContents)
        elif filename.startswith('hard'):
            pathToFile = f'..\\sudoku-starter-files\\tp-starter-files\\boards\\{filename}'
            fileContents = readFile(pathToFile)
            hardBoards.append(fileContents)
        elif filename.startswith('expert'):
            pathToFile = f'..\\sudoku-starter-files\\tp-starter-files\\boards\\{filename}'
            fileContents = readFile(pathToFile)
            expertBoards.append(fileContents)
        elif filename.startswith('evil'):
            pathToFile = f'..\\sudoku-starter-files\\tp-starter-files\\boards\\{filename}'
            fileContents = readFile(pathToFile)
            evilBoards.append(fileContents)
    allBoards = [easyBoards, mediumBoards, hardBoards, expertBoards, evilBoards]
    return allBoards
     

def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)

def load2DBoard(app):
    # Load boards into a 2d list categorized by difficulty
    app.boardLevels = getBoardsFromFile('..\\sudoku-starter-files\\tp-starter-files\\boards')

def onAppStart(app):
    load2DBoard(app)
    app.mode = 0
    app.easyBackground = CMUImage(Image.open('Image Files\\easyMode.jpg'))
    app.mediumBackground = CMUImage(Image.open('Image Files\\normalMode.jpg'))
    app.hardBackground = CMUImage(Image.open('Image Files\\hardMode.jpg'))
    app.expertBackground = CMUImage(Image.open('Image Files\\expertMode.jpg'))
    app.evilBackground = CMUImage(Image.open('Image Files\\evilMode.jpg'))
    app.music = loadSound('Image Files\\easyMusic.mp3')


##################################
# main
##################################
def main():
    runAppWithScreens(initialScreen='splashScreen', width = 800, height = 600)
main()

