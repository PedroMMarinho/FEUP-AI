import pygame
from states.state import State
from ui import draw_text, draw_input_box
from config import BLACK, WHITE, FONT, SCREEN_WIDTH, SCREEN_HEIGHT, BUTTONS_HEIGHT, BUTTONS_WIDTH, LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, CADET_BLUE
from button import ClickButton
from json_actions import load_boards, save_boards
from board import Board, BoardSpaceType
from tool_slider import ToolSlider, ToolType
import time  # Import time module to track error message duration

class BoardCreationMenu(State):
    def __init__(self, game, board_matrix=None, board_name=None):
        super().__init__(game)
        self.input_text = board_name if board_name else ""  # Store the board name
        self.original_text = self.input_text  # Store the original text
        self.error_message = ""
        self.error_time = 0  # Time when the error message appeared
        self.input_box = pygame.Rect(60, SCREEN_HEIGHT - 2 * BUTTONS_HEIGHT - 50, 200, 50)
        self.tool_slider = ToolSlider(SCREEN_WIDTH - 200, 160)  # Create a tool slider
        # Create an empty board
        self.board = Board()
        self.mode = "Create"
        if board_matrix:
            self.mode = "Edit"
            self.board.update_matrix(board_matrix)
            self.board.reload_board()
        
        self.mouse_down = False # Variable to control if mouse is pressed.

        self.action_buttons = [
            ClickButton("Save",
                        SCREEN_WIDTH - BUTTONS_WIDTH - 50, SCREEN_HEIGHT - BUTTONS_HEIGHT - 40,  # Bottom left
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT, LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.create_board()),

            ClickButton("Cancel",
                        50, SCREEN_HEIGHT - BUTTONS_HEIGHT - 40,  # Bottom right
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT, LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.go_back()),
            ClickButton("Clear Board",
                        SCREEN_WIDTH - BUTTONS_WIDTH * 3 // 4 - 40, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT,  # Bottom center
                        BUTTONS_HEIGHT, BUTTONS_WIDTH * 3 // 4,
                        FONT, LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.board.clear_board())
        ]


    def create_board(self):
        """Creates a new board and saves it using the current board's matrix."""
        if not self.input_text.strip():
            self.error_message = "Board name cannot be empty!"
            self.error_time = time.time()  # Store the time when error occurred
            return

        # Load current boards
        boards = load_boards("src/json/boards.json")

        # Check if board name already exists
        if self.input_text in boards and self.input_text != self.original_text:
            self.error_message = "Board name already exists!"
            self.error_time = time.time()  # Store the time when error occurred
            return

        if self.input_text != self.original_text and self.original_text in boards:
            boards[self.input_text] = boards.pop(self.original_text) #Rename the board
            boards[self.input_text]["layout"] = self.board.matrix #Updates the layout
        else:
            boards[self.input_text] = {"layout": self.board.matrix} #create a new board.
  
        save_boards("src/json/boards.json", boards)

        # Set as selected board and go back
        self.game.selected_board = self.input_text
        self.game.change_without_save("initial_board_customization")



    def handle_events(self, event):
        """Handles text input, button clicks, and board modifications."""
        if event.type == pygame.KEYDOWN:
            ctrl_held = pygame.key.get_mods() & pygame.KMOD_CTRL  # Check if Ctrl is held

            if event.key == pygame.K_RETURN:
                self.create_board()
            elif event.key == pygame.K_BACKSPACE:
                if ctrl_held:
                    self.input_text = ""  # Clear all text if Ctrl is held
                elif self.input_text:
                    self.input_text = self.input_text[:-1]  # Delete one character
            elif len(self.input_text) < 20:  # Prevent overflow (adjust max length as needed)
                self.input_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button click
                self.mouse_down = True
                self.populate_board_space(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_down = False
        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_down:
                self.populate_board_space(event.pos)

        for button in self.action_buttons:
            button.click(event)

        self.tool_slider.handle_event(event)

    def populate_board_space(self, pos):
        x, y = pos
        for (px, py), (col, row) in self.board.vertices.items():
            if abs(px - x) < self.board.radius and abs(py - y) < self.board.radius:
                tool = self.tool_slider.get_current_tool()
                tool_value = None

                if tool == ToolType.BLACK_MARKER:
                    if self.board.num_markers > 0 and self.board.matrix[row][col] == BoardSpaceType.EMPTY.value:
                        tool_value = BoardSpaceType.PLAYER2_MARKER.value
                        self.board.num_markers -= 1
                elif tool == ToolType.WHITE_MARKER:
                    if self.board.num_markers > 0 and self.board.matrix[row][col] == BoardSpaceType.EMPTY.value:
                        tool_value = BoardSpaceType.PLAYER1_MARKER.value
                        self.board.num_markers -= 1
                elif tool == ToolType.BLACK_RING:
                    if self.board.num_rings2 < 5 and self.board.matrix[row][col] == BoardSpaceType.EMPTY.value:
                        tool_value = BoardSpaceType.PLAYER2_RING.value
                        self.board.num_rings2 += 1
                elif tool == ToolType.WHITE_RING:
                    if self.board.num_rings1 < 5 and self.board.matrix[row][col] == BoardSpaceType.EMPTY.value:
                        tool_value = BoardSpaceType.PLAYER1_RING.value
                        self.board.num_rings1 += 1
                elif tool == ToolType.RUBBER:
                    current_value = self.board.matrix[row][col]
                    if current_value == BoardSpaceType.PLAYER1_MARKER.value or current_value == BoardSpaceType.PLAYER2_MARKER.value:
                        self.board.num_markers += 1
                    elif current_value == BoardSpaceType.PLAYER1_RING.value:
                        self.board.num_rings1 -= 1
                    elif current_value == BoardSpaceType.PLAYER2_RING.value:
                        self.board.num_rings2 -= 1
                    tool_value = BoardSpaceType.EMPTY.value

                if tool_value is not None:
                    self.board.matrix[row][col] = tool_value
                    self.board.update_matrix(self.board.matrix)
                break

    def draw(self):
        """Draws the board creation UI."""
        screen = self.game.screen
        title = "Edit Board" if self.mode == "Edit" else "Create New Board"
        draw_text(screen, title, FONT, BLACK, SCREEN_WIDTH // 2 - FONT.size(title)[0] // 2, 50)

        # Draw the current board
        self.board.draw(screen)

        draw_text(screen, "Board Name", FONT, BLACK, 70, SCREEN_HEIGHT - BUTTONS_HEIGHT * 2 - 90)
        # Make cursor blink every 500ms
        cursor_visible = (pygame.time.get_ticks() // 500) % 2 == 0

        # Truncate text if it's too long
        text_to_display = self.input_text[-13:]

        # Append blinking cursor if visible
        if cursor_visible:
            text_to_display += "|"

        draw_input_box(screen, self.input_box, text_to_display)


        # Hide the error message after 2 seconds (or any desired time)
        if self.error_message and (time.time() - self.error_time) < 2:
            draw_text(screen, self.error_message, FONT, (255, 0, 0), SCREEN_WIDTH // 10 - 100, 80)

        for button in self.action_buttons:
            button.draw(screen)

        self.tool_slider.draw(screen)