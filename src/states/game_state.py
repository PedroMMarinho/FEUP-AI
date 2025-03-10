import pygame
import math
from states.state import State
from board import Board, BoardPhase

class GameState(State):

    def __init__(self, game):
        super().__init__(game)
        self.board = Board() 
        self.player = 1
        self.valid_moves = self.board.valid_moves(self.player)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for (valid_x,valid_y) in self.valid_moves:
                if self.is_within_hitbox(x, y, valid_x, valid_y):
                    print(valid_x,valid_y)
                    if self.board.phase == BoardPhase.PREP:
                        self.board.perform_move((valid_x,valid_y), (0,0), self.player)
                        self.change_player()
                    elif self.board.phase == BoardPhase.GAME:
                        if not self.board.marker_placed:
                            self.board.perform_move((valid_x,valid_y), (0,0), self.player)
                            self.board.marker_placed = True
                            self.board.ring_pos = (valid_x,valid_y)
                        else:
                            self.board.perform_move(self.board.ring_pos, (valid_x,valid_y), self.player)
                            self.board.marker_placed = False
                            self.board.ring_pos = None
                            self.change_player()
                    break
            self.valid_moves = self.board.valid_moves(self.player)

    def draw(self):
        self.board.draw(self.game.screen)
        for x, y in self.valid_moves:
            pygame.draw.circle(self.game.screen, (0, 255, 0), (x, y), 12 ,4)

    def is_within_hitbox(self, mouse_x, mouse_y, piece_x, piece_y):
        """
        Checks if the mouse click is within the hitbox (a circle around the piece).
        """
        distance = math.sqrt((mouse_x - piece_x) ** 2 + (mouse_y - piece_y) ** 2)
        return distance <= 12

    def change_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1
            