import pygame
import math
from settings import WIDTH, HEIGHT
from model.board import Board
# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# Constants
VERTEX_RADIUS = 3  # Size of the vertex dots

class BoardView:
    def __init__(self,board):
        self.vertices = {}
        for row in range(board.sizeY):
            for col in range(board.sizeX):
                if board.matrix[row][col] != -1:
                    x, y = self.matrix_position_to_pixel(row, col)
                    self.vertices[(row, col)] = (x, y)

    def draw_board(self, screen,board):

        # Second pass: Draw all edges
        for row in range(board.sizeY):
            for col in range(board.sizeX):
                if board.matrix[row][col] != -1:
                    x, y = self.matrix_position_to_pixel(row, col)
                    # Draw neighbor edges
                    for (dx, dy) in [(-1, 1), (0,-2),(0,2), (1,-1), (-1,-1), (1,1) ]:
                        if (row + dy, col + dx) in self.vertices:
                            x2, y2 = self.vertices[(row + dy, col + dx)]
                            pygame.draw.line(screen, BLACK, (x, y), (x2, y2), 2)

        for vertice in self.vertices.values():
            pygame.draw.circle(screen, RED, vertice, VERTEX_RADIUS)

    def matrix_position_to_pixel(self, row, col):
        """Convert hex grid coordinates to pixel positions (center points)."""
        x = col * 2 * 20 + WIDTH // 2 - 220  # 20 = base radius
        y = (row + 1) * math.sqrt(3) * 20 * 0.7 + HEIGHT // 2 - 300
        return int(x), int(y)

