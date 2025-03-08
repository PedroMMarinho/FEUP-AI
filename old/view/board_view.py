import pygame
import math
from settings import WIDTH, HEIGHT
from model.board import Board
from model.button import GameButton
# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (160,160,160)
# Constants
VERTEX_RADIUS = 3  # Size of the vertex dots

class BoardView:
    def __init__(self,board):
        self.vertices = {}
        self.buttons = {}
        for row in range(board.sizeY):
            for col in range(board.sizeX):
                x, y = self.matrix_position_to_pixel(row, col)
                if board.matrix[row][col] != -1:
                    self.vertices[(row, col)] = (x, y)
                if board.matrix[row][col] == 0:
                    button = GameButton("blank",x,y,BLACK,BLACK,None)

                if board.matrix[row][col] == 1:
                    button = GameButton("marker",x,y,BLACK,BLACK,None)

                if board.matrix[row][col] == 2:
                    button = GameButton("marker",x,y,BLACK,BLACK,None)

                if board.matrix[row][col] == 3:
                    button = GameButton("ring",x,y,BLACK,BLACK,None)

                if board.matrix[row][col] == 4:
                    button = GameButton("ring",x,y,BLACK,BLACK,None)
    
                self.buttons.append(button)

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

        for button in self.buttons:
            button.draw(screen)


    def matrix_position_to_pixel(self, row, col):
        """Convert hex grid coordinates to pixel positions (center points)."""
        x = col * 2 * 30 + WIDTH // 2 - 220 # 20 = base radius
        y = (row + 1) * math.sqrt(3) * 30 * 0.7 + HEIGHT // 2 - 300 
        return int(x), int(y)
    