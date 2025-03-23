import pygame
import pygame.gfxdraw 
from ui import draw_text
from states.state import State
from states.game_state import GameState
from board import Board
from json_actions import load_boards
from config import FONT, BUTTONS_HEIGHT, BUTTONS_WIDTH, LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, SCREEN_HEIGHT, SCREEN_WIDTH
from button import ClickButton

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
        

    def handle_events(self):
        if self.state.is_ai_turn():
            if not self.state.ai_has_moved:
                new_state = self.state.handle_ai()
                if new_state is not None:
                    self.state = new_state
                else:
                    self.game.change_state("game_over", winner=self.state.winner)
        else:
            if self.state.game_over:
                self.game.change_state("game_over", winner=self.state.winner)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        button.click(event)
                self.state.handle_events(event)

    def draw(self):
        #Buttons
        super().draw()
        #Board
        self.state.board.draw(self.game.screen)
    
        draw_text(self.game.screen, "Available Markers", FONT, STEEL_BLUE, SCREEN_WIDTH // 2 - FONT.size("Available Markers")[0] // 2, 35)
        draw_text(self.game.screen, str(self.state.board.num_markers), FONT, STEEL_BLUE, SCREEN_WIDTH // 2 - FONT.size(str(self.state.board.num_markers))[0] // 2, 80)

        draw_text(self.game.screen, "White Rings", FONT, STEEL_BLUE, SCREEN_WIDTH // 6 - FONT.size("White Rings")[0] // 2, 220)
        draw_text(self.game.screen, str(self.state.board.num_rings1), FONT, STEEL_BLUE, SCREEN_WIDTH // 6 - FONT.size(str(self.state.board.num_rings1))[0] // 2, 265)

        draw_text(self.game.screen, "Black Rings", FONT, STEEL_BLUE, 5*SCREEN_WIDTH // 6 - FONT.size("Black Rings")[0] // 2, 220)
        draw_text(self.game.screen, str(self.state.board.num_rings2), FONT, STEEL_BLUE, 5*SCREEN_WIDTH // 6 - FONT.size(str(self.state.board.num_rings2))[0] // 2, 265)

        #Player Turn
        draw_text(self.game.screen, "Player Turn", FONT, STEEL_BLUE, SCREEN_WIDTH // 6 - FONT.size("Player Turn")[0] // 2, 35)
        if self.state.player == 1:
            draw_text(self.game.screen, "White", FONT, STEEL_BLUE, SCREEN_WIDTH // 6 - FONT.size("White")[0] // 2, 80)
        else:
            draw_text(self.game.screen, "Black", FONT, STEEL_BLUE, SCREEN_WIDTH // 6 - FONT.size("Black")[0] // 2, 80)

        #Action
        draw_text(self.game.screen, "Next Action", FONT, STEEL_BLUE, 5*SCREEN_WIDTH // 6 - FONT.size("Next Action")[0] // 2, 35)
        draw_text(self.game.screen, self.state.board.next_action.value, FONT, STEEL_BLUE, 5*SCREEN_WIDTH // 6 - FONT.size(self.state.board.next_action.value)[0] // 2, 80)



        for x, y in self.state.valid_moves:
            pygame.gfxdraw.aacircle(self.game.screen, x, y, 14, (38, 238, 38))  # Green outline
            pygame.draw.circle(self.game.screen, (38, 238, 38), (x, y), 12 ,5)
        for x, y in self.state.valid_ring_moves:
            pygame.gfxdraw.aacircle(self.game.screen, x, y, 14, (255, 128, 0))  # Orange outline
            pygame.draw.circle(self.game.screen, (255, 128, 0), (x, y), 12 ,5)
        for x, y in self.state.valid_connect5:
            pygame.gfxdraw.aacircle(self.game.screen, x, y, 16, (240, 240, 65))  # Yellow outline
            pygame.draw.circle(self.game.screen, (240, 240, 65), (x, y), 14 ,5)

            