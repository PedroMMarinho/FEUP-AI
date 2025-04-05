import pygame
import math
from board import BoardPhase
from mode import GameMode
import copy
from ai_algorithms import MonteCarlo, MiniMax
import time

class GameState:
    """
    GameState class represents the state of the game, encapsulating all the necessary information
    to manage the game's logic, including player actions, AI behavior, and game rules.
    """

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
        self.hint_move = None
        #AI needs 
        self.bot1_mode = bot1_mode
        self.bot1_difficulty = bot1_difficulty
        self.bot2_mode = bot2_mode
        self.bot2_difficulty = bot2_difficulty
        self.player_moves = [] # list of all moves done in the game
        self.turn_time = pygame.time.get_ticks()
        self.ai_time = 0
        self.init_game = True



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
            "init_game": self.init_game,
            "player_moves" : self.player_moves
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
        state.valid_moves = list(map(tuple,data["valid_moves"]))
        state.game_over = data["game_over"]
        state.winner = data["winner"]
        state.line5 = line5
        state.active_connect5 = data["active_connect5"]
        state.line5_end_turn = data["line5_end_turn"]
        state.init_game = data["init_game"]
        state.player_moves = data["player_moves"]
        return state


    # Handles AI Play
    def handle_ai(self, stop_flag=lambda: False):
        """Executes the AI's turn based on the game mode and bot configurations.""" 
        if self.game_over or stop_flag():
            return None
        if self.init_game:
            self.init_game = False
            self.line5_end_turn = False
            self.verify_5line()
            if self.active_connect5:
                self.valid_moves= []
        simulated_state = copy.deepcopy(self)
        if self.game_mode == GameMode.PLAYER_VS_AI or (self.game_mode == GameMode.AI_VS_AI and self.player == 1):
            if self.bot1_mode == "MiniMax":
                move, move_2,timeTaken = MiniMax.best_move(simulated_state,self.bot1_difficulty,stop_flag=stop_flag)
                self.ai_time = timeTaken

                if not stop_flag():
                    if self.active_connect5:
                        self.handle_action(seq=move)
                    else:
                        self.handle_action(pos=move)

                    if move_2:
                        start = time.time()
                        while time.time() - start < 1:
                            continue
                        self.handle_action(pos=move_2)
            else:
                self = MonteCarlo.monte_carlo(simulated_state,self.bot1_difficulty,stop_flag=stop_flag)
                if not stop_flag():
                    self.player_moves[-1] = (self.player_moves[-1][0],self.player_moves[-1][1],self.bot1_difficulty)
        elif self.game_mode == GameMode.AI_VS_AI:
            if self.bot2_mode == "MiniMax":
                move, move_2,timeTaken = MiniMax.best_move(simulated_state,self.bot2_difficulty,stop_flag=stop_flag)
                self.ai_time = timeTaken
                if not stop_flag():
                    if self.active_connect5:
                        self.handle_action(seq=move)
                    else:
                        self.handle_action(pos=move)

                    if move_2:
                        start = time.time()
                        while time.time() - start < 1:
                            continue
                        self.handle_action(pos=move_2)
            else:
                self = MonteCarlo.monte_carlo(simulated_state,self.bot2_difficulty,stop_flag=stop_flag)
                if not stop_flag():
                    self.player_moves[-1] = (self.player_moves[-1][0],self.player_moves[-1][1],self.bot1_difficulty)
                

        return self
    

    # Handles Player Play
    def handle_events(self,event):
        """Handles various game events such as mouse clicks and mouse movements."""
        self.valid_ring_moves = []
        if self.init_game:
            self.init_game = False
            self.line5_end_turn = False
            self.verify_5line()
            if self.active_connect5:
                self.valid_moves= []

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.hint_move = None
                if self.active_connect5:
                    if self.valid_connect5 != []:   
                        self.handle_action(seq=self.valid_connect5)
                else:
                    self.handle_action(pos=event.pos)
               
            if event.button == 3 and self.active_connect5: # Select markers to remove (change direction)
                if self.selected_sequence != None and len(self.possible_sequences) > 1:
                    sequence_index = self.possible_sequences.index(self.selected_sequence)
                    next_index = (sequence_index + 1) % len(self.possible_sequences)
                    self.selected_sequence = self.possible_sequences[next_index]
                    point_index = self.selected_sequence.index(self.last_hovered_point)


                    if len(self.selected_sequence) <= 5:
                        self.valid_connect5 = self.selected_sequence  # Return all if 4 or fewer exist
                    else:
                        # Try to center around hovered point
                        start_index = max(0, min(point_index - 1, len(self.selected_sequence) - 5))
                        self.valid_connect5 = self.selected_sequence[start_index:start_index + 5]

                        if len(self.selected_sequence) % 2 == 1 and sequence_index == len(self.selected_sequence) // 2:
                            self.possible_sequences.append(self.selected_sequence[sequence_index:])

                    
        if event.type == pygame.MOUSEMOTION and self.board.phase == BoardPhase.GAME:
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
                        for sequence in sequences:
                            for (x,y) in sequence:
                                if self.is_within_hitbox(mouse_x, mouse_y, x, y):
                                    hovered_point = (x,y)
                                    possible_sequences.append(sequence)
                                    if self.selected_sequence == None or hovered_point != self.last_hovered_point:
                                        selected_sequence = sequence
                                    self.last_hovered_point = hovered_point
                                    break  
                            if hovered_point:
                                break
                    if len(possible_sequences) != 0:
                        self.possible_sequences = possible_sequences
                        self.selected_sequence = selected_sequence
                        enter = True
                    if self.selected_sequence != None and enter:
                        index = self.selected_sequence.index(hovered_point)
        
                        # Select 5 consecutive points
                        if len(self.selected_sequence) <= 5:
                            self.valid_connect5 = self.selected_sequence 
                        else:
                            # Try to center around hovered point
                            start_index = max(0, min(index - 1, len(self.selected_sequence) - 5)) 
                            self.valid_connect5 = self.selected_sequence[start_index:start_index + 5] 

                            if len(self.selected_sequence) % 2 == 1 and index == len(self.selected_sequence) // 2:
                                self.possible_sequences.append(self.selected_sequence[index:])


    # Starting point game logic - validation and next valid moves
    def handle_action(self, pos=None, seq=None, simul=False):
        """Handles a player's action during the game."""
        if len(self.valid_moves) == 0 :
            if self.active_connect5:
                self.board.remove_markers(seq)
                self.board.remove_ring_phase = True
                self.active_connect5 = False
                self.valid_connect5 = []
                newLine = []
                for i in range(len(seq)):
                    newLine.append(self.board.vertices[seq[i]]) 
                self.add_move_to_list("remove_line", newLine)
                self.turn_time = pygame.time.get_ticks()
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
        """Handles a player's move in the game based on the current phase and state of the board."""
        if self.board.phase == BoardPhase.PREP:
            self.board.perform_move((x,y), (0,0), self.player)
            self.add_move_to_list("place_ring",self.board.vertices[(x,y)])
            self.change_player()
            self.turn_time = pygame.time.get_ticks()

        elif self.board.phase == BoardPhase.GAME:
            if not self.board.marker_placed and not self.board.remove_ring_phase:        
                self.board.perform_move((x,y), (0,0), self.player)
                self.board.marker_placed = True
                self.board.num_markers -= 1
                self.board.ring_pos = (x,y)
                self.add_move_to_list("place_marker",self.board.vertices[(x,y)])
                self.turn_time = pygame.time.get_ticks()
            elif not self.active_connect5 and not self.board.remove_ring_phase:
                self.board.perform_move(self.board.ring_pos, (x,y), self.player)
                self.line5_end_turn = True
                self.verify_5line()
                self.add_move_to_list("move_ring",self.board.vertices[(x,y)])
                self.turn_time = pygame.time.get_ticks()
                if not self.active_connect5:
                    if self.board.num_markers <= 0:
                        if self.board.num_rings1 == self.board.num_rings2: 
                            self.winner = 0
                        else:
                            self.winner = 1 if self.board.num_rings1 < self.board.num_rings2 else 2
                        self.game_over = True
                    self.board.marker_placed = False
                    self.board.ring_pos = None
                    self.change_player()
            elif self.board.remove_ring_phase:
                self.board.remove_ring((x,y))
                self.board.remove_ring_phase = False
                self.board.marker_placed = False
                self.board.ring_pos = None
                self.add_move_to_list("remove_ring",self.board.vertices[(x,y)])
                self.turn_time = pygame.time.get_ticks()
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


    def add_move_to_list(self, type, move):
        if self.is_ai_turn():
            time = self.ai_time
        else: 
            time = (pygame.time.get_ticks() - self.turn_time ) / 1000 
        self.player_moves.append((type,move,time,self.player))



    # Utility funcitons

    # Check if mouse pos is within hitbox
    def is_within_hitbox(self, mouse_x, mouse_y, piece_x, piece_y):
        """
        Determines whether a given point (mouse_x, mouse_y) is within the hitbox
        of a piece located at (piece_x, piece_y).
        The hitbox is defined as a circular area with a radius of 12 units.
        """

        distance = math.sqrt((mouse_x - piece_x) ** 2 + (mouse_y - piece_y) ** 2)
        return distance <= 12

    # Verify if 5 markers in line
    def verify_5line(self):
        """
        Verifies if there is a line of 5 consecutive pieces for the current player on the board.
        This method checks the board to determine if the current player has achieved a line
        of exactly 5 consecutive pieces. If such a line exists, it updates the `line5` attribute
        with the positions of the pieces in the line and sets the `active_connect5` attribute
        to True. Otherwise, `active_connect5` is set to False.
        """

        self.line5 = self.board.check_x_in_line(5,self.player)
        self.active_connect5 = len(self.line5) > 0               

    # Changes player turn
    def change_player(self):
        """
        Switches the current player to the other player and resets the end-of-turn state.
        This method toggles the `player` attribute between player 1 and player 2.
        It also resets the `line5_end_turn` attribute to `False` and calls the 
        `verify_5line` method to perform any necessary checks related to the game state.
        """

        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

        self.line5_end_turn = False
        self.verify_5line()

    # Checks if is game over state 
    def check_game_over(self):
        """
        Checks if the game is over based on the current board state and game type.
        """

        if self.board.phase == BoardPhase.GAME and (self.game_type == "Blitz" and self.board.num_rings1 == 4 or self.game_type == "Normal" and self.board.num_rings1 == 2 ):
            return True
        if self.board.phase == BoardPhase.GAME and (self.game_type == "Blitz" and self.board.num_rings2 == 4 or self.game_type == "Normal" and self.board.num_rings2 == 2 ):
            return True
        if self.board.num_markers <= 0 and not self.active_connect5: 
            return True
        return False
    

    # Checks if is ai turn
    def is_ai_turn(self):
        """
        Determines if it is the AI's turn to play.
        """

        return (self.game_mode == GameMode.PLAYER_VS_AI and ((self.player == 1 and self.player_pieces == "Black") or (self.player == 2 and self.player_pieces == "White"))) or self.game_mode == GameMode.AI_VS_AI

    # AI - When n in line creates a list with valid selections
    def create_possible_choices(self, dic, n):
        """
        Generates all possible groups of length `n` from the sequences in the given dictionary.
        """
        possible_choices = []
        for sequences in dic.values():
            for sequence in sequences:
                for i in range(len(sequence) - (n-1)):  
                    group = sequence[i:i + n] 
                    possible_choices.append(group)        
        return possible_choices

    # AI - Valid moves
    def legal_moves(self):
        """
        Determines the legal moves available in the current game state for the AI.
        """

        if self.active_connect5:
            return self.create_possible_choices(self.line5, 5)
        else:
            return self.valid_moves

    # AI(MonteCarlo) - Used in simulation phase of montecarlo, checks if player wins or lose the game 
    def get_result(self):
        """
        Determines the result of the game based on the current state.
        """
        
        if self.board.phase == BoardPhase.GAME and self.player == 1 and (self.game_type == "Blitz" and self.board.num_rings1 == 4 or self.game_type == "Normal" and self.board.num_rings1 == 2) :
            return 1
        elif self.board.phase == BoardPhase.GAME and self.player == 2 and (self.game_type == "Blitz" and self.board.num_rings2 == 4 or self.game_type == "Normal" and self.board.num_rings2 == 2) :
            return 1
        return 0
    

    # AI(Minimax) - Heuristics

    def evaluate(self):
        """
        Evaluates the current game state by calculating a score based on various factors.
        """
        return self.x_in_line() + self.can_win(self.player) + self.n_rings(self.player)
    
    def x_in_line(self):
        """
        Calculates the score difference between the current player and the opponent
        based on the number of consecutive pieces in a line.
        The scoring system assigns weights to the number of consecutive pieces:
        - 1 point for a single piece in a line.
        - 3 points for two consecutive pieces in a line.
        - 9 points for three consecutive pieces in a line.
        - 27 points for four consecutive pieces in a line.
        - 81 points for five or more consecutive pieces in a line.
        """
        opponent = 1 if (self.player == 2) else 2
        score_current_player = 1*self.inline_equals_n(1, self.player) + 3*self.inline_equals_n(2, self.player) + 9*self.inline_equals_n(3, self.player) + 27*self.inline_equals_n(4, self.player) + 81*self.inline_five_or_more(self.player)
        score_opponent = 1*self.inline_equals_n(1, opponent) + 3*self.inline_equals_n(2, opponent) + 9*self.inline_equals_n(3, opponent) + 27*self.inline_equals_n(4, opponent) + 81*self.inline_five_or_more(opponent)
        return score_current_player - score_opponent


    def inline_equals_n(self, n, player ):
        """
        Calculates the number of lines of length `n` occupied by the specified player.
        """
        
        score = 0
        dic = self.board.check_x_in_line(n,player)
        for key, value_list in dic.items():
            for line in value_list:
                score += len(line) == n
        return score
    
    def inline_five_or_more(self, player):
        """
        Calculates the number of inline sequences of five or more pieces on the board.
        """

        score = 0
        dic = self.board.check_x_in_line(5,player)
        for key, valueList in dic.items():
            for line in valueList:
                score += len(line) - 4

        return score
    
    def can_win(self, player):
        """
        Determines if the specified player can win the game.
        """

        player_rings = self.board.num_rings1 if player == 1 else self.board.num_rings2
        return 10000*(self.inline_five_or_more(player) > 0 and player_rings == 3)
    
    
    
    
    def next_to_previous_move(self,move): 
        """
        Determines if the given move is adjacent to the previous move made by the player.
        """

        if len(self.player_moves) == 0: 
            return False 
        (boardX,boardY) = move
        (X,Y) = self.player_moves[-1][1]
        
        vectors = [(0,2),(0,-2),(1,1),(-1,-1),(1,-1),(-1,1)]
        for v in vectors:
            (vX,vY) = v
            altPos = (X + vX,Y + vY)
            if altPos == (boardX, boardY):
                return True
        return False
        
    def distance_from_center(self,move): 
        """
        Calculate the squared distance of a given move from the center point.
        """

        (centerX,centerY) = (5,9)
        (X,Y) = move
        return (X - centerX)**2 + (Y - centerY)**2
    
    def eval_prep_move_ai(self,move): 
        """
        Evaluates the preparation move for the AI player based on the current game state.
        """

        boardMove = self.board.vertices[move]
        if len(self.player_moves) == 0 and self.on_edge(boardMove) :
            return 10000

        if self.count_moves_on_edge(self.player) > 1: 
            val = -(self.distance_from_center(boardMove))
            return val
        if self.on_edge(boardMove) and self.next_to_previous_move(boardMove):
            return 10000
        return -(self.distance_from_center(boardMove))
        
    def on_edge(self, move):
        """
        Determines if a given move is on the edge of the board.
        """

        vectors = [(0,2),(0,-2),(1,1),(-1,-1),(1,-1),(-1,1)]
        (moveX, moveY) = move
        for v in vectors:
            (vX, vY ) = v
            if moveX + vX > len(self.board.matrix[0]) -1 or moveX + vX < 0 or moveY + vY > len(self.board.matrix) - 1 or moveY + vY < 0:
                return True 
            
            if self.board.matrix[moveY + vY][moveX + vX] == -1:
                return True
        return False    
    
    def count_moves_on_edge(self,player): 
        """
        Counts the number of moves made by the specified player that are on the edge of the game board.
        """

        moves = [ self.player_moves[i][1] for i in range(0, len(self.player_moves)) if (i + player - 1) % 2 == 0 ]

        counter = 0
        for m in moves: 
            if self.on_edge(m): 
                counter+=1
        return counter 
    
    def n_rings(self,player): 
        """
        Calculates the heuristic value based on the number of rings for the given player
        and their opponent.
        The heuristic is computed as the difference between the opponent's rings and
        the player's rings, each weighted by a factor of 100.
        """

        if player == 1: 
            player_rings = self.board.num_rings1
            opponent_rings = self.board.num_rings2
        else: 
            player_rings = self.board.num_rings2
            opponent_rings = self.board.num_rings1
        return (opponent_rings*100) - (player_rings*100)
    
                




