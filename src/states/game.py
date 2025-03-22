import pygame
import pygame.gfxdraw 
from ui import draw_text
from states.state import State
from states.game_state import GameState
from board import Board
from json_actions import load_boards

class Game(State):

    def __init__(self, game , mode, player="White", bot1_mode=None, bot1_difficulty=None, bot2_mode=None, bot2_difficulty=None):
        #General
        super().__init__(game)
        board_data = load_boards("src/boards.json")
        board = Board(matrix=board_data[game.selected_board]['layout'])
        self.state = GameState(mode, board, player, bot1_mode, bot1_difficulty, bot2_mode, bot2_difficulty)
        

    def handle_events(self, event):
        if self.state.game_over:
            self.game.change_state("game_over", winner=self.state.winner)
        self.state.handle_events(event)


    def draw(self):
        self.state.board.draw(self.game.screen)
        draw_text(self.game.screen, "Next Action",pygame.font.Font(None, 50),(0,0,0),900,30)
        draw_text(self.game.screen, self.state.board.next_action.value,pygame.font.Font(None, 50),(0,0,0),900,100)

        draw_text(self.game.screen, "Player Turn",pygame.font.Font(None, 50),(0,0,0),100,30)
        if self.state.player == 1:
            draw_text(self.game.screen, "White",pygame.font.Font(None, 50),(0,0,0),100,100)
        else:
            draw_text(self.game.screen, "Black",pygame.font.Font(None, 50),(0,0,0),100,100)


        for x, y in self.state.valid_moves:
            pygame.gfxdraw.aacircle(self.game.screen, x, y, 14, (0, 255, 0))  # Green outline
            pygame.draw.circle(self.game.screen, (0, 255, 0), (x, y), 12 ,5)
        for x, y in self.state.valid_ring_moves:
            pygame.gfxdraw.aacircle(self.game.screen, x, y, 14, (255, 255, 0))  # Green outline
            pygame.draw.circle(self.game.screen, (255, 255, 0), (x, y), 12 ,5)
        for x, y in self.state.valid_connect5:
            pygame.gfxdraw.aacircle(self.game.screen, x, y, 16, (255, 255, 0))  # Yellow outline
            pygame.draw.circle(self.game.screen, (255, 255, 0), (x, y), 14 ,5)

            