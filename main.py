"""
This is a simple Rock, Paper, Scissors game made with the Pygame package for self-learning purposes.
It's not pretty, it's not very sophisticated, but it works.
@JPM 2020
"""

# Main loop of the game and initialization are contained within this file.

import sys, os, pygame
from uiClasses import *
from gameClasses import *
from constants import *

def resource_path(relative):
    """
    This function ensures that relative paths work when the game is frozen to .exe

    Parameters:

        - relative - str, relative path to file
    
    Returns: correctly formatted path depending on run location
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(relative)

def loadImage(name):
    """
    Function for loading images

    Parameters:

        - name - str, Filename to be loaded (without file extension)

    Returns: a correctly formatted pygame.Surface containing the image
    """

    try:
        filename = "media\\" + name + ".png"
        filedir = resource_path(filename)
        image = pygame.image.load(filedir)
    except FileNotFoundError:
        print("Could not locate necessary image file {}.png".format(name))

    colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey, pygame.RLEACCEL)
    image = image.convert()
    
    return image

def run_game(size, fps, sequence):
    """
    Function for running the main loop of the game.

    Parameters:

        - size - tuple, size of the game window

        - fps - int, refresh rate of the main game loop (frames per second)
        
        - sequence - Sequence (incl. subclasses), first sequence to be run 

    """
    screen = pygame.display.set_mode(size)
    sequenceActive = sequence

    while sequenceActive != None:
        keysPressed = pygame.key.get_pressed()
        
        filtered_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            else:
                filtered_events.append(event)
        
        sequenceActive.input(filtered_events, keysPressed)
        sequenceActive.update()
        sequenceActive.render(screen)
        
        sequenceActive = sequenceActive.next
        
        pygame.display.update()
        clock.tick(fps)


# initialize the game
pygame.init()
# Have to initialize a dummy screen here in order to get everything else initialized
pygame.display.set_mode((0,0))
pygame.display.set_caption('Rock, Paper & Scissors!')
clock = pygame.time.Clock()
gamelogic = GameLogic()        
scoreboard = Scoreboard(gamelogic)

# Load up all the images used across the different classes into a dictionary

files = ["rock", "paper", "scissors"]

for i in files:
    img = loadImage(i)
    DICT_IMAGES[i] = img

# Call the main loop
run_game(SIZE_SCREEN, 10, SequenceStart(scoreboard))

pygame.quit()
sys.exit()