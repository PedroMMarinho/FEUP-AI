import pygame
from button import ClickButton
from config import BUTTONS_HEIGHT, BUTTONS_WIDTH, LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, FONT, BLACK
from ui import draw_text
import enum

class ToolType(enum.Enum):
    RUBBER = 0
    BLACK_MARKER = 1
    WHITE_MARKER = 2
    BLACK_RING = 3
    WHITE_RING = 4

class ToolSlider:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tools = list(ToolType)
        self.current_tool_index = ToolType.BLACK_MARKER.value
        self.buttons = [
            ClickButton(
                "<", 
                self.x - 120, self.y,
                4 * BUTTONS_HEIGHT / 6, BUTTONS_WIDTH / 6,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                lambda: self.change_tool(-1)
            ),
            ClickButton(
                ">", 
                self.x + 120, self.y,
                4 * BUTTONS_HEIGHT / 6, BUTTONS_WIDTH / 6,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                lambda: self.change_tool(1)
            )
        ]

    def change_tool(self, direction):
        self.current_tool_index = (self.current_tool_index + direction) % len(self.tools)

    def draw_tool(self, screen):
        tool_x_offset = 20  # Shift the tool slightly to the right
        tool_y_offset = (4 * BUTTONS_HEIGHT / 6) // 2 + 5  # Center vertically

        match (self.current_tool_index):
            case ToolType.BLACK_MARKER.value:
                pygame.draw.circle(screen, (0, 0, 0), (self.x + tool_x_offset, self.y + tool_y_offset), 10)
            case ToolType.WHITE_MARKER.value:
                pygame.draw.circle(screen, (255, 255, 255), (self.x + tool_x_offset, self.y + tool_y_offset), 10)
            case ToolType.BLACK_RING.value:
                pygame.draw.circle(screen, (0, 0, 0), (self.x + tool_x_offset, self.y + tool_y_offset), 10, 2)
            case ToolType.WHITE_RING.value:
                pygame.draw.circle(screen, (255, 255, 255), (self.x + tool_x_offset, self.y + tool_y_offset), 10, 2)
            case ToolType.RUBBER.value:
                pygame.draw.rect(screen, (255, 255, 255), (self.x + tool_x_offset - 10, self.y + tool_y_offset - 10, 20, 20))
                pygame.draw.rect(screen, (0, 0, 0), (self.x + tool_x_offset - 10, self.y + tool_y_offset - 10, 20, 20), 2)

    def draw(self, screen):
        # Draw the current tool
        self.draw_tool(screen)

        # Draw the current tool's name
        tool_name = self.get_tool_name(self.get_current_tool())
        text_x_offset = 20  # keep the text centered
        text_y_offset = BUTTONS_HEIGHT + 10  # Adjust text position below tool
        draw_text(screen, "Current Tool", FONT, BLACK, self.x + text_x_offset - FONT.size("Current Tool")[0] // 2, self.y - (4 * BUTTONS_HEIGHT / 6) - 10)
        draw_text(screen, tool_name, FONT, STEEL_BLUE, self.x + text_x_offset - FONT.size(tool_name)[0] // 2, self.y + text_y_offset)

        # Draw the buttons
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        for button in self.buttons:
            button.click(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.change_tool(-1)
            elif event.key == pygame.K_RIGHT:
                self.change_tool(1)

    def get_current_tool(self):
        return self.tools[self.current_tool_index]

    def get_tool_name(self, tool_type):
        if tool_type == ToolType.BLACK_MARKER:
            return "Black Marker"
        elif tool_type == ToolType.WHITE_MARKER:
            return "White Marker"
        elif tool_type == ToolType.WHITE_RING:
            return "White Ring"
        elif tool_type == ToolType.BLACK_RING:
            return "Black Ring"
        elif tool_type == ToolType.RUBBER:
            return "Rubber"