import pygame
import pygame.gfxdraw 
import math
from ui import draw_text
from states.state import State
from board import Board, BoardPhase
from mode import GameMode
from json_actions import load_boards

class GameState(State):

    def __init__(self, game , mode, player="White", bot1_mode=None, bot1_difficulty=None, bot2_mode=None, bot2_difficulty=None):
        super().__init__(game)
        self.game_mode = mode
        self.game_type = "Normal"
        board_data = load_boards("src/boards.json")
        self.board = Board(matrix=board_data[game.selected_board]['layout'])
        self.player = 1
        self.valid_moves = self.board.valid_moves(self.player)
        self.valid_ring_moves = []
        self.line5 = []
        self.active_connect5 = False
        self.valid_connect5 = []
        self.selected_sequence = None
        self.possible_sequences = []  
        self.last_hovered_point = (-1,-1)
        self.line5_end_turn = False


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
                                if not self.board.marker_placed and not self.board.remove_ring_phase:
                                    self.board.perform_move((valid_x,valid_y), (0,0), self.player)
                                    self.board.marker_placed = True
                                    self.board.num_markers -= 1
                                    self.board.ring_pos = (valid_x,valid_y)
                                elif not self.active_connect5 and not self.board.remove_ring_phase:
                                    self.board.perform_move(self.board.ring_pos, (valid_x,valid_y), self.player)
                                    self.line5_end_turn = True
                                    self.verify_5line()

                                    if not self.active_connect5:
                                        self.board.marker_placed = False
                                        self.board.ring_pos = None
                                        self.change_player()

                                elif self.board.remove_ring_phase:
                                    print("REMOVE RING STATE")
                                    self.board.remove_ring((valid_x,valid_y))
                                    self.board.remove_ring_phase = False
                                    self.board.marker_placed = False
                                    self.board.ring_pos = None
                                    if self.player == 1:
                                        self.board.num_rings1 -= 1
                                        if self.game_type == "Blitz" and self.board.num_rings1 == 4 or self.game_type == "Normal" and self.board.num_rings1 == 2 :
                                            print("GAME OVER 1 WIN") # TODO: Handle finish game
                                    else: 
                                        self.board.num_rings2 -= 1
                                        if self.game_type == "Blitz" and self.board.num_rings2 == 4 or self.game_type == "Normal" and self.board.num_rings2 == 2 :
                                            print("GAME OVER 2 WIN") # TODO: Handle finish game
                                    if self.line5_end_turn:
                                        self.change_player()

                            break
                if self.active_connect5:
                    self.valid_moves = []
                else:
                    self.valid_moves = self.board.valid_moves(self.player)
            if event.button == 3 and self.active_connect5:
                print("RIGHT CLICK")
                print(f"SELCT SEQ: {self.selected_sequence}")
                if self.selected_sequence != None and len(self.possible_sequences) > 1:
                    print(f"POSSIBLE SQ {self.possible_sequences}")
                    sequence_index = self.possible_sequences.index(self.selected_sequence)
                    next_index = (sequence_index + 1) % len(self.possible_sequences)
                    self.selected_sequence = self.possible_sequences[next_index]
                    point_index = self.selected_sequence.index(self.last_hovered_point)


                    if len(self.selected_sequence) <= 2: # TODO: Change to 5
                        self.valid_connect5 = self.selected_sequence  # Return all if 4 or fewer exist
                    else:
                        # Try to center around hovered point
                        start_index = max(0, min(point_index - 1, len(self.selected_sequence) - 2)) # TODO: Change to 5
                        self.valid_connect5 = self.selected_sequence[start_index:start_index + 2] # TODO: Change to 5

                        if len(self.selected_sequence) % 2 == 1 and sequence_index == len(self.selected_sequence) // 2:
                            print(f"Appending case impar -- Idx {sequence_index} | Seq {self.selected_sequence}")
                            self.possible_sequences.append(self.selected_sequence[sequence_index:])

                    

        if event.type == pygame.MOUSEMOTION and self.board.phase == BoardPhase.GAME:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not self.board.marker_placed and not self.board.remove_ring_phase:
                for (valid_x,valid_y) in self.valid_moves:
                    if self.is_within_hitbox(mouse_x, mouse_y, valid_x, valid_y):
                        self.board.ring_pos = (valid_x,valid_y)
                        self.valid_ring_moves = self.board.get_ring_moves()
            
            if self.active_connect5:
                (x,y) = self.last_hovered_point
                if self.last_hovered_point == (-1,-1) or not self.is_within_hitbox(mouse_x, mouse_y, x, y):
                    hovered_point = None
                    selected_sequence = None
                    possible_sequences = []
                    enter = False
                    for sequences in self.line5.values():
                        print(f"SEQ1: {sequences} || MOUSE: {mouse_x,mouse_y}")
                        for sequence in sequences:
                            print(f"SEQ2: {sequence}")
                            for (x,y) in sequence:
                                if self.is_within_hitbox(mouse_x, mouse_y, x, y):
                                    hovered_point = (x,y)
                                    possible_sequences.append(sequence)
                                    if self.selected_sequence == None or hovered_point != self.last_hovered_point:
                                        selected_sequence = sequence
                                    self.last_hovered_point = hovered_point

                                    print(f"SEQUECEN : {sequence}")
                                    break  
                            if hovered_point:
                                break
                    if len(possible_sequences) != 0:
                        self.possible_sequences = possible_sequences
                        self.selected_sequence = selected_sequence
                        enter = True
                    print(self.selected_sequence)
                    if self.selected_sequence != None and enter:
                        index = self.selected_sequence.index(hovered_point)
        
                        # Select 5 consecutive points
                        if len(self.selected_sequence) <= 2: # TODO: Change to 5
                            self.valid_connect5 = self.selected_sequence 
                        else:
                            # Try to center around hovered point
                            start_index = max(0, min(index - 1, len(self.selected_sequence) - 2)) # TODO: Change to 5
                            self.valid_connect5 = self.selected_sequence[start_index:start_index + 2] # TODO: Change to 5

                            if len(self.selected_sequence) % 2 == 1 and index == len(self.selected_sequence) // 2:
                                print(f"Appending case impar -- Idx {index} | Seq {self.selected_sequence}")
                                self.possible_sequences.append(self.selected_sequence[index:])

                            
    def verify_5line(self):
        self.line5 = self.board.check_5_line(self.player)
        self.active_connect5 = len(self.line5) > 0
                

    def draw(self):
        self.board.draw(self.game.screen)
        draw_text(self.game.screen, "Next Action",pygame.font.Font(None, 50),(0,0,0),900,30)
        draw_text(self.game.screen, self.board.next_action.value,pygame.font.Font(None, 50),(0,0,0),900,100)

        draw_text(self.game.screen, "Player Turn",pygame.font.Font(None, 50),(0,0,0),100,30)
        if self.player == 1:
            draw_text(self.game.screen, "White",pygame.font.Font(None, 50),(0,0,0),100,100)
        else:
            draw_text(self.game.screen, "Black",pygame.font.Font(None, 50),(0,0,0),100,100)


        for x, y in self.valid_moves:
            pygame.gfxdraw.aacircle(self.game.screen, x, y, 14, (0, 255, 0))  # Green outline
            pygame.draw.circle(self.game.screen, (0, 255, 0), (x, y), 12 ,5)
        for x, y in self.valid_ring_moves:
            pygame.gfxdraw.aacircle(self.game.screen, x, y, 14, (255, 255, 0))  # Green outline
            pygame.draw.circle(self.game.screen, (255, 255, 0), (x, y), 12 ,5)
        for x, y in self.valid_connect5:
            pygame.gfxdraw.aacircle(self.game.screen, x, y, 16, (255, 255, 0))  # Yellow outline
            pygame.draw.circle(self.game.screen, (255, 255, 0), (x, y), 14 ,5)


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

        self.line5_end_turn = False
        self.verify_5line()

            