import pygame
import math
from states.state import State
from board import BoardPhase
from mode import GameMode
import copy
from ai_algorithms import MonteCarlo, MinMax
import ast

class GameState(State):

    def __init__(self, mode, board, player="White", bot1_mode=None, bot1_difficulty=None, bot2_mode=None, bot2_difficulty=None):
        #General
        self.game_mode = mode
        self.game_type = "Normal"
        self.board = board
        self.player = 1
        self.valid_moves = self.board.valid_moves(self.player)
        self.game_over = False
        self.winner = None
        #Mode Player_AI
        self.player_pieces = player
        # Player needs
        self.valid_ring_moves = []
        self.line5 = {}
        self.active_connect5 = False
        self.valid_connect5 = []
        self.selected_sequence = None
        self.possible_sequences = []  
        self.last_hovered_point = (-1,-1)
        self.line5_end_turn = False
        #AI needs 
        self.bot1_mode = bot1_mode
        self.bot1_difficulty = bot1_difficulty
        self.bot2_mode = bot2_mode
        self.bot2_difficulty = bot2_difficulty
        self.ai_has_moved = False

    def __str__(self):
        return (f"GameState(\n"
                f"  Game Mode: {self.game_mode},\n"
                f"  Game Type: {self.game_type},\n"
                f"  Player: {self.player},\n"
                f"  PlayerPieces: {self.player_pieces},\n"
                f"  Active Connect5: {self.active_connect5},\n"
                f"  Valid Moves: {len(self.valid_moves)},\n"
                f"  Bot1 Mode: {self.bot1_mode}, Difficulty: {self.bot1_difficulty},\n"
                f"  Bot2 Mode: {self.bot2_mode}, Difficulty: {self.bot2_difficulty},\n"
                f"  AI Has Moved: {self.ai_has_moved}\n"
                f")")


    def to_dict(self):
        line5_dict = {str(key): value for key, value in self.line5.items()}

        return {
            "game_mode": self.game_mode.value,
            "game_type": self.game_type,
            "board": self.board.to_dict(),  
            "player": self.player,
            "valid_moves": self.valid_moves, 
            "game_over": self.game_over,
            "winner": self.winner,
            "player_pieces": self.player_pieces,

            "line5": line5_dict,
            "active_connect5": self.active_connect5,
            "line5_end_turn": self.line5_end_turn,
            "bot1_mode": self.bot1_mode,
            "bot1_difficulty": self.bot1_difficulty,
            "bot2_mode": self.bot2_mode,
            "bot2_difficulty": self.bot2_difficulty,
            "ai_has_moved": self.ai_has_moved
        }

    @classmethod
    def from_dict(cls, data, board_class):
        board = board_class.from_dict(data["board"]) 
        line5 = {
            # For each key-value pair, process the key and values
            tuple(
                tuple(map(int, key.replace("(", "").replace(")", "").split(", ")[i:i+2])) 
                for i in range(0, len(key.replace("(", "").replace(")", "").split(", ")), 2)
            ): [
                [tuple(coord) for coord in group]  # Convert inner lists into tuples
                for group in value
            ]
            for key, value in data["line5"].items()
        }

        print(f"LINE%: {line5}")

        state = cls(
            mode=GameMode(data["game_mode"]),
            board=board,
            player=data["player_pieces"],
            bot1_mode=data["bot1_mode"],
            bot1_difficulty=data["bot1_difficulty"],
            bot2_mode=data["bot2_mode"],
            bot2_difficulty=data["bot2_difficulty"]
        )
        state.player = data["player"]
        state.valid_moves = data["valid_moves"]
        state.game_over = data["game_over"]
        state.winner = data["winner"]
        state.line5 = line5
        state.active_connect5 = data["active_connect5"]
        state.line5_end_turn = data["line5_end_turn"]
        state.ai_has_moved = data["ai_has_moved"]
        return state


    # Handles AI Play
    def handle_ai(self):
        self.ai_has_moved = True

        if self.game_over:
            self.ai_has_moved = False
            return None

        simulated_state = copy.deepcopy(self)
        if self.game_mode == GameMode.PLAYER_VS_AI or (self.game_mode == GameMode.AI_VS_AI and self.player == 1):
            if self.bot1_mode == "MinMax":
                move = MinMax.best_move(simulated_state,self.bot1_difficulty)
                if self.active_connect5:
                    self.handle_action(seq=move)
                else:
                    self.handle_action(pos=move)
            else:
                self = MonteCarlo.monte_carlo(simulated_state,self.bot1_difficulty)
        elif self.game_mode == GameMode.AI_VS_AI:
            if self.bot2_mode == "MinMax":
                move = MinMax.best_move(simulated_state,self.bot2_difficulty)
                if self.active_connect5:
                    self.handle_action(seq=move)
                else:
                    self.handle_action(pos=move)
            else:
                self = MonteCarlo.monte_carlo(simulated_state,self.bot2_difficulty)

        self.ai_has_moved = False
        return self
    

    # Handles Player Play
    def handle_events(self,event):
        self.valid_ring_moves = []
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.active_connect5:
                    self.handle_action(seq=self.valid_connect5)
                else:
                    self.handle_action(pos=event.pos)
               
            if event.button == 3 and self.active_connect5: # Select markers to remove (change direction)
                #print("RIGHT CLICK")
                #print(f"SELCT SEQ: {self.selected_sequence}")
                if self.selected_sequence != None and len(self.possible_sequences) > 1:
                    #print(f"POSSIBLE SQ {self.possible_sequences}")
                    sequence_index = self.possible_sequences.index(self.selected_sequence)
                    next_index = (sequence_index + 1) % len(self.possible_sequences)
                    self.selected_sequence = self.possible_sequences[next_index]
                    point_index = self.selected_sequence.index(self.last_hovered_point)


                    if len(self.selected_sequence) <= 5: # TODO: Change to 5
                        self.valid_connect5 = self.selected_sequence  # Return all if 4 or fewer exist
                    else:
                        # Try to center around hovered point
                        start_index = max(0, min(point_index - 1, len(self.selected_sequence) - 5)) # TODO: Change to 5
                        self.valid_connect5 = self.selected_sequence[start_index:start_index + 5] # TODO: Change to 5

                        if len(self.selected_sequence) % 2 == 1 and sequence_index == len(self.selected_sequence) // 2:
                            #print(f"Appending case impar -- Idx {sequence_index} | Seq {self.selected_sequence}")
                            self.possible_sequences.append(self.selected_sequence[sequence_index:])

                    
        if event.type == pygame.MOUSEMOTION and self.board.phase == BoardPhase.GAME:
            #print(self.last_hovered_point, self.selected_sequence, self.active_connect5, self.possible_sequences)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not self.board.marker_placed and not self.board.remove_ring_phase: # Show ring moves when hover
                for (valid_x,valid_y) in self.valid_moves:
                    if self.is_within_hitbox(mouse_x, mouse_y, valid_x, valid_y):
                        self.board.ring_pos = (valid_x,valid_y)
                        self.valid_ring_moves = self.board.get_ring_moves()
            
            if self.active_connect5: # Select markers to remove
                (x,y) = self.last_hovered_point
                if self.last_hovered_point == (-1,-1) or not self.is_within_hitbox(mouse_x, mouse_y, x, y):
                    hovered_point = None
                    selected_sequence = None
                    possible_sequences = []
                    enter = False
                    for sequences in self.line5.values():
                        #print(f"SEQ1: {sequences} || MOUSE: {mouse_x,mouse_y}")
                        for sequence in sequences:
                            #print(f"SEQ2: {sequence}")
                            for (x,y) in sequence:
                                if self.is_within_hitbox(mouse_x, mouse_y, x, y):
                                    hovered_point = (x,y)
                                    possible_sequences.append(sequence)
                                    if self.selected_sequence == None or hovered_point != self.last_hovered_point:
                                        selected_sequence = sequence
                                    self.last_hovered_point = hovered_point
                                    #print(f"SEQUECEN : {sequence}")
                                    break  
                            if hovered_point:
                                break
                    if len(possible_sequences) != 0:
                        self.possible_sequences = possible_sequences
                        self.selected_sequence = selected_sequence
                        enter = True
                    #print(self.selected_sequence)
                    if self.selected_sequence != None and enter:
                        index = self.selected_sequence.index(hovered_point)
        
                        # Select 5 consecutive points
                        if len(self.selected_sequence) <= 5: # TODO: Change to 5
                            self.valid_connect5 = self.selected_sequence 
                        else:
                            # Try to center around hovered point
                            start_index = max(0, min(index - 1, len(self.selected_sequence) - 5)) # TODO: Change to 5
                            self.valid_connect5 = self.selected_sequence[start_index:start_index + 5] # TODO: Change to 5

                            if len(self.selected_sequence) % 2 == 1 and index == len(self.selected_sequence) // 2:
                                #print(f"Appending case impar -- Idx {index} | Seq {self.selected_sequence}")
                                self.possible_sequences.append(self.selected_sequence[index:])


    # Starting point game logic - validation and next valid moves
    def handle_action(self, pos=None, seq=None, simul=False):
        if len(self.valid_moves) == 0 and self.active_connect5:
            print("REMOVE MARKERS STATE")
            self.board.remove_markers(seq)
            self.board.remove_ring_phase = True
            self.active_connect5 = False
            self.valid_connect5 = []
        else:
            x,y = pos
            if self.is_ai_turn():
                self.handle_move(x, y, simul=simul)
            else:
                for (valid_x,valid_y) in self.valid_moves:
                    if self.is_within_hitbox(x, y, valid_x, valid_y):
                        self.handle_move(valid_x, valid_y)
                        break
        
        if self.active_connect5:
            self.valid_moves = []
        else:
            self.valid_moves = self.board.valid_moves(self.player)

        return self


    # Game logic - Does actual move
    def handle_move(self,x,y, simul=False):
        if self.board.phase == BoardPhase.PREP:
            self.board.perform_move((x,y), (0,0), self.player)
            self.change_player()
        elif self.board.phase == BoardPhase.GAME:
            if not self.board.marker_placed and not self.board.remove_ring_phase:
                self.board.perform_move((x,y), (0,0), self.player)
                self.board.marker_placed = True
                self.board.num_markers -= 1
                self.board.ring_pos = (x,y)
            elif not self.active_connect5 and not self.board.remove_ring_phase:
                self.board.perform_move(self.board.ring_pos, (x,y), self.player)
                self.line5_end_turn = True
                self.verify_5line()
                if not self.active_connect5:
                    self.board.marker_placed = False
                    self.board.ring_pos = None
                    self.change_player()
            elif self.board.remove_ring_phase:
              #  print("REMOVE RING STATE")
                self.board.remove_ring((x,y))
                self.board.remove_ring_phase = False
                self.board.marker_placed = False
                self.board.ring_pos = None
                if self.player == 1:
                    self.board.num_rings1 -= 1
                    if self.check_game_over() and not simul:
                        self.game_over = True
                        self.winner = 1                            
                else: 
                    self.board.num_rings2 -= 1
                    if self.check_game_over() and not simul:
                        self.game_over = True
                        self.winner = 2
                if self.line5_end_turn:
                    self.change_player()


    # Utility funcitons

    # Check if mouse pos is within hitbox
    def is_within_hitbox(self, mouse_x, mouse_y, piece_x, piece_y):
        distance = math.sqrt((mouse_x - piece_x) ** 2 + (mouse_y - piece_y) ** 2)
        return distance <= 12

    # Verify if 5 markers in line
    def verify_5line(self):
        self.line5 = self.board.check_x_in_line(5,self.player)
        self.active_connect5 = len(self.line5) > 0               

    # Changes player turn
    def change_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

        self.line5_end_turn = False
        self.verify_5line()

    # Checks if is game over state 
    def check_game_over(self):
        if self.board.phase == BoardPhase.GAME and (self.game_type == "Blitz" and self.board.num_rings1 == 4 or self.game_type == "Normal" and self.board.num_rings1 == 2 ):
            return True
        if self.board.phase == BoardPhase.GAME and (self.game_type == "Blitz" and self.board.num_rings2 == 4 or self.game_type == "Normal" and self.board.num_rings2 == 2 ):
            return True
        return False
    

    # Checks if is ai turn
    def is_ai_turn(self):
        return (self.game_mode == GameMode.PLAYER_VS_AI and ((self.player == 1 and self.player_pieces == "Black") or (self.player == 2 and self.player_pieces == "White"))) or self.game_mode == GameMode.AI_VS_AI

    # AI - When n in line creates a list with valid selections
    def create_possible_choices(self, dic, n):
        possible_choices = []
        for sequences in dic.values():
            for sequence in sequences:
                for i in range(len(sequence) - (n-1)):  
                    group = sequence[i:i + n] 
                    possible_choices.append(group)        
        return possible_choices

    # AI - Valid moves
    def legal_moves(self):
        if self.active_connect5:
            return self.create_possible_choices(self.line5, 5)
        else:
            return self.valid_moves

    # AI(MonteCarlo) - Used in simulation phase of montecarlo, checks if player wins or lose the game 
    def get_result(self):
        if self.board.phase == BoardPhase.GAME and self.player == 1 and (self.game_type == "Blitz" and self.board.num_rings1 == 4 or self.game_type == "Normal" and self.board.num_rings1 == 2) :
            return 1
        elif self.board.phase == BoardPhase.GAME and self.player == 2 and (self.game_type == "Blitz" and self.board.num_rings2 == 4 or self.game_type == "Normal" and self.board.num_rings2 == 2) :
            return 1
        return 0
    

    # AI(Minimax) - Heuristics

    def evaluate(self):
        return 0.5*self.inline_2() + self.inline_2() + 1.5*self.inline_3() + 3*self.inline_4()

    # grupos sobresposts??
    def inline_2(self):
        dic = self.board.check_x_in_line(2,self.player)
        list = self.create_possible_choices(dic,2)
        return len(list)

    def inline_3(self):
        dic = self.board.check_x_in_line(3,self.player)
        list = self.create_possible_choices(dic,3)
        return len(list)
    

    def inline_4(self):
        dic = self.board.check_x_in_line(4,self.player)
        list = self.create_possible_choices(dic,4)
        return len(list)
    
    def inline_5(self):
        dic = self.board.check_x_in_line(5,self.player)
        list = self.create_possible_choices(dic,5)
        return len(list)
    
    #valor pos e neg?
    def dif_markers(self):
        return self.board.dif_markers(self.player)
