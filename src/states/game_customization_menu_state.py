import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BUTTONS_HEIGHT, BUTTONS_WIDTH, BLACK, WHITE
from states.state import State
from ui import draw_button, draw_text
from mode import GameMode
from board import Board

class GameCustomizationMenu(State):

    def __init__(self, game, gameMode=None):
        super().__init__(game)
        self.start_game = None
        self.back_button = None
        self.gameMode = gameMode
        self.board = Board()
        self.difficulty_button = None
        self.piece_button = None
        self.customize_initial_board_button = None
        self.difficulty_button_2 = None  # For AI vs AI mode

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.start_game.collidepoint(x, y):
                self.game.change_state("game", self.gameMode, self.board)
            elif self.back_button.collidepoint(x, y):
                self.game.change_state("options")
            elif self.difficulty_button and self.difficulty_button.collidepoint(x, y):
                # TODO
                pass
            elif self.piece_button and self.piece_button.collidepoint(x, y):
                # TODO
                pass
            elif self.customize_initial_board_button and self.customize_initial_board_button.collidepoint(x, y):
                # TODO
                pass

    def draw(self):
        screen = self.game.screen
        font = pygame.font.SysFont(None, 50)
        small_font = pygame.font.SysFont(None, 30)

        # Draw the title of the screen
        draw_text(screen, "Game Customization", font, BLACK, SCREEN_WIDTH // 2 - font.size("Game Customization")[0] // 2, 100)

        match self.gameMode:
            case GameMode.PLAYER_VS_PLAYER:
                # Draw for player vs player mode
                self.start_game = draw_button(screen, "Start Game", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
                self.back_button = draw_button(screen, "Go Back", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT - BUTTONS_HEIGHT - 30, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
                # Optionally, add a customize initial board button
                self.customize_initial_board_button = draw_button(screen, "Customize Initial Board", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 + 150, BUTTONS_WIDTH, BUTTONS_HEIGHT, small_font, BLACK, WHITE)
            
            case GameMode.PLAYER_VS_AI:
                # Draw for player vs AI mode
                self.difficulty_button = draw_button(screen, "Select Difficulty", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - 40, BUTTONS_WIDTH, BUTTONS_HEIGHT, small_font, BLACK, WHITE)
                self.piece_button = draw_button(screen, "Select Piece (White/Black)", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTONS_HEIGHT // 2 + 20, BUTTONS_WIDTH, BUTTONS_HEIGHT, small_font, BLACK, WHITE)
                self.start_game = draw_button(screen, "Start Game", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
                self.back_button = draw_button(screen, "Go Back", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT - BUTTONS_HEIGHT - 30, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
                self.customize_initial_board_button = draw_button(screen, "Customize Initial Board", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, BUTTONS_WIDTH, BUTTONS_HEIGHT, small_font, BLACK, WHITE)

            case GameMode.AI_VS_AI:
                # Draw for AI vs AI mode
                self.difficulty_button = draw_button(screen, "Select AI 1 Difficulty", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - 40, BUTTONS_WIDTH, BUTTONS_HEIGHT, small_font, BLACK, WHITE)
                self.difficulty_button_2 = draw_button(screen, "Select AI 2 Difficulty", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTONS_HEIGHT // 2 + 20, BUTTONS_WIDTH, BUTTONS_HEIGHT, small_font, BLACK, WHITE)
                self.start_game = draw_button(screen, "Start Game", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
                self.back_button = draw_button(screen, "Go Back", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT - BUTTONS_HEIGHT - 30, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
                self.customize_initial_board_button = draw_button(screen, "Customize Initial Board", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 + 250, BUTTONS_WIDTH, BUTTONS_HEIGHT, small_font, BLACK, WHITE)
