import pygame
import math
from enum import Enum
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK
# Board class - MatrixSize = 11x19

class BoardSpaceType(Enum): 
    INVALID = -1 
    EMPTY = 0
    PLAYER1_MARKER = 1
    PLAYER2_MARKER = 2
    PLAYER1_RING = 3
    PLAYER2_RING = 4

class BoardPhase(Enum):
    PREP = 0
    GAME = 1

class Board:
    def __init__(self, x_offset=None, y_offset=None, radius=None):
        self.sizeX = 11
        self.sizeY = 19
        self.x_offset = x_offset if x_offset is not None else SCREEN_WIDTH // 2 - 220 
        self.y_offset = y_offset if y_offset is not None else SCREEN_HEIGHT // 2 - 300 
        self.radius = radius if radius is not None else 30
        self.matrix = self.createBoard() 
        self.vertices = self.createBoardVertices()
        self.phase = BoardPhase.PREP
        self.num_rings1 = 0
        self.num_rings2 = 0
        self.num_markers = 51
        self.marker_placed = False
        self.ring_pos = None


    def update_matrix(self, matrix):
        self.matrix = matrix
        self.vertices = self.createBoardVertices()

    def createBoard(self):
         
        board = [[-1,-1,-1,-1,0,-1,0,-1,-1,-1,-1], 
                 [-1,-1,-1,0,-1,0,-1,0,-1,-1,-1], 
                 [-1,-1,0,-1,0,-1,0,-1,0,-1,-1], 
                 [-1,0,-1,0,-1,0,-1,0,-1,0,-1], 
                 [-1,-1,0,-1,0,-1,0,-1,0,-1,-1], 
                 [-1,0,-1,0,-1,0,-1,0,-1,0,-1],
                 [0,-1,0,-1,0,-1,0,-1,0,-1,0],
                 [-1,0,-1,0,-1,0,-1,0,-1,0,-1],
                 [0,-1,0,-1,0,-1,0,-1,0,-1,0],
                 [-1,0,-1,0,-1,0,-1,0,-1,0,-1],
                 [0,-1,0,-1,0,-1,0,-1,0,-1,0],
                 [-1,0,-1,0,-1,0,-1,0,-1,0,-1], 
                 [0,-1,0,-1,0,-1,0,-1,0,-1,0], 
                 [-1,0,-1,0,-1,0,-1,0,-1,0,-1], 
                 [-1,-1,0,-1,0,-1,0,-1,0,-1,-1], 
                 [-1,0,-1,0,-1,0,-1,0,-1,0,-1], 
                 [-1,-1,0,-1,0,-1,0,-1,0,-1,-1], 
                 [-1,-1,-1,0,-1,0,-1,0,-1,-1,-1], 
                 [-1,-1,-1,-1,0,-1,0,-1,-1,-1,-1]]
        return board
    
    def createBoardVertices(self):
        vertices = {}
        for row in range(self.sizeY):
            for col in range(self.sizeX):
                x, y = self.matrix_position_to_pixel(row, col)
                if self.matrix[row][col] != -1:
                    vertices[(x, y)] = (col, row)
        return vertices

    
    def matrix_position_to_pixel(self, row, col):
        """Convert hex grid coordinates to pixel positions (center points)."""
        x = col * 2 * self.radius + self.x_offset
        y = (row + 1) * math.sqrt(3) * self.radius * 0.7 + self.y_offset
        return int(x), int(y)    


    def place_piece(self, pos, piece): 
        x,y = pos
        self.matrix[x][y] = piece

    def perform_move(self,startPos,endPos, player):

        (colStartMatrix, rowStartMatrix) = self.vertices[startPos]

        if self.phase == BoardPhase.PREP:
            self.place_piece((rowStartMatrix, colStartMatrix),player+2)
            if player == 1:
                self.num_rings1 += 1
            else:
                self.num_rings2 += 1
        
        elif self.phase == BoardPhase.GAME:
            if self.marker_placed:
                (colEndMatrix, rowEndMatrix) = self.vertices[endPos]

                (vectorX,vectorY) = (colEndMatrix -colStartMatrix, rowEndMatrix - rowStartMatrix) # determine direction of move
                if vectorX == 0: 
                    vectorY = vectorY // abs(vectorY)
                else: 
                    (vectorX,vectorY) = (vectorX // abs(vectorX), vectorY // abs(vectorY))
                
                x = colStartMatrix + vectorX
                y = rowStartMatrix + vectorY 

                while x != colEndMatrix or y != rowEndMatrix:
                    if self.matrix[y][x] != BoardSpaceType.EMPTY.value: 
                        self.place_piece((y,x),3- self.matrix[y][x]) # flip
                    x += vectorX
                    y += vectorY

                self.place_piece((rowEndMatrix, colEndMatrix),player+2)
            else:
                self.place_piece((rowStartMatrix, colStartMatrix),player)

    def valid_moves(self, player):
        moves = []
        if (self.phase == BoardPhase.PREP and self.num_rings1 == 5 and self.num_rings2 == 5):
            self.phase = BoardPhase.GAME

        if self.phase == BoardPhase.GAME and self.marker_placed:
            moves = self.get_ring_moves()
        else:
            for (x,y), (col, row) in self.vertices.items():
                if self.phase == BoardPhase.PREP and self.matrix[row][col] == BoardSpaceType.EMPTY.value:
                    moves.append((x,y))
                elif self.phase == BoardPhase.GAME and self.matrix[row][col] == BoardSpaceType.PLAYER1_RING.value and player == 1 and not self.marker_placed:
                    moves.append((x,y))
                elif self.phase == BoardPhase.GAME and self.matrix[row][col] == BoardSpaceType.PLAYER2_RING.value and player == 2 and not self.marker_placed:
                    moves.append((x,y))
        return moves

    def get_ring_moves(self):
        moves = []
        moves.extend(self.get_ring_moves_direction((0,-2)))
        moves.extend(self.get_ring_moves_direction((0,2)))
        moves.extend(self.get_ring_moves_direction((1,1)))
        moves.extend(self.get_ring_moves_direction((1,-1)))
        moves.extend(self.get_ring_moves_direction((-1,-1)))
        moves.extend(self.get_ring_moves_direction((-1,1)))
        return moves
        

    def get_ring_moves_direction(self,vector):
        (ringPosX, ringPosY) = self.ring_pos
        (ringPosXMatrix, ringPosYMatrix) = self.vertices[(ringPosX, ringPosY)]
        (vectorX, vectorY ) = vector
        print(f"Vector {vector} --- rinnBegin {ringPosXMatrix, ringPosYMatrix}")
        jumped = False
        x = ringPosXMatrix + vectorX
        y = ringPosYMatrix + vectorY
        moves = []
        while x >= 0 and y>= 0 and x < self.sizeX and y < self.sizeY:
            if self.matrix[y][x] == BoardSpaceType.INVALID.value: 
                break
            if self.matrix[y][x] == BoardSpaceType.PLAYER1_RING.value or self.matrix[y][x] == BoardSpaceType.PLAYER2_RING.value:
                break
            if self.matrix[y][x] == BoardSpaceType.EMPTY.value:
                posX, posY = self.matrix_position_to_pixel(y,x)
                print(f"Matrix: [{y}, {x}] | Pos: ({posX}, {posY})")
                moves.append((posX, posY))
                if jumped:
                    break
            if self.matrix[y][x] == BoardSpaceType.PLAYER1_MARKER.value or self.matrix[y][x] == BoardSpaceType.PLAYER2_MARKER.value:
                jumped = True
            x = x + vectorX
            y = y + vectorY
        return moves
                

    def draw(self, screen):
        for (x,y), (col, row) in self.vertices.items():
            for (dx, dy) in [(-1, 1), (0,-2),(0,2), (1,-1), (-1,-1), (1,1) ]:
                        x2, y2 = self.matrix_position_to_pixel(row+dy,col+dx)
                        if (x2,y2) in self.vertices:
                            pygame.draw.line(screen, BLACK, (x, y), (x2, y2), 2)

            if self.matrix[row][col] == BoardSpaceType.PLAYER1_RING.value:
                pygame.draw.circle(screen, (0, 0, 255), (x, y), 12, 4)

            elif self.matrix[row][col] == BoardSpaceType.PLAYER1_MARKER.value:
                pygame.draw.circle(screen, (0, 0, 255), (x, y), 12)

            elif self.matrix[row][col] == BoardSpaceType.PLAYER2_RING.value:
                pygame.draw.circle(screen, (255, 0, 0), (x, y), 12, 4)

            elif self.matrix[row][col] == BoardSpaceType.PLAYER2_MARKER.value:
                pygame.draw.circle(screen, (255, 0, 0), (x, y), 12)

        '''
        # Second pass: Draw all edges
        for row in range(self.sizeY):
            for col in range(self.sizeX):
                if self.matrix[row][col] != -1:
                    x, y = self.matrix_position_to_pixel(row, col)
                    # Draw neighbor edges
                    for (dx, dy) in [(-1, 1), (0,-2),(0,2), (1,-1), (-1,-1), (1,1) ]:
                        if (row + dy, col + dx) in self.vertices:
                            x2, y2 = self.vertices[(row + dy, col + dx)]
                            pygame.draw.line(screen, BLACK, (x, y), (x2, y2), 2)
        '''


            

        

    
    


        

           