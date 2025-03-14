import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BUTTONS_HEIGHT, BUTTONS_WIDTH, BLACK, WHITE
from states.state import State
from ui import draw_button, draw_text
from mode import GameMode

class OptionMenuState(State):

    def __init__(self, game):
        super().__init__(game)
        self.player_vs_player_button = None
        self.player_vs_ai_button = None
        self.ai_vs_ai_button = None
        self.back_button = None

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.player_vs_player_button.collidepoint(x, y):
                self.game.change_state("customization", GameMode.PLAYER_VS_PLAYER)  
            elif self.player_vs_ai_button.collidepoint(x, y):
                self.game.change_state("customization", GameMode.PLAYER_VS_AI)  
            elif self.ai_vs_ai_button.collidepoint(x, y):
                self.game.change_state("customization", GameMode.AI_VS_AI)  
            elif self.back_button.collidepoint(x, y):
                self.game.go_back()

    def draw(self):
        screen = self.game.screen
        font = pygame.font.SysFont(None, 50)
        small_font = pygame.font.SysFont(None, 30)

        # Title text: Centered at the top of the screen
        draw_text(screen, "Yinsh", font, BLACK, SCREEN_WIDTH // 2 - font.size("Yinsh")[0] // 2, 100)

        # Draw the buttons
        button_margin = 20  # Margin between buttons
        y_offset = SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - BUTTONS_HEIGHT - button_margin

        # Player vs Player button
        self.player_vs_player_button = draw_button(
            screen, "Player vs Player", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE
        )
        
        # Player vs AI button
        y_offset += BUTTONS_HEIGHT + button_margin
        self.player_vs_ai_button = draw_button(
            screen, "Player vs AI", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE
        )
        
        # AI vs AI button
        y_offset += BUTTONS_HEIGHT + button_margin
        self.ai_vs_ai_button = draw_button(
            screen, "AI vs AI", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE
        )

        # Back button at the bottom of the screen
        y_offset += BUTTONS_HEIGHT + button_margin
        self.back_button = draw_button(
            screen, "Back", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE
        )
