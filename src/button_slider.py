import pygame
import json
from config import BUTTONS_HEIGHT, BUTTONS_WIDTH, FONT, SCREEN_WIDTH, SCREEN_HEIGHT, LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, CADET_BLUE, WHITE
from button import ClickButton
from board import Board
from json_actions import load_boards

class ButtonSlider:
    def __init__(self, json_file, visible_area_width, visible_area_height, button_spacing, scrollbar_width, board_name):
        self.boards = load_boards(json_file)
        self.selected_board = board_name
        self.board = self.get_board_config()
        self.scroll_offset = 0
        self.board_button_spacing = button_spacing
        self.scrollbar_width = scrollbar_width
        self.json_file = json_file
        # Define the visible area
        self.visible_area = pygame.Rect(45, 150, visible_area_width, visible_area_height)
        self.background_color = (220, 220, 220)  # Light gray background
        
        # Scrollbar properties
        self.max_scroll = max(0, len(self.boards) * (self.board_button_spacing + BUTTONS_HEIGHT) - self.visible_area.height)
        self.scrollbar = pygame.Rect(self.visible_area.x + self.visible_area.width + 10, self.visible_area.y, self.scrollbar_width, self.visible_area.height)
        self.dragging_scrollbar = False
        self.drag_offset = 0

        self.buttons = self.create_buttons()



    def get_board_config(self):
        board = Board(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 250, 20)
        board.update_matrix(self.boards[self.selected_board]['layout'])
        return board
    

    def create_buttons(self):
        """Creates buttons with proper spacing and updates their visibility."""
        buttons = []
        start_y = self.visible_area.y - self.scroll_offset + self.board_button_spacing

        for board_name in self.boards:
            if start_y + BUTTONS_HEIGHT > self.visible_area.y and start_y < self.visible_area.y + self.visible_area.height:
                button = ClickButton(
                    text=board_name,  # Use the board key as the name
                    x=self.visible_area.x + 10,
                    y=start_y,
                    height=BUTTONS_HEIGHT,
                    width=BUTTONS_WIDTH,
                    font=FONT,
                    button_color=LIGHT_CYAN,
                    text_color=STEEL_BLUE,
                    hover_color=POWER_BLUE,
                    hover_text_color=CADET_BLUE,
                    action=lambda name=board_name: self.select_board(name)
                )
                buttons.append(button)

            start_y += self.board_button_spacing + BUTTONS_HEIGHT
        return buttons

    def select_board(self, board_name):
        """Updates the selected board and refreshes the matrix."""
        self.selected_board = board_name
        self.board.update_matrix(self.boards[board_name]['layout'])

    def draw_buttons(self, screen):
        """Only draws buttons inside the visible area."""
        for button in self.buttons:
            if self.visible_area.y <= button.y <= self.visible_area.y + self.visible_area.height - BUTTONS_HEIGHT:
                if button.text == self.selected_board:
                    button.color = CADET_BLUE
                    button.text_color = WHITE
                else:
                    button.color = LIGHT_CYAN
                    button.text_color = STEEL_BLUE
                button.draw(screen)

    def draw_scrollbar(self, screen):
        """Draws the scrollbar with rounded edges."""
        pygame.draw.rect(screen, (150, 150, 150), self.scrollbar, border_radius=10)

        if self.max_scroll > 0:
            scrollbar_height = self.visible_area.height * (self.visible_area.height / (len(self.boards) * (self.board_button_spacing + BUTTONS_HEIGHT)))
            self.scrollbar.height = max(30, scrollbar_height)

    def draw(self, screen):
        """Draws buttons and scrollbar with a background."""
        pygame.draw.rect(screen, self.background_color, self.visible_area, border_radius=15)  # Background with rounded edges
        self.draw_buttons(screen)
        self.draw_scrollbar(screen)

    def handle_events(self, event):
        """Handles clicks on buttons and scroll interactions."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.click(event)

            # Check if scrollbar is clicked
            if self.scrollbar.collidepoint(event.pos):
                self.dragging_scrollbar = True
                self.drag_offset = event.pos[1] - self.scrollbar.y

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_scrollbar = False

        elif event.type == pygame.MOUSEMOTION and self.dragging_scrollbar:
            if self.max_scroll > 0:  # Prevent division by zero
                new_y = event.pos[1] - self.drag_offset
                new_y = max(self.visible_area.y, min(new_y, self.visible_area.y + self.visible_area.height - self.scrollbar.height))
                self.scrollbar.y = new_y

                # Convert scrollbar movement to scroll offset
                scroll_ratio = (new_y - self.visible_area.y) / (self.visible_area.height - self.scrollbar.height)
                self.scroll_offset = scroll_ratio * self.max_scroll
                self.buttons = self.create_buttons()  # Refresh button positions
        elif event.type == pygame.MOUSEWHEEL:
            # Adjust scroll offset based on mouse wheel movement
            self.scroll_offset -= event.y * 20  # Adjust scroll speed
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))  # Keep within bounds

            # Move scrollbar accordingly
            if self.max_scroll > 0:
                scroll_ratio = self.scroll_offset / self.max_scroll
                self.scrollbar.y = self.visible_area.y + scroll_ratio * (self.visible_area.height - self.scrollbar.height)

            self.buttons = self.create_buttons()  # Refresh button positions

    def update_scrollbar(self):
        """Recalculate max_scroll and scrollbar height."""
        self.max_scroll = max(0, len(self.boards) * (self.board_button_spacing + BUTTONS_HEIGHT) - self.visible_area.height)
        self.scrollbar = pygame.Rect(self.visible_area.x + self.visible_area.width + 10, self.visible_area.y, self.scrollbar_width, self.visible_area.height)
        self.update_scrollbar_height()

    def update_scrollbar_height(self):
        """Adjust the scrollbar height based on the number of boards."""
        if self.max_scroll > 0:
            scrollbar_height = self.visible_area.height * (self.visible_area.height / (len(self.boards) * (self.board_button_spacing + BUTTONS_HEIGHT)))
            self.scrollbar.height = max(30, scrollbar_height)
