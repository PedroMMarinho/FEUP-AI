import pygame
from ui import draw_text

class ClickButton:
    def __init__(self,text, x, y, height, width, font, button_color, text_color, hover_color, hover_text_color, border_color=None, shadow_color=None, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.font = font
        self.action = action
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Colors
        self.color = button_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.hover_text_color = hover_text_color
        self.border_color = border_color
        self.shadow_color = shadow_color

    def draw(self, screen):
        pos = pygame.mouse.get_pos()

        is_hovered = self.rect.collidepoint(pos)

        button_color = self.hover_color if is_hovered else self.color

        text_color = self.hover_text_color if is_hovered else self.text_color

        # Shadow
        if self.shadow_color is not None:
            shadow_offset = 4
            pygame.draw.rect(screen, self.shadow_color, (self.x + shadow_offset, self.y + shadow_offset, self.width, self.height), border_radius=10)

        # Border
        if self.border_color is not None:
            pygame.draw.rect(screen, self.border_color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), border_radius=12)

        # Button
        pygame.draw.rect(screen, button_color, self.rect, border_radius=10)

        # Text
        text_x = self.x + (self.width - self.font.size(self.text)[0]) // 2
        text_y = self.y + (self.height - self.font.get_height()) // 2

        draw_text(screen, self.text, self.font, text_color, text_x, text_y)

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos) and self.action:
            self.action()


class Button:
    def __init__(self, text, screen, width, height, font, color, text_color, isSelected=False):
        self.text = text
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.color = color
        self.text_color = text_color
        self.isSelected = isSelected
        self.rect = pygame.Rect(0, 0, width, height)

    def draw(self, x, y):
        self.rect.x = x
        self.rect.y = y

        rect = pygame.Rect(x, y, self.width, self.height)
        final_color = self.color
        final_text_color = self.text_color
        if self.isSelected:
            # Darken the button color (reduce RGB values)
            final_color = tuple(max(0, int(c * 0.7)) for c in self.color)  # Darken by 30%
            # Lighten the text color (increase RGB values)
            final_text_color = tuple(min(255, int(c + (255 - c) * 0.4)) for c in self.text_color)  # Lighten by 40%

        pygame.draw.rect(self.screen, final_color, rect)
        draw_text(self.screen,self.text, self.font, final_text_color, x + self.width // 2 - self.font.size(self.text)[0] // 2, y + self.height // 2 - self.font.get_height() // 2)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y) 
    

class PieceButton:
    def __init__(self, screen, width, height, font, color, text_color):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.color = color
        self.text_color = text_color
        self.rect = pygame.Rect(0, 0, width, height)
        self.state = 1  # Default state

    def draw(self, x, y):
        self.rect.topleft = (x, y)  # Update position
        string = "Black" if self.state == 2 else "White"
        pygame.draw.rect(self.screen, self.color, self.rect)
        draw_text(self.screen, string, self.font, self.text_color, 
                  x + self.width // 2 - self.font.size(string)[0] // 2, 
                  y + self.height // 2 - self.font.get_height() // 2)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def toggle(self):
        self.state = 1 if self.state == 2 else 2

        if self.state == 2:
            self.color = (0, 0, 0)
            self.text_color = (255, 255, 255)
        else:
            self.color = (255, 255, 255)
            self.text_color = (0, 0, 0)