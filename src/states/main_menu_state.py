import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BUTTONS_HEIGHT, BUTTONS_WIDTH, FONT
from config import LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, CADET_BLUE, WHITE
from states.state import State
from ui import draw_text
from button import ClickButton
import os


class MainMenuState(State):

    def __init__(self, game):
        super().__init__(game)
        if os.stat("src/json/game_state.json").st_size == 0:
            self.buttons = [
                ClickButton("New Game", 
                    SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - BUTTONS_HEIGHT - 10,
                    BUTTONS_HEIGHT, BUTTONS_WIDTH,
                    FONT,
                    LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                    action=lambda: self.game.change_state("options")),
                ClickButton("Instructions", 
                    SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 + 25,
                    BUTTONS_HEIGHT, BUTTONS_WIDTH,
                    FONT,
                    LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                    action=lambda: self.game.change_state("instructions")),
                ClickButton("Exit", 
                    SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 + BUTTONS_HEIGHT + 60,
                    BUTTONS_HEIGHT, BUTTONS_WIDTH,
                    FONT,
                    LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                    action=lambda: self.game.exit_game())
            ]
        else:
            self.buttons = [
                ClickButton("Continue Game", 
                    SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - BUTTONS_HEIGHT - 20,
                    BUTTONS_HEIGHT, BUTTONS_WIDTH,
                    FONT,
                    LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                    action=lambda: self.game.load_game_state()),
                ClickButton("New Game", 
                    SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2,
                    BUTTONS_HEIGHT, BUTTONS_WIDTH,
                    FONT,
                    LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                    action=lambda: self.game.clear_game_state()),
                ClickButton("Instructions", 
                    SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 + BUTTONS_HEIGHT + 20,
                    BUTTONS_HEIGHT, BUTTONS_WIDTH,
                    FONT,
                    LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                    action=lambda: self.game.change_state("instructions")),
                ClickButton("Exit", 
                    SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 + 2*BUTTONS_HEIGHT + 40,
                    BUTTONS_HEIGHT, BUTTONS_WIDTH,
                    FONT,
                    LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                    action=lambda: self.game.exit_game())
            ]
        

    def draw(self):
        screen = self.game.screen
        font = pygame.font.Font(None, 60)
        draw_text(screen,"Yinsh",font, STEEL_BLUE, SCREEN_WIDTH // 2 - font.size("Yinsh")[0] // 2, 160)
        # buttons
        super().draw()

