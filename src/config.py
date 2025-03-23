import pygame

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)


LIGHT_CYAN = (222, 247, 247)  
STEEL_BLUE = (60, 100, 140)
POWER_BLUE = (183, 225, 225)
CADET_BLUE = (141,182,200)
SELECT_CYAN = (180, 230, 230)


PLAYER1_COLOR = WHITE
PLAYER2_COLOR = BLACK


BUTTONS_WIDTH = 300
BUTTONS_HEIGHT = 60
BUTTON_FONT_SIZE = 50

pygame.font.init()
FONT_TITLE = pygame.font.Font(None, 50) # Title font
FONT = pygame.font.Font(None, 40) # Button font 
SMALL_FONT = pygame.font.Font(None, 30) 
