import pygame
from states.state import State
from ui import draw_text
from config import BLACK, WHITE, BUTTONS_WIDTH, BUTTONS_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT,RED,BLUE, FONT, LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, CADET_BLUE, SMALL_FONT, FONT2
from button_slider import ButtonSlider
from button import ClickButton
from json_actions import  save_boards

class BoardCustomizationMenu(State):
    def __init__(self, game):
        super().__init__(game)

        # Configurable values 
        self.board_button_width = BUTTONS_WIDTH
        self.board_button_height = BUTTONS_HEIGHT
        self.board_slider = ButtonSlider("src/boards.json", SCREEN_WIDTH // 4 + 20, SCREEN_HEIGHT // 2 + 20, 10, 10, game.selected_board)
        self.action_buttons = [
    ClickButton("Back", 
                SCREEN_WIDTH // 3 - BUTTONS_WIDTH - 30, SCREEN_HEIGHT - 100,
                BUTTONS_HEIGHT, 250,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.go_back()),
    
    ClickButton("Delete Board",
                SCREEN_WIDTH - BUTTONS_WIDTH*2 + 25 , SCREEN_HEIGHT - 100,
                BUTTONS_HEIGHT, 250,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.delete_board()),
    
    ClickButton("Select Board",
                SCREEN_WIDTH - BUTTONS_WIDTH, SCREEN_HEIGHT - 100,
                BUTTONS_HEIGHT, 250,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.select_board_and_go_back()),
    ClickButton("New Board",
                SCREEN_WIDTH // 3 - BUTTONS_WIDTH - 30, SCREEN_HEIGHT - 200,
                BUTTONS_HEIGHT, 250,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.change_state("board_creation_menu")),
    ClickButton("Edit Board",
                SCREEN_WIDTH - BUTTONS_WIDTH*3 + 50, SCREEN_HEIGHT - 100,
                BUTTONS_HEIGHT, 250,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.change_state("board_creation_menu", self.board_slider.board.matrix, self.board_slider.selected_board
                ))
]

    def select_board_and_go_back(self):
        """Sets the selected board and navigates back."""
        self.game.selected_board = self.board_slider.selected_board
        self.game.go_back()

    def delete_board(self):
        """Deletes a board from the JSON file and UI, and sets the selected board to the one above it."""
        if self.board_slider.selected_board != "Default":
            # Get list of board names
            board_names = list(self.board_slider.boards.keys())

            # Find index of the selected board
            selected_index = board_names.index(self.board_slider.selected_board)

            # Remove from memory
            del self.board_slider.boards[self.board_slider.selected_board]

            # Save updated list to JSON
            save_boards(self.board_slider.json_file, self.board_slider.boards)

            # Determine the new selected board
            if selected_index > 0:
                self.board_slider.selected_board = board_names[selected_index - 1]
                self.game.selected_board = self.board_slider.selected_board  # Select the board above
            elif len(self.board_slider.boards) > 0:
                self.board_slider.selected_board = list(self.board_slider.boards.keys())[0]
                self.game.selected_board = self.board_slider.selected_board
            else:
                self.selected_board = "Default"  
                self.game.selected_board = self.board_slider.selected_board  # Select the board above

            # Recreate buttons with updated board list
            self.board_slider.buttons = self.board_slider.create_buttons()

            # Recalculate scroll values
            self.board_slider.update_scrollbar()  # Recalculate max_scroll and scrollbar height
            self.board_slider.scroll_offset = min(self.board_slider.scroll_offset, self.board_slider.max_scroll)  # Prevent overscrolling
        else:
            print("Cannot delete the Default board.")

        
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
        # Draw "Selected Board Preview:" first
        text1 = "Selected Board Preview:"
        text1_x = SCREEN_WIDTH // 2 - SMALL_FONT.size(text1)[0] // 2 + 120
        draw_text(screen, text1, SMALL_FONT, BLACK, text1_x, 120)

        # Draw the selected board right after text1
        text2 = self.board_slider.selected_board
        text2_x = text1_x + SMALL_FONT.size(text1)[0] + 10  # Add some spacing
        draw_text(screen, text2, FONT, STEEL_BLUE, text2_x, 115)

        self.board_slider.board.draw(screen)
        # Draw the back button
        for button in self.action_buttons:
            button.draw(screen)