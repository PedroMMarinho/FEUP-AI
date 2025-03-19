import pygame
import json
from states.state import State
from ui import draw_text
from config import BLACK, WHITE, BUTTONS_WIDTH, BUTTONS_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT,RED,BLUE, FONT, LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, CADET_BLUE, SMALL_FONT
from board import Board
from button_slider import ButtonSlider
from button import ClickButton

class BoardCustomizationMenu(State):
    def __init__(self, game):
        super().__init__(game)

        # Configurable values 
        self.board_button_width = BUTTONS_WIDTH
        self.board_button_height = BUTTONS_HEIGHT
        self.board_slider = ButtonSlider("src/boards.json", SCREEN_WIDTH // 4 + 20, SCREEN_HEIGHT // 2 + 20, 10, 15, game.selected_board)
        self.action_buttons = [
    ClickButton("Back", 
                SCREEN_WIDTH // 3 - BUTTONS_WIDTH, SCREEN_HEIGHT - 100,
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.go_back()),
    
    ClickButton("Delete Board",
                SCREEN_WIDTH // 3 - BUTTONS_WIDTH, SCREEN_HEIGHT - 200,
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.board_slider.delete_board()),
    
    ClickButton("Select Board",
                SCREEN_WIDTH - BUTTONS_WIDTH - 20, SCREEN_HEIGHT - 100,
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.select_board_and_go_back())
]

    def select_board_and_go_back(self):
        """Sets the selected board and navigates back."""
        self.game.selected_board = self.board_slider.selected_board
        self.game.go_back()
        
    def handle_events(self, event):
        self.board_slider.handle_events(event)  # Handles button clicks & scroll
        for button in self.action_buttons:
            button.click(event)

    def select_board(self):
        """Sets the selected board and transitions back."""
        self.game.selected_board = self.board_slider.selected_board
        self.game.go_back()

    def draw(self):
        """Draws the board customization menu."""
        screen = self.game.screen
        draw_text(screen, "Board Customization", FONT, BLACK, SCREEN_WIDTH // 2 - FONT.size("Board Customization")[0] // 2, 50)
        # Draw the board slider
        self.board_slider.draw(screen)

        # Draw the selected board
        draw_text(screen, f"Selected Board Preview: {self.board_slider.selected_board}", SMALL_FONT, BLACK, SCREEN_WIDTH // 2 - SMALL_FONT.size(f"Selected Board Preview: {self.board_slider.selected_board}")[0] // 2 + 220 , 100)
        self.board_slider.board.draw(screen)
        # Draw the back button
        for button in self.action_buttons:
            button.draw(screen)