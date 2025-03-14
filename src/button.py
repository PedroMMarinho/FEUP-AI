import pygame
from ui import draw_text

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