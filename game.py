import pygame
import sys, os
import numpy as np
import random
import threading

from sudoku import Sudoku
from button import Button
from button import SudokuButton
        

### GAME ###
class Game(object):
    """Runs sudoku game."""
    ## Constants
    WIDTH = 800
    HEIGHT = 600
    FPS = 30
    ## Colors
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    GRAY = (127,127,127)
    
    YELLOW = (255,255,0)
    MAGENTA = (255,0,255)
    CYAN = (0,255,255)
    LILAC = (200,162,200)
    VIOLET = (238,130,238)
    CREAM = (255,253,208)
    AQUAMARINE = (127,255,212)
    
    LIGHT_GRAY = (200,200,200)
    
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sudoku")
        self.clock = pygame.time.Clock()
        ## lists
        self.squares = [[None for i in range(9)] for j in range(9)]
        self.digitSquares = [None for i in range(10)]
        self.allButtons = []
        ## Key dictionaries and lists
        self.digitKeys = {pygame.K_0: 0, pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
                          pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7,
                          pygame.K_8: 8, pygame.K_9: 9}
        self.arrowKeys = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]
        ## button colors
        self.buttonColors = [self.GREEN, self.GREEN, self.GREEN, self.GREEN, self.GREEN,
                             self.GREEN, self.LILAC, self.GREEN, self.GREEN, self.GREEN]
        ## Fonts
        self.smallfont = pygame.font.SysFont("comicsansms", 25)
        self.medfont = pygame.font.SysFont("comicsansms", 45)
        self.largefont = pygame.font.SysFont("comicsansms", 80)

        self.smallfontbold = pygame.font.SysFont("comicsansms", 28, bold=True)
        
        ## variables
        self.win = False
        self.activeDigit = None
        self.activeSudokuSquare = None
        ## start menu
        self.mainMenu()

    ### GAME FUNCTIONS ###
    ## exits program
    def exitProgram(self):
        pygame.quit()
        sys.exit()
        #os._exit()

    ## defines sudoku area's and button's properties
    def sudokuArea(self):
        ## Create sudoku area
        # buttons
        self.squareWidth = 40
        self.squareHeight = 40
        # lines
        self.thinLineWidth = 5
        self.thickLineWidth = 10
        # main area
        self.sudokuBGX = 50
        self.sudokuBGY = 50
        self.sudokuBGColor = self.BLACK
        self.sudokuBGHeight = 9*self.squareHeight + 4*self.thickLineWidth + 6*self.thinLineWidth
        self.sudokuBGWidth = 9*self.squareWidth + 4*self.thickLineWidth + 6*self.thinLineWidth

    ## draws background of sudoku
    def drawSudokuBG(self):
        pygame.draw.rect(self.screen, self.sudokuBGColor,
                         [self.sudokuBGX, self.sudokuBGY, self.sudokuBGWidth, self.sudokuBGHeight])

    ## buttons functions
    # sudoku squares
    def createSudokuSquares(self):
        # x and y of buttons
        self.x = self.sudokuBGX
        self.y = self.sudokuBGY
        for blk in range(3):
            # increase x and y every block as thick line width
            self.x += self.thickLineWidth
            self.y += self.thickLineWidth
            for sqr in range(3):
                for row in range(3):
                    # look for every button
                    for col in range(3):
                        r = blk*3 + row%3 # row in range(0,9)
                        c = sqr*3 + col%3 # col in range(0,9)
                        # create button
                        if self.sudoku.resetBoard[blk,sqr,row,col] != 0:
                            self.square = SudokuButton(self.screen, self.x, self.y, self.squareWidth, self.squareHeight,
                                                 self.BLACK, self.LIGHT_GRAY, self.CYAN, self.GREEN,
                                                 sudokuRow=r, sudokuCol=c)
                        else:
                            self.square = SudokuButton(self.screen, self.x, self.y, self.squareWidth, self.squareHeight,
                                                 self.BLACK, self.WHITE, self.CYAN, self.GREEN,
                                                 sudokuRow=r, sudokuCol=c)
                            
                        self.square.font = self.smallfont
                        self.squares[r][c] = self.square
                        # update x and y after every square in a row
                        if col != 2:
                            self.x += self.thinLineWidth + self.squareWidth
                    #update x and y after every row
                    if row != 2:
                        self.x -= 2*(self.thinLineWidth + self.squareWidth)
                        self.y += self.thinLineWidth + self.squareHeight
                # update x and y after every 3x3 square
                if sqr != 2:
                    self.x += self.squareWidth + self.thickLineWidth
                    self.y -= 2*(self.thinLineWidth + self.squareHeight)
            # update x and y after every block
            self.x = self.sudokuBGX
            self.y += self.squareWidth                               
    
    def updateSquares(self):
        for r in range(9):
            for c in range(9):
                square = self.squares[r][c]
                blk = r//3
                sqr = c//3
                row = r%3
                col = c%3
                # update digit value of square
                digit = self.sudoku.playBoard[blk,sqr,row,col]
                self.squares[r][c].text = str(digit)
                # update square's pressed color by looking digit
                square.pressed_col = self.buttonColors[digit]
                # update if there is a pressed square to active square
                if square.pressed:
                    self.activeSudokuSquare = square
                # squares that have active digit are making like active,
                # to show same digits in sudoku to user
                if digit == self.activeDigit and digit != 0:
                    square.likePressed = True
                else:
                    square.likePressed = False
                # update square
                square.update()
                
                    
        # if sudoku square and a digit pressed, update sudoku square to digit
        if (self.activeDigit or self.activeDigit == 0) and self.activeSudokuSquare != None:
            self.getActiveSquareProperties()
            # look if digit can be placed in sudoku square
            if self.sudoku.resetBoard[self.blk,self.sqr,self.row,self.col] == 0:
                # look if digits are the same or not
                if self.activeDigit != self.sudoku.playBoard[self.blk,self.sqr,self.row,self.col]:
                    self.sudoku.playBoard[self.blk,self.sqr,self.row,self.col] = self.activeDigit
                    self.resetPressedValues()
                    self.activeDigit = None
                    self.activeSudokuSquare = None
                    self.resetActiveSquareProperties()
                
    def drawSquares(self):
        for row in self.squares:
            for square in row:
                square.draw()

    ## sudoku digits' buttons
    # defines digits' background
    def digitArea(self):
        # buttons
        self.digitWidth = 40
        self.digitHeight = 40
        # lines
        self.digitLineWidth = 5
        # main area
        self.digitBGX = self.sudokuBGX + self.sudokuBGWidth + 2*self.digitWidth
        self.digitBGY = self.sudokuBGY
        self.digitBGColor = self.BLACK
        self.digitBGHeight = 4*self.digitHeight + 5*self.digitLineWidth
        self.digitBGWidth = 3*self.digitWidth + 4*self.digitLineWidth

    # draws digits' background
    def drawDigitBG(self):
        pygame.draw.rect(self.screen, self.digitBGColor,
                         [self.digitBGX, self.digitBGY, self.digitBGWidth, self.digitBGHeight])

    # sudoku digits
    def createDigitSquares(self):
        self.x = self.digitBGX + self.digitLineWidth
        self.y = self.digitBGY + self.digitLineWidth
        for row in range(3):
            for col in range(3):
                self.digit = row*3 + col%3 + 1
                self.digitSquare = Button(self.screen, self.x, self.y, self.digitWidth, self.digitHeight,
                                          self.BLACK, self.WHITE, self.CYAN, self.GREEN,
                                          None, str(self.digit), self.smallfont)
                self.digitSquare.digit = self.digit
                self.digitSquares[self.digit-1] = self.digitSquare
                if col != 2:
                    # update x
                    self.x += self.digitWidth + self.digitLineWidth
            # update x and y
            if row != 2:
                self.x -= 2*(self.digitWidth + self.digitLineWidth)
                self.y += self.digitHeight + self.digitLineWidth
        # create delete digit button
        self.x -= self.digitHeight + self.digitLineWidth
        self.y += self.digitHeight + self.digitLineWidth
        self.delButton = Button(self.screen, self.x, self.y, self.digitWidth, self.digitHeight,
                                self.BLACK, self.WHITE, self.CYAN, self.GREEN,
                                None, "del", self.smallfont)
        self.delButton.digit = 0
        self.digitSquares[9] = self.delButton

    def updateDigitSquares(self):
        for button in self.digitSquares:
            button.update()
            # if pressing the button, update active digit
            if button.pressing:
                self.activeDigit = button.digit

    def drawDigitSquares(self):
        for button in self.digitSquares:
            button.draw()

    ### Create functional buttons ###
    ## reset button
    def createResetButton(self):
        self.resetButtonWidth = 100
        self.resetButtonHeight = 50
        self.resetButtonX = self.digitBGX
        self.resetButtonY = self.digitBGY + self.digitBGHeight + 2*self.digitHeight
        self.resetButton = Button(self.screen, self.resetButtonX, self.resetButtonY,
                                  self.resetButtonWidth, self.resetButtonHeight,
                                  self.BLACK, self.WHITE, self.CYAN, self.WHITE,
                                  lambda: self.resetSudoku(), "Reset", self.smallfont)

    ## done button
    def createDoneButton(self):
        self.doneButtonWidth = 100
        self.doneButtonHeight = 50
        self.doneButtonX = self.resetButtonX
        self.doneButtonY = self.resetButtonY + 2*self.doneButtonHeight
        self.doneButton = Button(self.screen, self.doneButtonX, self.doneButtonY,
                                 self.doneButtonWidth, self.doneButtonHeight,
                                 self.BLACK, self.WHITE, self.CYAN, self.WHITE,
                                 lambda: self.finishPage(), "Done", self.smallfont)
    
    ## List of All buttons
    def uniteAllButtons(self):
        for row in self.squares:
            for button in row:
                self.allButtons.append(button)
        for button in self.digitSquares:
            self.allButtons.append(button)
        self.allButtons.append(self.resetButton)

    ## update active digit and button by looking any button pressed or not
    def updateActives(self):
        self.anyPressed = False
        for button in self.allButtons:
            if button.pressed:
                self.anyPressed = True
                break
        if not self.anyPressed:
            self.activeDigit = None
            self.activeSudokuSquare = None
            self.resetActiveSquareProperties()

    ## get active sudoku square's row and column properties
    def getActiveSquareProperties(self):
        self.r = self.activeSudokuSquare.sudokuRow
        self.c = self.activeSudokuSquare.sudokuCol
        self.blk = self.r//3
        self.sqr = self.c//3
        self.row = self.r%3
        self.col = self.c%3

    ## set active sudoku square's properties to None
    def resetActiveSquareProperties(self):
        self.r = None
        self.c = None
        self.blk = None
        self.sqr = None
        self.row = None
        self.col = None

    ## set pressed values of all buttons to False
    def resetPressedValues(self):
        for button in self.allButtons:
            if button.pressed:
                button.pressed = False

    ## reset sudoku function
    def resetSudoku(self):
        self.activeDigit = None
        self.activeSudokuSquare = None
        self.resetActiveSquareProperties()
        self.sudoku.playBoard = np.copy(self.sudoku.resetBoard)
        for button in self.allButtons:
            button.pressed = False

    ## put text to screen (x and y is center of the text)
    def textToScreen(self, x, y, text, color, font):
        textSurf = font.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.center = (x, y)
        self.screen.blit(textSurf, textRect)

    ## create sudoku
    def createSudoku(self):
        self.sudoku = Sudoku()
        self.sudoku.createPlayBoard()

    ## kill sudoku creating process and go to main menu
    def kill_goMainMenu(self):
        self.sudoku.kill()
        self.mainMenu()
        

    ### PAGES ###
    ## main menu
    def mainMenu(self):
        ## set win to false
        self.win = False
        ## create menu buttons
        self.menuButtonWidth = 120
        self.menuButtonHeight = 80
        self.playButton = Button(self.screen, int((self.WIDTH-self.menuButtonWidth)/2), 200,
                                 self.menuButtonWidth, self.menuButtonHeight,
                                 self.BLACK, self.AQUAMARINE, self.CYAN, self.GREEN,
                                 lambda: self.creatingSudokuPage(), "Play", self.medfont)
        self.exitButton = Button(self.screen, int((self.WIDTH-self.menuButtonWidth)/2), 400,
                                 self.menuButtonWidth, self.menuButtonHeight,
                                 self.BLACK, self.LILAC, self.CYAN, self.GREEN,
                                 lambda: self.exitProgram(), "Exit", self.medfont)
                                 
        self.mainMenuRun = True
        while self.mainMenuRun:
            ## Running speed (fps)
            self.clock.tick(self.FPS)
            
            ## Process inputs (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.mainMenuRun = False
                
            ## Update    
            self.playButton.update()
            self.exitButton.update()

            ## Draw (render)
            self.screen.fill(self.CREAM)
            self.playButton.draw()
            self.exitButton.draw()
            
            # after drawing everything, flip the display
            pygame.display.flip()

        self.exitProgram()

    ## creating sudoku page
    def creatingSudokuPage(self):
        ## set win to false
        self.win = False
        ## create sudoku as a background process
        self.creatingThread = threading.Thread(target=self.createSudoku, args=())
        self.creatingThread.start()

        # buttons
        self.menuButtonWidth = 230
        self.menuButtonHeight = 80
        self.playButton = Button(self.screen, int((self.WIDTH-self.menuButtonWidth)/2), self.HEIGHT/2+100,
                                 self.menuButtonWidth, self.menuButtonHeight,
                                 self.BLACK, self.AQUAMARINE, self.CYAN, self.GREEN,
                                 lambda: self.gameLoop(), "Play", self.medfont)
        self.mainMenuButton = Button(self.screen, int((self.WIDTH-self.menuButtonWidth)/2), self.HEIGHT/2-200,
                                     self.menuButtonWidth, self.menuButtonHeight,
                                     self.BLACK, self.AQUAMARINE, self.CYAN, self.GREEN,
                                     lambda: self.kill_goMainMenu(), "Main Menu", self.medfont)

        ## creating page as a foreground process
        self.creating = True
        while self.creating:
            ## Running speed (fps)
            self.clock.tick(self.FPS)

            ## Process inputs (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.running = False
                    self.exitProgram()

            ## Update

            ## Draw (render)
            self.screen.fill(self.CREAM)

            if self.creatingThread.is_alive():
                self.textToScreen(self.WIDTH/2, self.HEIGHT/2, "Creating Sudoku...", self.BLACK, self.medfont)
                self.mainMenuButton.update()
                self.mainMenuButton.draw()
            else:
                self.textToScreen(self.WIDTH/2, self.HEIGHT/2, "Created Sudoku.", self.BLACK, self.medfont)
                self.mainMenuButton.update()
                self.mainMenuButton.draw()
                self.playButton.update()
                self.playButton.draw()
                
            # after drawing everything, flip the display
            pygame.display.flip()
            
    ## Game Loop
    def gameLoop(self):
        ## set win to false
        self.win = False
        ## set active sudoku square to false
        self.activeSudokuSquare = None
        ## create backgrounds,buttons and squares
        self.sudokuArea()
        self.createSudokuSquares()
        self.digitArea()
        self.createDigitSquares()
        self.createResetButton()
        self.createDoneButton()
        self.uniteAllButtons()
        
        self.running = True
        while self.running:
            ## Running speed (fps)
            self.clock.tick(self.FPS)

            ## Process inputs (events)
            
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN:
                    
                    # puts pressed digit key into active sudoku square
                    if (event.key in self.digitKeys.keys()) and self.activeSudokuSquare:
                        # get row and col values for active square
                        self.getActiveSquareProperties()
                        # look if digit can be placed in sudoku square
                        if self.sudoku.resetBoard[self.blk,self.sqr,self.row,self.col] == 0:
                            self.sudoku.playBoard[self.blk,self.sqr,self.row,self.col] = self.digitKeys[event.key]
                            self.activeDigit = None
                            self.activeSudokuSquare = None
                            
                    # moves active square up,down,left,right by keyboard
                    elif (event.key in self.arrowKeys) and self.activeSudokuSquare:
                        # get row and col values for active square
                        self.getActiveSquareProperties()
                        if event.key == pygame.K_UP and self.r > 0:
                            self.squares[self.r][self.c].pressed = False
                            self.r -= 1
                        elif event.key == pygame.K_DOWN and self.r < 8:
                            self.squares[self.r][self.c].pressed = False
                            self.r += 1
                        elif event.key == pygame.K_RIGHT and self.c < 8:
                            self.squares[self.r][self.c].pressed = False
                            self.c += 1
                        elif event.key == pygame.K_LEFT and self.c > 0:
                            self.squares[self.r][self.c].pressed = False
                            self.c -= 1
                        self.activeSudokuSquare = self.squares[self.r][self.c]
                        self.squares[self.r][self.c].pressed = True

            ## Update
            # update backgrounds and squares
            self.updateActives()
            self.updateSquares()
            self.updateDigitSquares()
            self.resetButton.update()
            self.doneButton.update()

            ## Draw (render)
            self.screen.fill(self.CREAM)
            # draw backgrounds and squares
            self.drawSudokuBG()
            self.drawSquares()
            self.drawDigitBG()
            self.drawDigitSquares()
            self.resetButton.draw()
            self.doneButton.draw()
            
            # after drawing everything, flip the display
            pygame.display.flip()

        self.exitProgram()
        
    ## Game finish page
    def finishPage(self):
        ## check win or lose
        ## create win or lose texts
        if self.sudoku.areBoardsSame(self.sudoku.playBoard, self.sudoku.sudokuSol):
            self.win = True
        else:
            self.win = False

        ## create buttons
        self.replayButton = Button(self.screen, int((self.WIDTH-self.menuButtonWidth)/2), 200,
                                    self.menuButtonWidth, self.menuButtonHeight,
                                    self.BLACK, self.AQUAMARINE, self.CYAN, self.GREEN,
                                    lambda: self.creatingSudokuPage(), "Replay", self.medfont)
                                    
        self.mainMenuButton = Button(self.screen, int((self.WIDTH-self.menuButtonWidth)/2), 320,
                                     self.menuButtonWidth, self.menuButtonHeight,
                                     self.BLACK, self.AQUAMARINE, self.CYAN, self.GREEN,
                                     lambda: self.mainMenu(), "Main Menu", self.medfont)
        
        self.exitButton = Button(self.screen, int((self.WIDTH-self.menuButtonWidth)/2), 440,
                                 self.menuButtonWidth, self.menuButtonHeight,
                                 self.BLACK, self.LILAC, self.CYAN, self.GREEN,
                                 lambda: self.exitProgram(), "Exit", self.medfont)
                                 
        self.finishRun = True
        while self.finishRun:
            ## Running speed (fps)
            self.clock.tick(self.FPS)
            
            ## Process inputs (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.finishRun = False
                
            ## Update    
            self.replayButton.update()
            self.mainMenuButton.update()
            self.exitButton.update()

            ## Draw (render)
            self.screen.fill(self.CREAM)
            #texts
            if self.win:
                self.textToScreen(self.WIDTH/2, self.HEIGHT/4, "YOU WIN!", self.BLACK, self.medfont)
            else:
                self.textToScreen(self.WIDTH/2, self.HEIGHT/4, "YOU LOSE.", self.BLACK, self.medfont)
            #buttons
            self.replayButton.draw()
            self.mainMenuButton.draw()
            self.exitButton.draw()
            
            # after drawing everything, flip the display
            pygame.display.flip()

        self.exitProgram()


if __name__ == "__main__":
    game = Game()
