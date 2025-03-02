import pygame
from model.board import generate_hex_grid
HEX_COLOR = (0, 0, 0)
HEX_RADIUS = 40
VERTEX_COLOR = (255, 0, 0)
LINE_COLOR = (150, 150, 150)

def draw_board(screen):

    pygame.draw.line(screen, LINE_COLOR, (240, 350), (240, 590), 2) # vertical first
    pygame.draw.line(screen, LINE_COLOR, (960, 350), (960, 590), 2) # vertical last
    pygame.draw.line(screen, LINE_COLOR, (600, 150), (600, 790), 2) # vertical mid

    pygame.draw.line(screen, LINE_COLOR, (312, 230), (528, 110), 2) # diagonal first
    pygame.draw.line(screen, LINE_COLOR, (672, 830), (888, 710), 2) # diagonal last
    pygame.draw.line(screen, LINE_COLOR, (312, 630), (888, 310), 2) # diagonal mid

    for i in range(1,5):

        pygame.draw.line(screen, LINE_COLOR, (240 + 72*i, 270 - 40*i), (240 + 72*i, 670 + 40*i), 2)
        pygame.draw.line(screen, LINE_COLOR, (960 - 72*i, 270 - 40*i), (960 - 72*i, 670 + 40*i), 2)

        pygame.draw.line(screen, LINE_COLOR, (240, 270 + 80*i), (600 + 72*i, 70 + 40*i), 2)
        pygame.draw.line(screen, LINE_COLOR, (600 - 72*i, 870 - 40*i), (960, 670 - 80*i), 2)

    



    """
        for hexagon in generate_hex_grid():
            pygame.draw.polygon(screen, HEX_COLOR, hexagon.corners, 2)
            for vertex in hexagon.vertices:
                pygame.draw.circle(screen, VERTEX_COLOR, (int(vertex[0]), int(vertex[1])), 3)
            for line in hexagon.internal_lines:
                pygame.draw.line(screen, LINE_COLOR, (line[0], line[1]), (line[2], line[3]), 1)
        pygame.display.flip()
    """