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
        self.valid_ring_moves = []
        self.line5 = []
        self.active_connect5 = False
        self.valid_connect5 = []
        self.selected_sequence = None
        self.possible_sequences = []

    def handle_events(self, event):
        self.valid_ring_moves = []
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if len(self.valid_moves) == 0 and self.active_connect5:
                    print("REMOVE MARKERS STATE")
                    self.board.remove_markers(self.valid_connect5)
                    self.board.remove_ring_phase = True
                    self.active_connect5 = False
                    self.valid_connect5 = []
                else:
                    x, y = event.pos
                    for (valid_x,valid_y) in self.valid_moves:
                        if self.is_within_hitbox(x, y, valid_x, valid_y):
                            #print(valid_x,valid_y)
                            if self.board.phase == BoardPhase.PREP:
                                self.board.perform_move((valid_x,valid_y), (0,0), self.player)
                                self.change_player()
                            elif self.board.phase == BoardPhase.GAME:
                                if not self.board.marker_placed:
                                    self.board.perform_move((valid_x,valid_y), (0,0), self.player)
                                    self.board.marker_placed = True
                                    self.board.num_markers -= 1
                                    self.board.ring_pos = (valid_x,valid_y)
                                elif not self.active_connect5 and not self.board.remove_ring_phase:
                                    self.board.perform_move(self.board.ring_pos, (valid_x,valid_y), self.player)
                                    self.line5 = self.board.check_5_line(self.player)
                                    self.active_connect5 = len(self.line5) > 0

                                    if not self.active_connect5:
                                        self.board.marker_placed = False
                                        self.board.ring_pos = None
                                        self.change_player()

                                    # valid moves vazio meter fora
                                # select a ring to remove 
                                # change player , false connect5 markerplaced rinpos
                                elif self.board.remove_ring_phase:
                                    print("REMOVE RING STATE")
                                    self.board.remove_ring((valid_x,valid_y))
                                    self.board.remove_ring_phase = False
                                    self.board.marker_placed = False
                                    self.board.ring_pos = None
                                    if self.player == 1:
                                        self.board.num_rings1 -= 1
                                    else: 
                                        self.board.num_rings2 -= 1
                                    self.change_player()

                            break
                if self.active_connect5:
                    self.valid_moves = []
                else:
                    self.valid_moves = self.board.valid_moves(self.player)
            if event.button == 3 and self.active_connect5:
                print("RIGHT CLICK")
                print(f"SELCT SEQ: {self.selected_sequence}")
                if self.selected_sequence != None:
                    sequence_index = self.possible_sequences.index(self.selected_sequence)
                    next_index = (sequence_index + 1) % len(self.possible_sequences)
                    self.selected_sequence = self.possible_sequences[next_index]

                    if len(self.selected_sequence) <= 2:
                        self.valid_connect5 = self.selected_sequence  # Return all if 4 or fewer exist
                    else:
                        # Try to center around hovered point
                        start_index = max(0, min(next_index - 1, len(self.selected_sequence) - 2))
                        self.valid_connect5 = self.selected_sequence[start_index:start_index + 2]

                    

        if event.type == pygame.MOUSEMOTION and self.board.phase == BoardPhase.GAME:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not self.board.marker_placed:
                for (valid_x,valid_y) in self.valid_moves:
                    if self.is_within_hitbox(mouse_x, mouse_y, valid_x, valid_y):
                        self.board.ring_pos = (valid_x,valid_y)
                        self.valid_ring_moves = self.board.get_ring_moves()
            
            if self.active_connect5:
                hovered_point = None
                self.selected_sequence = None
                self.possible_sequences = []
                for sequences in self.line5.values():
                    print(f"SEQ1: {sequences} || MOUSE: {mouse_x,mouse_y}")
                    for sequence in sequences:
                        print(f"SEQ2: {sequence}")
                        for (x,y) in sequence:
                            if self.is_within_hitbox(mouse_x, mouse_y, x, y):
                                hovered_point = (x,y)
                                self.possible_sequences.append(sequence)
                                if self.selected_sequence == None:
                                    self.selected_sequence = sequence
                                print(f"SEQUECEN : {sequence}")
                                break  # Found it, stop searching
                        if hovered_point:
                            break
                        #if hovered_point: -- para conseguir buscar com o ponto em varias direcoes
                           # break
                print(self.selected_sequence)
                if self.selected_sequence != None:
                    index = self.selected_sequence.index(hovered_point)
    
                    # Select 4 consecutive points
                    if len(self.selected_sequence) <= 2:
                        self.valid_connect5 = self.selected_sequence  # Return all if 4 or fewer exist
                    else:

                    # Try to center around hovered point
                        start_index = max(0, min(index - 1, len(self.selected_sequence) - 2))
                        self.valid_connect5 = self.selected_sequence[start_index:start_index + 2]

                        

                

    def draw(self):
        self.board.draw(self.game.screen)
        for x, y in self.valid_moves:
            pygame.draw.circle(self.game.screen, (0, 255, 0), (x, y), 12 ,4)
        for x, y in self.valid_ring_moves:
            pygame.draw.circle(self.game.screen, (0, 255, 255), (x, y), 12 ,4)
        for x, y in self.valid_connect5:
            pygame.draw.circle(self.game.screen, (255, 255, 0), (x, y), 12 ,4)

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
            