import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BUTTONS_HEIGHT, BUTTONS_WIDTH, FONT
from config import LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, CADET_BLUE, WHITE
from states.state import State
from ui import draw_text
from button import ClickButton


class GameOver(State):

    def __init__(self, game, winner=None):
        super().__init__(game)
        self.winner = winner
        self.buttons = [
            ClickButton("Back to menu", 
                SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 + BUTTONS_HEIGHT + 60,
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.change_state("menu")),
            ClickButton("Exit", 
                SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 + 2*BUTTONS_HEIGHT + 95,
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
        fontSmall = pygame.font.Font(None, 50)
        draw_text(screen,"GameOver",font,(60, 100, 140), SCREEN_WIDTH // 2 - font.size("GameOver")[0] // 2, 160)

        if self.winner == 1:
            draw_text(screen,"White Player Wins",fontSmall,(60, 100, 140), SCREEN_WIDTH // 2 - fontSmall.size("White Player Wins")[0] // 2, 320)
        elif self.winner == 2:
            draw_text(screen,"Black Player Wins",fontSmall,(60, 100, 140), SCREEN_WIDTH // 2 - fontSmall.size("Black Player Wins")[0] // 2, 320)
        else:
            draw_text(screen,"Draw",fontSmall,(60, 100, 140), SCREEN_WIDTH // 2 - fontSmall.size("Draw")[0] // 2, 260)

        for button in self.buttons:
            button.draw(screen)

