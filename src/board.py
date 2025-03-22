import pygame
import math
from enum import Enum
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK, PLAYER1_COLOR, PLAYER2_COLOR
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

class BoardAction(Enum):
    PLACE_RING = "Place Ring"
    PLACE_MARKER = "Place Marker"
    MOVE_RING = "Move Ring"
    REMOVE_5LINE = "Remove a 5 line group"
    REMOVE_RING = "Remove Ring"

class Board:
    def __init__(self, x_offset=None, y_offset=None, radius=None, matrix=None):
        self.sizeX = 11
        self.sizeY = 19
        self.radius = radius if radius is not None else 29
        self.calculate_offsets()
        if x_offset is not None:
            self.x_offset = x_offset
        if y_offset is not None:
            self.y_offset = y_offset

        self.matrix = self.createBoard() if matrix is None else matrix
        self.vertices = self.createBoardVertices()
        self.phase = BoardPhase.PREP
        self.next_action = BoardAction.PLACE_RING
        self.num_rings1 = 0
        self.num_rings2 = 0
        self.num_markers = 51
        self.marker_placed = False
        self.ring_pos = None
        self.remove_ring_phase = False
        if matrix is not None:
            self.reload_board()
            if self.num_markers != 51:
                self.phase = BoardPhase.GAME
                self.next_action = BoardAction.PLACE_MARKER

    def __str__(self):
        """Return a string representation of the board matrix."""
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.matrix)


    def calculate_offsets(self):
        board_width = (self.sizeX-1) * 2 * self.radius  # Width based on hex spacing
        board_height = (self.sizeY-1) * math.sqrt(3) * self.radius * 0.7# Height based on row spacing

        # Center the board
        self.x_offset = (SCREEN_WIDTH - board_width) // 2
        self.y_offset = (SCREEN_HEIGHT - (board_height + board_height/10)) // 2

    def reload_board(self):
        for row in range(self.sizeY):
            for col in range(self.sizeX):
                matrix_elem = self.matrix[row][col]
                if matrix_elem == BoardSpaceType.PLAYER1_MARKER.value or matrix_elem == BoardSpaceType.PLAYER2_MARKER.value:
                    self.num_markers -= 1
                elif matrix_elem == BoardSpaceType.PLAYER1_RING.value:
                    self.num_rings1 += 1
                elif matrix_elem == BoardSpaceType.PLAYER2_RING.value:
                    self.num_rings2 += 1
                
    def update_matrix(self, matrix):
        self.matrix = matrix
        self.vertices = self.createBoardVertices()

    def clear_board(self):
            self.matrix = self.createBoard()
            self.num_rings1 = 0
            self.num_rings2 = 0
            self.num_markers = 51

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
            self.next_action = BoardAction.PLACE_MARKER

        if self.phase == BoardPhase.GAME and self.marker_placed and not self.remove_ring_phase:
            moves = self.get_ring_moves()
            self.next_action = BoardAction.MOVE_RING
        else:
            if self.remove_ring_phase:
                self.next_action = BoardAction.REMOVE_RING
            elif self.phase == BoardPhase.GAME:
                self.next_action = BoardAction.PLACE_MARKER
            for (x,y), (col, row) in self.vertices.items():
                if self.phase == BoardPhase.PREP and self.matrix[row][col] == BoardSpaceType.EMPTY.value:
                    moves.append((x,y))
                elif self.phase == BoardPhase.GAME and self.matrix[row][col] == BoardSpaceType.PLAYER1_RING.value and player == 1 and (not self.marker_placed or self.remove_ring_phase) and not self.ring_blocked(x,y):
                    moves.append((x,y))
                elif self.phase == BoardPhase.GAME and self.matrix[row][col] == BoardSpaceType.PLAYER2_RING.value and player == 2 and (not self.marker_placed or self.remove_ring_phase) and not self.ring_blocked(x,y):
                    moves.append((x,y))                        
        return moves
    
    def ring_blocked(self,x,y):
        self.ring_pos = (x,y)
        moves = self.get_ring_moves()
        self.ring_pos = None
        if len(moves) != 0: 
            return False
        return True

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
        #print(f"Vector {vector} --- rinnBegin {ringPosXMatrix, ringPosYMatrix}")
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
                #print(f"Matrix: [{y}, {x}] | Pos: ({posX}, {posY})")
                moves.append((posX, posY))
                if jumped:
                    break
            if self.matrix[y][x] == BoardSpaceType.PLAYER1_MARKER.value or self.matrix[y][x] == BoardSpaceType.PLAYER2_MARKER.value:
                jumped = True
            x = x + vectorX
            y = y + vectorY
        return moves
    
    def check_x_in_line(self, n, player):
        all_lines = dict()
        visited = dict()

        for (x,y), (col, row) in self.vertices.items():
            if self.matrix[row][col] == player:
                for direction in [((0,-2),(0,2)), ((1,1),(-1,-1)), ((1,-1),(-1,1))]:
                    #print(f"MTRXPOS: {col,row} | PLAYER {player} | DIRECTION: {direction}")
                    visited.setdefault(direction, set())
                    if (col,row) in visited[direction]:
                      #  print("A")
                        continue
                    else:
                       # print("B")
                        visited[direction].add((col,row))
                        line = []
                        line.append((x,y))
                       # print(f"APENDING TO LINE FIRST: {col,row}")
                        for (vectorX, vectorY) in direction:
                            c = col + vectorX
                            r = row + vectorY
                           # print(f"DIRECTION: {vectorX, vectorY}  |||| POS: {c,r}")
                            while c >= 0 and r>= 0 and c < self.sizeX and r < self.sizeY:
                                if self.matrix[r][c] != player:
                                 #   print("break")
                                    break
                               # print(f"APENDING TO LINE: {c,r}")
                                visited[direction].add((c,r))
                                line.append((self.matrix_position_to_pixel(r,c)))


                                c += vectorX
                                r += vectorY
                        if len(line) >= n:
                            all_lines.setdefault(direction, []).append(line)

       # print(f"LINE5: {all_lines}")
       # print(f"VISITED: {visited}")
       # print("-------------------------------")
        if len(all_lines) > 0 and n == 5 :
            self.next_action = BoardAction.REMOVE_5LINE
        return all_lines

    def dif_markers(self,player):
        for row in range(self.sizeY):
            for col in range(self.sizeX):
                if self.matrix[row][col] == BoardSpaceType.PLAYER1_MARKER.value:
                    marker_1+=1
                elif self.matrix[row][col] == BoardSpaceType.PLAYER2_MARKER.value:
                    marker_2+=1
        if player == 1:
            return marker_1 - marker_2
        else:
            return marker_2 - marker_1

    #error
    def remove_markers(self,sequence):
        for (x,y) in sequence:
            (col, row) = self.vertices[(x,y)]
            self.matrix[row][col] = BoardSpaceType.EMPTY.value
            self.num_markers += 1

    def remove_ring(self, pos):
        (x, y) = pos
        (col, row) = self.vertices[(x,y)]
        self.matrix[row][col] = BoardSpaceType.EMPTY.value


    def draw(self, screen):
        white_markers = []
        white_rings = []
        black_markers = []
        black_rings = []

        for (x,y), (col, row) in self.vertices.items():
            for (dx, dy) in [(-1, 1), (0,-2),(0,2), (1,-1), (-1,-1), (1,1) ]:
                        x2, y2 = self.matrix_position_to_pixel(row+dy,col+dx)
                        if (x2,y2) in self.vertices:
                            pygame.draw.aaline(screen, BLACK, (x, y), (x2, y2))
            if self.matrix[row][col] == BoardSpaceType.PLAYER1_RING.value:
                white_rings.append((x,y))

            elif self.matrix[row][col] == BoardSpaceType.PLAYER1_MARKER.value:
                white_markers.append((x,y))

            elif self.matrix[row][col] == BoardSpaceType.PLAYER2_RING.value:
                black_rings.append((x,y))

            elif self.matrix[row][col] == BoardSpaceType.PLAYER2_MARKER.value:
                black_markers.append((x,y))
                
        for (x,y) in white_rings:
            pygame.draw.circle(screen, PLAYER1_COLOR, (x, y), 12, 5)

        for (x,y) in white_markers:
            pygame.draw.circle(screen, PLAYER1_COLOR, (x, y), 12)

        for (x,y) in black_rings:
            pygame.draw.circle(screen, PLAYER2_COLOR, (x, y), 12, 5)

        for (x,y) in black_markers:
            pygame.draw.circle(screen, PLAYER2_COLOR, (x, y), 12)


            
        

    
    


        

           