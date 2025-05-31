import pygame
import pygame.gfxdraw 
from ui import draw_text
from states.state import State
from states.game_state import GameState
from board import Board
from json_actions import load_boards
from config import SMALL_FONT, FONT, BUTTONS_HEIGHT, BUTTONS_WIDTH, LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, SCREEN_HEIGHT, SCREEN_WIDTH
from button import ClickButton
from ai_algorithms import MiniMax
import copy
import threading
from mode import GameMode

class Game(State):

    def __init__(self, game , mode, player="White", bot1_mode=None, bot1_difficulty=None, bot2_mode=None, bot2_difficulty=None):
        super().__init__(game)
        board_data = load_boards("src/json/boards.json")
        board = Board(matrix=board_data[game.selected_board]['layout'])
        self.state = GameState(mode, board, player, bot1_mode, bot1_difficulty, bot2_mode, bot2_difficulty)
        self.buttons = [
            ClickButton(
                "Back To Menu", 
                SCREEN_WIDTH // 6 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT - BUTTONS_HEIGHT - 35, 
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.change_state("menu")),
            ClickButton(
                "Save and Exit", 
                5*SCREEN_WIDTH // 6 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT - BUTTONS_HEIGHT - 35, 
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.save_exit()),
        ]

        if mode is not GameMode.AI_VS_AI:
            self.buttons.append(
                ClickButton(
                    "Hint", 
                    5*SCREEN_WIDTH // 6 - FONT.size("Next Action")[0] // 2 - BUTTONS_WIDTH/5, 35,
                    BUTTONS_HEIGHT/2, BUTTONS_WIDTH/5,
                    SMALL_FONT,
                    LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                    action=lambda: self.start_ai_thread(hint=True)),
            )

    def handle_events(self):
        if self.state.is_ai_turn():
            self.state.hint_move = None
            if not self.game.ai_thinking:
                self.start_ai_thread()
        elif self.state.game_over:
                self.game.change_state("game_over", winner=self.state.winner,player_moves=self.state.player_moves, p1_rings=self.state.board.num_rings1, p2_rings=self.state.board.num_rings2  )
        for event in pygame.event.get():
            click = False
            if event.type == pygame.QUIT:   
                self.game.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click(event)
                    if button.clicked:
                        click = True
                        button.clicked = False
                        break
            if not click and not self.state.is_ai_turn():
                self.state.handle_events(event)

    def start_ai_thread(self, hint=False):
        self.game.ai_thinking = True
        if hint:
            self.game.ai_thread = threading.Thread(target=self.run_hint_logic, daemon=True)
        else:
            self.game.ai_thread = threading.Thread(target=self.run_ai_logic, daemon=True)
        self.game.ai_thread.start()

    def run_ai_logic(self):
        new_state = self.state.handle_ai(stop_flag=lambda: self.game.stop_ai)
        if self.game.stop_ai:  
            return
        if new_state is not None:
            self.state = new_state
        else:
            self.game.change_state("game_over", winner=self.state.winner,player_moves=self.state.player_moves, p1_rings=self.state.board.num_rings1, p2_rings=self.state.board.num_rings2 )
        self.game.ai_thinking = False 


    def run_hint_logic(self):
        copy_state = copy.deepcopy(self.state)
        self.state.hint_move,_,_ = MiniMax.best_move(copy_state,2,stop_flag=lambda: self.game.stop_ai)
        if self.game.stop_ai:  
            return
        self.game.ai_thinking = False 


    def draw(self):
        #Buttons
        super().draw()
        #Board
        self.state.board.draw(self.game.screen)
    
        draw_text(self.game.screen, "Available Markers", FONT, STEEL_BLUE, SCREEN_WIDTH // 2 - FONT.size("Available Markers")[0] // 2, 35)
        draw_text(self.game.screen, str(self.state.board.num_markers), FONT, STEEL_BLUE, SCREEN_WIDTH // 2 - FONT.size(str(self.state.board.num_markers))[0] // 2, 80)

        draw_text(self.game.screen, "White Rings", FONT, STEEL_BLUE, SCREEN_WIDTH // 6 - FONT.size("White Rings")[0] // 2-40, 220)
        draw_text(self.game.screen, str(self.state.board.num_rings1), FONT, STEEL_BLUE, SCREEN_WIDTH // 6 - FONT.size(str(self.state.board.num_rings1))[0] // 2-40, 265)

        draw_text(self.game.screen, "Black Rings", FONT, STEEL_BLUE, 5*SCREEN_WIDTH // 6 - FONT.size("Black Rings")[0] // 2+40, 220)
        draw_text(self.game.screen, str(self.state.board.num_rings2), FONT, STEEL_BLUE, 5*SCREEN_WIDTH // 6 - FONT.size(str(self.state.board.num_rings2))[0] // 2+40, 265)

        #Player Turn
        draw_text(self.game.screen, "Player Turn", FONT, STEEL_BLUE, SCREEN_WIDTH // 6 - FONT.size("Player Turn")[0] // 2-40, 35)
        if self.state.player == 1:
            draw_text(self.game.screen, "White", FONT, STEEL_BLUE, SCREEN_WIDTH // 6 - FONT.size("White")[0] // 2-40, 80)
        else:
            draw_text(self.game.screen, "Black", FONT, STEEL_BLUE, SCREEN_WIDTH // 6 - FONT.size("Black")[0] // 2-40, 80)

        #Action
        draw_text(self.game.screen, "Next Action", FONT, STEEL_BLUE, 5*SCREEN_WIDTH // 6 - FONT.size("Next Action")[0] // 2+40, 35)
        draw_text(self.game.screen, self.state.board.next_action.value, FONT, STEEL_BLUE, 5*SCREEN_WIDTH // 6 - FONT.size(self.state.board.next_action.value)[0] // 2+40, 80)



        for x, y in self.state.valid_moves:
            pygame.gfxdraw.aacircle(self.game.screen, x, y, 14, (38, 238, 38))  # Green outline
            pygame.draw.circle(self.game.screen, (38, 238, 38), (x, y), 12 ,5)
        for x, y in self.state.valid_ring_moves:
            pygame.gfxdraw.aacircle(self.game.screen, x, y, 14, (255, 128, 0))  # Orange outline
            pygame.draw.circle(self.game.screen, (255, 128, 0), (x, y), 12 ,5)
        for x, y in self.state.valid_connect5:
            pygame.gfxdraw.aacircle(self.game.screen, x, y, 16, (240, 240, 65))  # Yellow outline
            pygame.draw.circle(self.game.screen, (240, 240, 65), (x, y), 14 ,5)

        if self.state.hint_move is not None:
            if self.state.active_connect5:
                for x, y in self.state.hint_move:
                    pygame.gfxdraw.aacircle(self.game.screen, x, y, 16, (233, 52, 52))  # Red outline
                    pygame.draw.circle(self.game.screen, (233, 52, 52), (x, y), 14 ,5)
            else: 
                pygame.gfxdraw.aacircle(self.game.screen, self.state.hint_move[0], self.state.hint_move[1], 14, (233, 52, 52))  # Red outline
                pygame.draw.circle(self.game.screen, (233, 52, 52), self.state.hint_move, 12 ,5)


            