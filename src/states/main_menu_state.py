import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BUTTONS_HEIGHT, BUTTONS_WIDTH, FONT
from config import LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, CADET_BLUE, WHITE
from states.state import State
from ui import draw_text
from button import ClickButton


class MainMenuState(State):

    def __init__(self, game):
        super().__init__(game)
        self.buttons = [
            ClickButton("Play", 
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
        
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.click(event)

    def draw(self):
        screen = self.game.screen
        font = pygame.font.Font(None, 60)
        draw_text(screen,"Yinsh",font,(60, 100, 140), SCREEN_WIDTH // 2 - font.size("Yinsh")[0] // 2, 160)
        for button in self.buttons:
            button.draw(screen)

