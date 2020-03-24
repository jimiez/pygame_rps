# Classes pertaining to game operations and logic are contained within this source file

import pygame
from uiClasses import *
from constants import *

class GameLogic:
    """
    This class that contains the entire game logic of Rock, Paper, Scissors. Includes also rudimentary AI and bookkeeping.
    """
    def __init__(self):
        self.rounds = 0
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.playerChoices = []
        self.computerChoices = []
        self.listOfChoices = ["rock", "paper", "scissors"]
        self.winStats = [] # -1 computer wins, 0 tie, 1 player wins
        self.aiRandomness = 5 # percentage chance that AI plays a completely random hand any given round

    def _computerLogic(self):
        """
        This method is used to figure out the computer's next move. Note that it's entirely self-contained
        """

        #First round, start random
        if self.rounds < 1:
            return random.choice(self.listOfChoices)
        
        # There is a set probability that the AI plays a completely random hand
        if random.randint(1,100) < self.aiRandomness:
            return random.choice(self.listOfChoices)
            
        # MAIN LOGIC
        # if computer lost previous round, play the winning action of previous round. People are much more likely to keep using a winning tactic.
        if self.winStats[-1] == 1:
            computerChoice = self._oppositeChoice(self.playerChoices[-1])
        # if computer won the previous round, switch to what wins what it played in the previous round
        elif self.winStats[-1] == -1:
            computerChoice = self._oppositeChoice(self.computerChoices[-1])
        # if last round was a draw, play a random hand
        else:
            computerChoice = random.choice(self.listOfChoices)  
        return computerChoice


    def _oppositeChoice(self, choice):
        """
        Returns the option that WINS the chosen action
        
            Parameters:
            
                - choice - str, choice to which the opposite is requested

        Return: the opposite as a string
        """
        if choice == "rock":
            return "paper"
        elif choice == "paper":
            return "scissors"
        elif choice == "scissors":
            return "rock"      
        
    def playRound(self, playerChoice):
        """
        Play a single round, requires the player's input as a numeric value
        
        Parameters:

            - playerChoice - string, Player's action
        """      
        # make sure input is valid
        if playerChoice not in self.listOfChoices:
            print("Invalid choice!")
            raise ValueError

        # Resolve computer's choice 
        computerChoice = self._computerLogic()
        
        # Add the latest choices to action history
        self.playerChoices.append(playerChoice)
        self.computerChoices.append(computerChoice)
        
        # See who won

        if playerChoice == computerChoice:
            result = 0
            self.ties += 1
        elif self._oppositeChoice(computerChoice) == playerChoice:
            result = 1
            self.wins += 1
        else:
            result = -1
            self.losses += 1

        self.winStats.append(result)
        self.rounds += 1

class Sequence:
    """ 
    A (mostly) abstract class for defining basic functions in a game sequence
    """ 

    def __init__(self):
        self.next = self
    
    def input(self, events, keys):
        """
        Method for processing input and events from the game sequence
        """
        raise NotImplementedError

    def update(self):
        """
        Game logic should be placed here
        """
        raise NotImplementedError

    def render(self, screen):
        """
        Draws the updates on the screen
        """
        raise NotImplementedError

    def nextSequence(self, sequence):
        """
        Activate the next sequence
        """
        self.next = sequence

class SequenceStart(Sequence):
    """
    Just a start-up screen

    Parameters:

        - scoreboard - Scoreboard object, passed between scenes to maintain consistency.
    """
    def __init__(self, scoreboard):
        Sequence.__init__(self)
        self.scoreboard = scoreboard
        self.mainfont = pygame.font.Font(FONT_MAIN, 42)
        self.maintext = self.mainfont.render("ROCK, PAPER & SCISSORS!", 1, COLOR_BLACK)
        self.maintext_rect = self.maintext.get_rect()
        self.maintext_rect.center = (SIZE_SCREEN[0] / 2, SIZE_SCREEN[1] / 2 - 100)

        self.subfont = pygame.font.Font(FONT_MAIN, 24)
        self.subtext = self.subfont.render("Press any key to start", 1, COLOR_BLUE)
        self.subtext_rect = self.subtext.get_rect()
        self.subtext_rect.center = (SIZE_SCREEN[0] / 2, SIZE_SCREEN[1] / 2 + 100)

    def input(self, events, keys):
        # See if any key is pressed start the actual game
        if sum(keys) > 0:
            self.nextSequence(SequenceSelection(self.scoreboard))

    def update(self):
        pass

    def render(self, screen):
        screen.fill(COLOR_WHITE)
        screen.blit(self.maintext, self.maintext_rect)
        screen.blit(self.subtext, self.subtext_rect)
    
class SequenceSelection(Sequence):
    """
    This sequence handles the part of the game where player chooses their next move

        Parameters:

            - scoreboard - scoreboard object passed between scenes
    """

    def __init__(self, scoreboard):
        Sequence.__init__(self)

        # Images to be loaded along with offsets
        images = ("rock", "paper", "scissors")
        offsets = [-150, 0, 150]
        self.selections = []
        self.choice = None
        
        # Initialize and load the game selections (i.e. rock, paper, scissors). 
        for i in range(0, 3):
            self.selections.append(Selection(images[i], (offsets[i], 0)))
    
        # Init rest
        self.scoreboard = scoreboard
        self.gamelogic = self.scoreboard.gamelogic

    def input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                for s in self.selections:
                    if self.choice == None:
                        self.choice = s.getClick(pos)

    def update(self):
        if self.choice != None:
            self.gamelogic.playRound(self.choice)
            self.choice = None
            self.nextSequence(SequenceResolve(self.scoreboard))

    def render(self, screen):
        screen.fill(COLOR_WHITE)
        for s in self.selections:
            s.update(screen)
        self.scoreboard.update(screen)

 
class SequenceResolve(Sequence):
    """
    This sequence displays the result of the previous round and prompts whether the player wants to play another round.
    
        Parameters:

            - scoreboard - scoreboard, object passed between scenes
    """
    def __init__(self, scoreboard):
        Sequence.__init__(self)

        self.scoreboard = scoreboard
        # Initialize the helper class for displaying results with stuff from the scoreboard class
        self.result = ResultDisplayer(
            scoreboard.gamelogic.playerChoices[-1],
            scoreboard.gamelogic.computerChoices[-1],
            scoreboard.gamelogic.winStats[-1])
              
        # The buttons for next round or quitting
        self.button_newround = Button((-120, 150), (150, 50), "New round")
        self.button_quit = Button((120, 150), (150, 50), "Quit")

    def input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.button_newround.getClick(pygame.mouse.get_pos())
                self.button_quit.getClick(pygame.mouse.get_pos())
        
    def update(self):

        if self.button_newround.clicked:
            self.nextSequence(SequenceSelection(self.scoreboard))
        if self.button_quit.clicked:
            self.nextSequence(None)
    
    def render(self, screen):
        screen.fill(COLOR_WHITE)
        self.scoreboard.update(screen)
        self.result.update(screen)
        self.button_newround.update(screen)
        self.button_quit.update(screen)