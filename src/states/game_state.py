import pygame
import math
from states.state import State
from board import Board, BoardPhase
from mode import GameMode

class GameState(State):

    def __init__(self, game , mode ,board, player=1,bot1_difficulty=None, bot2_difficulty=None):
        super().__init__(game)
        self.board = board
        self.player = player
        self.valid_moves = self.board.valid_moves(self.player)
        self.valid_ring_moves = []
        self.game_mode = mode

    def handle_events(self, event):
        self.valid_ring_moves = []
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
                            self.board.num_markers -= 1
                            self.board.ring_pos = (valid_x,valid_y)
                        else:
                            self.board.perform_move(self.board.ring_pos, (valid_x,valid_y), self.player)
                            self.board.marker_placed = False
                            self.board.ring_pos = None
                            self.change_player()
                    break
            self.valid_moves = self.board.valid_moves(self.player)
        if event.type == pygame.MOUSEMOTION and self.board.phase == BoardPhase.GAME and not self.board.marker_placed:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for (valid_x,valid_y) in self.valid_moves:
                if self.is_within_hitbox(mouse_x, mouse_y, valid_x, valid_y):
                    self.board.ring_pos = (valid_x,valid_y)
                    self.valid_ring_moves = self.board.get_ring_moves()

    def draw(self):
        self.board.draw(self.game.screen)
        for x, y in self.valid_moves:
            pygame.draw.circle(self.game.screen, (0, 255, 0), (x, y), 12 ,4)
        for x, y in self.valid_ring_moves:
            pygame.draw.circle(self.game.screen, (0, 255, 255), (x, y), 12 ,4)

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
            