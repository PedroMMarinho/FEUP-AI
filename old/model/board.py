import math
from settings import WIDTH, HEIGHT
from enum import Enum
# Board class - MatrixSize = 11x19

class BoardSpaceType(Enum): 
    INVALID = -1 
    EMPTY = 0
    PLAYER1_MARKER = 1
    PLAYER2_MARKER = 2
    PLAYER1_RING = 3
    PLAYER2_RING = 4

class Board:
    def __init__(self):
        self.sizeX = 11
        self.sizeY = 19
        self.matrix = self.createBoard()

    def createBoard(self):
         
        board = [[-1,-1,-1,-1,0,-1,0,-1,-1,-1,-1], 
                 [-1,-1,-1,1,-1,2,-1,3,-1,-1,-1], 
                 [-1,-1,0,-1,0,-1,0,-1,4,-1,-1], 
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
 
    def placePiece(self, pos, piece): 
        (x,y) = pos
        self.matrix[x][y] = piece

    def performMove(self,startPos,endPos):
        (startPosX, startPosY) = startPos
        (endPosX,endPosY) = endPos
        ringType = self.board[startPosX][startPosY] # get the player of the ring
        (vectorX,vectorY) = (endPosX -startPosX, endPosY - startPosY) # determine direction of move
        if vectorX == 0: 
            vectorY = vectorY / abs(vectorY)
        else: 
            (vectorX,vectorY) = (vectorX / abs(vectorX), vectorY / abs(vectorY))
        
        self.placePiece(startPos,ringType-2)
        x = startPosX + vectorX
        y = startPosY + vectorY 

        while x != endPosX and y != endPosY:
            if self.matrix[x][y] != BoardSpaceType.EMPTY: 
                self.placePiece((x,y),3- self.matrix[x][y]) # flip
        
        self.placePiece(endPos,ringType)

    def getRingMoves(self,ringPos):
        moves = []
        moves.extend(self.getRingMovesDirection(ringPos,(0,-2)))
        moves.extend(self.getRingMovesDirection(ringPos,(0,2)))
        moves.extend(self.getRingMovesDirection(ringPos,(1,1)))
        moves.extend(self.getRingMovesDirection(ringPos,(1,-1)))
        moves.extend(self.getRingMovesDirection(ringPos,(-1,-1)))
        moves.extend(self.getRingMovesDirection(ringPos,(-1,1)))
        return moves
        

    def getRingMovesDirection(self,ringPos,vector):
        (ringPosX, ringPosY ) = ringPos
        (vectorX, vectorY ) = vector
        jumped = False
        x = ringPosX + vectorX
        y = ringPosY + vectorY
        moves = []
        while x >= 0 and y>= 0 and x < self.sizeX and y < self.sizeY:
            if self.matrix[x][y] == BoardSpaceType.INVALID: 
                break
            if self.matrix[x][y] == BoardSpaceType.PLAYER1_RING or self.matrix[x][y] == BoardSpaceType.PLAYER2_RING:
                break
            if self.matrix[x][y] == BoardSpaceType.EMPTY:
                moves.append((x,y))
                if jumped:
                    break
            if self.matrix[x][y] == BoardSpaceType.PLAYER1_MARKER or self.matrix[x][y] == BoardSpaceType.PLAYER2_MARKER:
                jumped = True
            x = ringPosX + vectorX
            y = ringPosY + vectorY
        return moves
                
            

        

    
    


        

           