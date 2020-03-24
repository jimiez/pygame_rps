# Classes pertaining to graphical elements of the game are contained within this source file

import random
import pygame
import os
from constants import *

def loadImage(name):
    """
    Function for loading images

    Parameters:

        - name - str, Filename to be loaded (without file extension)

    Returns: a correctly formatted pygame.Surface
    """

    try:
        path = os.getcwd() + "\\media\\"
        filename = path + name + ".png"
        image = pygame.image.load(filename)
    except FileNotFoundError:
        print("Could not locate necessary image file {}.png".format(name))

    colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey, pygame.RLEACCEL)
    image = image.convert()
    return image

class Selection:
    """
    Class for handling the three main elements of the game that also includes image handling
    
    Parameters:

        - image - str, Image file to be used (loadImage)

        - pos - tuple, Position of the element on the screen as an offset from the middle
    """
    def __init__(self, image, pos):
        self.image = loadImage(image)
        self.imageOrig = self.image
        self.name = image
        self.rect = self.image.get_rect()
        self.rect.center = (SIZE_SCREEN[0] / 2 + pos[0], SIZE_SCREEN[1] / 2 + pos[1])
        self.rectOrig = self.rect
        self.highlighted = False

    def update(self, screen):
        self.drawHighlight()
        screen.blit(self.image, self.rect)
    
    def getClick(self, pos):
        if self.rect.collidepoint(pos):
            return self.name

    def drawHighlight(self):
        # Draw a red rectangle around the selection when mouse cursor hovers
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos) and not self.highlighted:
            pygame.draw.rect(self.image, COLOR_RED, pygame.Rect(0,0, 90, 90), 3)
        elif self.rect.collidepoint(pos):
            pass
        else:
            self.image = loadImage(self.name)
            self.highlighted = False

class Scoreboard:
    """
    This class displays the scoreboard on the game screen

    Parameters:

        - gamelogic - Gamelogic, class to get all the necessary stats from

        - screen - pygame.Screen, screen on which the scoreboard is displayed

    """

    def __init__(self, gamelogic):
        self.gamelogic = gamelogic
        self.scorebackground = pygame.Surface((150, 100))
        self.font = pygame.font.SysFont(FONT_MAIN, 36)
        self.rect = self.scorebackground.get_rect()

    def update(self, screen):
        
        # Because pygame doesn't support breaklines, text on separate rows needs to be updated individually
        self.scorebackground.fill(COLOR_GRAY)
        self.text_wins = self.font.render("Wins: " + str(self.gamelogic.wins), 1, COLOR_GREEN)
        self.scorebackground.blit(self.text_wins, (10, 10))
        self.text_ties = self.font.render("Ties: " + str(self.gamelogic.ties), 1, COLOR_BLACK)
        self.scorebackground.blit(self.text_ties, (10, 40))
        self.text_losses = self.font.render("Losses: " + str(self.gamelogic.losses), 1, COLOR_RED)
        self.scorebackground.blit(self.text_losses, (10, 70))

        newpos = (screen.get_rect().topright[0] -20, screen.get_rect().topright[1])
        self.rect.topright = newpos
        screen.blit(self.scorebackground, self.rect)
        
class Button:
    """
    This is a class for drawing buttons on screen, also includes functionality for clicking

    Parameters:

        - pos - tuple, position of the button as an offset from center of the screen. E.g. (0, 0) = middle of the screen, (-100, -200) down 100 px and left 200 px.

        - size - tuple, size of the button

        - text: - str, text on the button

    """
    def __init__(self, pos, size, text):
        self.button = pygame.Surface(size)
        self.button.fill(COLOR_GRAY)
        self.rect = self.button.get_rect()
        self.rect.center = (SIZE_SCREEN[0] / 2 + pos[0], SIZE_SCREEN[1] / 2 + pos[1])

        font = pygame.font.Font(FONT_MAIN, 36)
        text = font.render(text, 1, COLOR_BLACK)
        text_rect = text.get_rect()
        text_rect.center = (size[0] / 2, size[1] / 2)
        self.button.blit(text, text_rect)
        self.clicked = False

    def getClick(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked = True
    
    def update(self, screen):
        screen.blit(self.button, self.rect)

class ResultDisplayer:
    """
    This class displays the results of the previous round.

    Parameters:

        - playerchoice - str, player's choice in the previous round

        - computerchoice - str, computers's choice in the previous round

        - result - int, result of the previous round (1 = player win, 0 = tie, -1 = player lost)

    """

    def __init__(self, playerchoice, computerchoice, result):
        self.playerchoice = playerchoice
        self.computerchoice = computerchoice
        self.result = result

        # Loading the images of previous round's actions
        pimage = loadImage(playerchoice)

        # Rotate and flip the image of player's choice before moving into place relative to the middle of the screen
        self.playerchoice = pygame.transform.rotate(pimage, 90)
        self.playerchoice = pygame.transform.flip(self.playerchoice, True, False)
        self.playerchoice_rect = self.playerchoice.get_rect()
        self.playerchoice_rect.center = (SIZE_SCREEN[0] / 2 - 150, SIZE_SCREEN[1] / 2)

        # Do the above for the computer
        cimage = loadImage(computerchoice)
        self.computerchoice = pygame.transform.rotate(cimage, 90)
        self.computerchoice_rect = self.computerchoice.get_rect()
        self.computerchoice_rect.center = (SIZE_SCREEN[0] / 2 + 150, SIZE_SCREEN[1] / 2)

        # Some text placement
        self.font = pygame.font.SysFont(FONT_MAIN, 36)
        self.ptext = self.font.render("You chose", 1, COLOR_BLACK)
        self.ptext_rect = self.ptext.get_rect()
        self.ptext_rect.center = (SIZE_SCREEN[0] / 2 - 150, SIZE_SCREEN[1] / 2 - 50)

        self.ctext = self.font.render("Computer chose", 1, COLOR_BLACK)
        self.ctext_rect = self.ctext.get_rect()
        self.ctext_rect.center = (SIZE_SCREEN[0] / 2 + 150, SIZE_SCREEN[1] / 2 - 50)

        # Result text placement. Text content and color change based on the outcome.
        if result == 1:
            self.resulttext = self.font.render("You win!", 1, COLOR_GREEN)
        elif result == 0:
            self.resulttext = self.font.render("Tie!", 1, COLOR_BLACK)
        else:
            self.resulttext = self.font.render("You lose!", 1, COLOR_RED)

        self.resulttext_rect = self.resulttext.get_rect()
        self.resulttext_rect.center = (SIZE_SCREEN[0] / 2, SIZE_SCREEN[1] / 2)

    def update(self, screen):
        screen.blit(self.playerchoice, self.playerchoice_rect)
        screen.blit(self.computerchoice, self.computerchoice_rect)
        screen.blit(self.ptext, self.ptext_rect)
        screen.blit(self.ctext, self.ctext_rect)
        screen.blit(self.resulttext, self.resulttext_rect)

