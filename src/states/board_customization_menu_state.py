import pygame
import json
from states.state import State
from ui import draw_button, draw_text
from config import BLACK, WHITE, BUTTONS_WIDTH, BUTTONS_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT,RED,BLUE
from board import Board

class BoardCustomizationMenu(State):
    def __init__(self, game):
        super().__init__(game)

        # Configurable values 
        self.board_button_width = BUTTONS_WIDTH
        self.board_button_height = BUTTONS_HEIGHT
        self.board_button_spacing = 10
        self.visible_area_width = 300
        self.visible_area_height = 400
        self.scrollbar_width = 20
        self.scroll_speed = 20
        self.selected_board = "Default"  # Default selected board layout
        self.board = Board(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 250, 20)

        self.boards = self.load_boards("src/boards.json")
        self.back_button = None
        self.scroll_offset = 0
        self.visible_area = pygame.Rect(100, 150, self.visible_area_width, self.visible_area_height) # Rectangle of boards
        self.max_scroll = max(0, len(self.boards) * (self.board_button_spacing + self.board_button_height) - self.visible_area.height)
        self.scrollbar = pygame.Rect(self.visible_area.x + self.visible_area.width + 10, self.visible_area.y, self.scrollbar_width, self.visible_area.height)
        self.dragging_scrollbar = False
        self.drag_offset = 0

    def load_boards(self, file):
        with open(file, "r") as f:
            return json.load(f)

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if self.back_button.collidepoint(x, y):
                self.game.change_state("menu")
            elif self.visible_area.collidepoint(x, y):
                for index, board in enumerate(self.boards):
                    button_rect = pygame.Rect(self.visible_area.x, self.visible_area.y + index * (self.board_button_spacing + self.board_button_height) - self.scroll_offset, self.board_button_width, self.board_button_height)
                    if button_rect.collidepoint(x, y):
                        # update the board layout
                        self.selected_board = board["name"]
                        self.board.update_matrix(board["layout"])

            elif self.scrollbar.collidepoint(x, y):
                self.dragging_scrollbar = True
                self.drag_offset = y - self.scrollbar.y
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_scrollbar:
                mouse_y = event.pos[1]
                new_y = mouse_y - self.drag_offset
                new_y = max(self.visible_area.y, min(new_y, self.visible_area.y + self.visible_area.height - self.scrollbar.height))
                self.scrollbar.y = new_y
                # Update the scroll offset based on scrollbar's position
                self.scroll_offset = (self.scrollbar.y - self.visible_area.y) / (self.visible_area.height - self.scrollbar.height) * self.max_scroll
    
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_scrollbar:
                self.dragging_scrollbar = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # Scroll up
                self.scroll_offset = max(self.scroll_offset - self.scroll_speed, 0)
            elif event.y < 0:  # Scroll down
                self.scroll_offset = min(self.scroll_offset + self.scroll_speed, self.max_scroll)
            # Update scrollbar position based on scroll offset
            self.scrollbar.y = self.visible_area.y + (self.scroll_offset / self.max_scroll) * (self.visible_area.height - self.scrollbar.height)

    def draw_buttons(self):
        """Draws board selection buttons inside a scrollable area."""
        pygame.draw.rect(self.game.screen, (220, 220, 220), self.visible_area)  # Draw scrollable area
        start_y = self.visible_area.y - self.scroll_offset
        for board in self.boards:
            button_rect = pygame.Rect(self.visible_area.x, start_y, self.board_button_width, self.board_button_height)
            if self.visible_area.colliderect(button_rect):
                button_color = (100, 100, 100) if board["name"] == self.selected_board else (200, 200, 200)
                text_color = BLUE if board["name"] == self.selected_board else BLACK
                pygame.draw.rect(self.game.screen, button_color, button_rect)
                draw_text(self.game.screen, board["name"], pygame.font.Font(None, 30), text_color, button_rect.topleft[0] + 10, button_rect.y + 10)
            start_y += self.board_button_spacing + self.board_button_height

    def draw_scrollbar(self):
        """Draws the visible scrollbar."""
        pygame.draw.rect(self.game.screen, (150, 150, 150), self.scrollbar)  # Draw the scrollbar
        if self.max_scroll > 0:  # Only show the scrollbar if content overflows
            scrollbar_height = self.visible_area.height * (self.visible_area.height / (len(self.boards) * (self.board_button_spacing + self.board_button_height)))
            self.scrollbar.height = max(30, scrollbar_height)  # Minimum height of the scrollbar is 30px


    def draw(self):
        """Draws the board customization menu."""
        screen = self.game.screen
        font = pygame.font.Font(None, 50)
        draw_text(screen, "Board Customization", font, BLACK, SCREEN_WIDTH // 2 - font.size("Board Customization")[0] // 2, 50)
        self.draw_buttons()
        self.draw_scrollbar()  # Draw the scrollbar

        # Draw the selected board
        draw_text(screen, f"Selected Board Preview: {self.selected_board}", pygame.font.Font(None, 30), BLACK, SCREEN_WIDTH - font.size(f"Selected Board Preview: {self.selected_board}")[0] - 50, 100
        )
        self.board.draw(screen)
        self.back_button = draw_button(
            screen, "Back", SCREEN_WIDTH // 6 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT - BUTTONS_HEIGHT - 30 , BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE
        )
