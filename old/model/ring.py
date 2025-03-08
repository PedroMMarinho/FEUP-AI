import pygame

class Ring:
    def __init__(self, x, y, radius, width, color, hover_color, action):
        self.rect = pygame.Rect(int(x - radius), int(y - radius), int(radius * 2), int(radius * 2))
        self.width = width
        self.radius = radius
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.hover_color if is_hovered else self.color

        pygame.draw.circle(screen, current_color, self.rect, radius=self.radius, width=self.width)

