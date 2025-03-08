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
    def __init__(self):
        self.sizeX = 11
        self.sizeY = 19
        self.matrix = self.createBoard()
        self.vertices = self.createBoardVertices()
        self.phase = BoardPhase.PREP
        self.num_rings1 = 0
        self.num_rings2 = 0
        self.marker_placed = False
        self.ring_pos = None

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
                    vertices[(x, y)] = (row, col)
        return vertices

    
    def matrix_position_to_pixel(self, row, col, radius=30):
        """Convert hex grid coordinates to pixel positions (center points)."""
        x = col * 2 * radius + SCREEN_WIDTH // 2 - 220 
        y = (row + 1) * math.sqrt(3) * radius * 0.7 + SCREEN_HEIGHT // 2 - 300 
        return int(x), int(y)    


    def place_piece(self, pos, piece): 
        x,y = pos
        self.matrix[x][y] = piece

    def perform_move(self,startPos,endPos, player):

        startPosMatrix = self.vertices[startPos]

        if BoardPhase.PREP:
            self.place_piece(startPosMatrix,player+2)
            if player == 1:
                self.num_rings1 += 1
            else:
                self.num_rings2 += 1
        
        elif BoardPhase.GAME:
            if self.marker_placed:
                (startPosX, startPosY) = startPos
                (endPosX,endPosY) = endPos
                (vectorX,vectorY) = (endPosX -startPosX, endPosY - startPosY) # determine direction of move
                if vectorX == 0: 
                    vectorY = vectorY / abs(vectorY)
                else: 
                    (vectorX,vectorY) = (vectorX / abs(vectorX), vectorY / abs(vectorY))
                
                x = startPosX + vectorX
                y = startPosY + vectorY 

                while x != endPosX and y != endPosY:
                    if self.matrix[x][y] != BoardSpaceType.EMPTY.value: 
                        self.place_piece((x,y),3- self.matrix[x][y]) # flip
                
                self.place_piece(endPos,player+2)
            else:
                self.place_piece(startPosMatrix,player)

    def valid_moves(self, player):
        print(self.phase)
        moves = []
        if (self.phase == BoardPhase.PREP and self.num_rings1 == 5 and self.num_rings2 == 5):
            self.phase = BoardPhase.GAME
        if self.phase == BoardPhase.GAME and self.marker_placed:
            moves = self.get_ring_moves()
        else:
            for (x,y), (row, col) in self.vertices.items():
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
        (ringPosX, ringPosY ) = self.ring_pos
        (vectorX, vectorY ) = vector
        jumped = False
        x = ringPosX + vectorX
        y = ringPosY + vectorY
        moves = []
        while x >= 0 and y>= 0 and x < self.sizeX and y < self.sizeY:
            if self.matrix[x][y] == BoardSpaceType.INVALID.value: 
                break
            if self.matrix[x][y] == BoardSpaceType.PLAYER1_RING.value or self.matrix[x][y] == BoardSpaceType.PLAYER2_RING.value:
                break
            if self.matrix[x][y] == BoardSpaceType.EMPTY.value:
                moves.append((x,y))
                if jumped:
                    break
            if self.matrix[x][y] == BoardSpaceType.PLAYER1_MARKER.value or self.matrix[x][y] == BoardSpaceType.PLAYER2_MARKER.value:
                jumped = True
            x = ringPosX + vectorX
            y = ringPosY + vectorY
        return moves
                

    def draw(self, screen):
        for (x,y), (row, col) in self.vertices.items():
            for (dx, dy) in [(-1, 1), (0,-2),(0,2), (1,-1), (-1,-1), (1,1) ]:
                        x2, y2 = self.matrix_position_to_pixel(row+dy,col+dx)
                        if (x2,y2) in self.vertices:
                            pygame.draw.line(screen, BLACK, (x, y), (x2, y2), 2)

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


            

        

    
    


        

           