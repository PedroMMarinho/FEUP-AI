import pygame
from config import FONT, STEEL_BLUE, LIGHT_CYAN, CADET_BLUE
def draw_text(screen,text, font, color, x, y):
    text_surf = font.render(text, True, color)
    screen.blit(text_surf, (x, y))

def draw_button(screen,text, x, y, width, height, font, color, text_color):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect)
    draw_text(screen,text, font, text_color, x + width // 2 - font.size(text)[0] // 2, y + height // 2 - font.get_height() // 2)
    
    return rect

def draw_input_box(screen, rect, text):
    pygame.draw.rect(screen, LIGHT_CYAN, rect, border_radius=10)
    pygame.draw.rect(screen, CADET_BLUE, rect, 2, border_radius=10)
    font_surface = FONT.render(text, True, STEEL_BLUE)
    screen.blit(font_surface, (rect.x + 5, rect.y + 10))
