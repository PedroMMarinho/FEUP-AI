import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BUTTONS_HEIGHT, BUTTONS_WIDTH, FONT
from config import LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, CADET_BLUE, WHITE
from states.state import State
from ui import draw_text
from mode import GameMode
from button import ClickButton

class OptionMenuState(State):

    def __init__(self, game):
        super().__init__(game)
        self.buttons = [
            ClickButton("Player vs Player", 
                SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - BUTTONS_HEIGHT - 20,
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.change_state("customization", gameMode=GameMode.PLAYER_VS_PLAYER)),
            ClickButton("Player vs AI", 
                SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2,
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.change_state("customization", gameMode=GameMode.PLAYER_VS_AI)  ),
            ClickButton("AI vs AI", 
                SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 + BUTTONS_HEIGHT + 20,
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.change_state("customization", gameMode=GameMode.AI_VS_AI)  ),
            ClickButton("Back", 
                SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 + 2*BUTTONS_HEIGHT + 40,
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.go_back()),
        ]

    def draw(self):
        screen = self.game.screen
        font = pygame.font.Font(None, 60)
        draw_text(screen,"Yinsh",font,(60, 100, 140), SCREEN_WIDTH // 2 - font.size("Yinsh")[0] // 2, 160)
        #buttons
        super().draw()
