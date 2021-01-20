import pygame


### BUTTON ###
class Button(object):
    """Creates a button."""
    def __init__(self, screen, x, y, width, height,
                 text_col, inactive_col, active_col, pressed_col,
                 action=None, text="", font=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_col = text_col
        self.inactive_col = inactive_col
        self.active_col = active_col
        self.pressed_col = pressed_col
        self.active = False
        self.pressed = False
        self.pressing = False
        self.action = action
        self.text = text
        self.font = font
        self.digit = None

    def update(self):
        # mouse position, click and activeness
        self.mouse_pos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        self.active = (self.x < self.mouse_pos[0] < self.x+self.width\
                       and self.y < self.mouse_pos[1] < self.y+self.height)      

        # update button activeness and color
        if self.active: # if mouse on button
            if self.click[0]: # if clicked
                self.pressed = True
                self.pressing = True
                if self.action:
                    self.action()
            else:
                self.pressing = False
        else:
            self.pressing = False
            if self.click[0]: # if clicked out of button
                self.pressed = False

    ## draws button
    def draw(self):
        if self.active:
             pygame.draw.rect(self.screen, self.active_col, [self.x, self.y, self.width, self.height])
        else:
            if self.pressed:
                pygame.draw.rect(self.screen, self.pressed_col, [self.x, self.y, self.width, self.height])
            else:
                pygame.draw.rect(self.screen, self.inactive_col, [self.x, self.y, self.width, self.height])

        if self.text:
            self.drawText(self.text, self.font, self.text_col)
        
    ## draw text on button
    def drawText(self, text, font, color):
        self.text = text
        self.font = font
        self.text_col = color
        self.textSurf = self.font.render(self.text, True, self.text_col)
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = ((self.x+(self.width/2)), (self.y+(self.height/2)))
        self.screen.blit(self.textSurf, self.textRect)


### SUDOKU SQUARE ###
class SudokuButton(Button):
    def __init__(self, screen, x, y, width, height, text_col,
                 inactive_col, active_col, pressed_col,
                 action=None, text="", font=None,
                 sudokuRow = None, sudokuCol = None):
        
        Button.__init__(self, screen, x, y, width, height, text_col,
                       inactive_col, active_col, pressed_col,
                       action=None, text="", font=None)
        self.sudokuRow = sudokuRow
        self.sudokuCol = sudokuCol
        # likePressed is used to showing more than one digits like they are pressed
        self.likePressed = False
        
    ## draws button
    def draw(self):
        if self.active:
             pygame.draw.rect(self.screen, self.active_col, [self.x, self.y, self.width, self.height])
        else:
            if self.pressed or self.likePressed:
                pygame.draw.rect(self.screen, self.pressed_col, [self.x, self.y, self.width, self.height])
            else:
                pygame.draw.rect(self.screen, self.inactive_col, [self.x, self.y, self.width, self.height])

        if self.text:
            self.drawText(self.text, self.font, self.text_col)
        
    ## draw text on button
    def drawText(self, text, font, color):
        # if sudoku square and it's text is 0, don't draw 0
        if self.text != "0":
            self.text = text
            self.font = font
            self.text_col = color
            self.textSurf = self.font.render(self.text, True, self.text_col)
            self.textRect = self.textSurf.get_rect()
            self.textRect.center = ((self.x+(self.width/2)), (self.y+(self.height/2)))
            self.screen.blit(self.textSurf, self.textRect)
