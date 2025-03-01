import pygame
from model.board import generate_hex_grid
HEX_COLOR = (0, 0, 0)
HEX_RADIUS = 40
VERTEX_COLOR = (255, 0, 0)
LINE_COLOR = (150, 150, 150)

def draw_board(screen):

    for hexagon in generate_hex_grid():
        pygame.draw.polygon(screen, HEX_COLOR, hexagon.corners, 2)
        for vertex in hexagon.vertices:
            pygame.draw.circle(screen, VERTEX_COLOR, (int(vertex[0]), int(vertex[1])), 3)
        for line in hexagon.internal_lines:
            pygame.draw.line(screen, LINE_COLOR, (line[0], line[1]), (line[2], line[3]), 1)
    pygame.display.flip()