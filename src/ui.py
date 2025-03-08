import pygame

def draw_text(screen,text, font, color, x, y):
    text_surf = font.render(text, True, color)
    screen.blit(text_surf, (x, y))

def draw_button(screen,text, x, y, width, height, font, color, text_color):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect)
    draw_text(screen,text, font, text_color, x + width // 2 - font.size(text)[0] // 2, y + height // 2 - font.get_height() // 2)
    
    return rect
