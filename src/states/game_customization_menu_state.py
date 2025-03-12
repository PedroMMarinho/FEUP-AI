import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BUTTONS_HEIGHT, BUTTONS_WIDTH, BLACK, WHITE, BUTTON_FONT_SIZE, GREEN, RED, YELLOW
from states.state import State
from ui import draw_button, draw_text
from mode import GameMode
from board import Board
from button import Button, PieceButton


class GameCustomizationMenu(State):

    def __init__(self, game, gameMode=None):
        super().__init__(game)
        self.start_game = None
        self.back_button = None
        self.gameMode = gameMode
        self.board = Board()
        self.difficulty_buttons = [
            Button("Easy", self.game.screen, BUTTONS_WIDTH,BUTTONS_HEIGHT,pygame.font.SysFont(None,BUTTON_FONT_SIZE),GREEN,BLACK), 
            Button("Medium", self.game.screen, BUTTONS_WIDTH,BUTTONS_HEIGHT,pygame.font.SysFont(None,BUTTON_FONT_SIZE),YELLOW,BLACK),
            Button("Hard", self.game.screen, BUTTONS_WIDTH,BUTTONS_HEIGHT,pygame.font.SysFont(None,BUTTON_FONT_SIZE),RED,BLACK),
                                ]
        self.difficulty_buttons_2 = [
            Button("Easy", self.game.screen, BUTTONS_WIDTH,BUTTONS_HEIGHT,pygame.font.SysFont(None,BUTTON_FONT_SIZE),GREEN,BLACK), 
            Button("Medium", self.game.screen, BUTTONS_WIDTH,BUTTONS_HEIGHT,pygame.font.SysFont(None,BUTTON_FONT_SIZE),YELLOW,BLACK),
            Button("Hard", self.game.screen, BUTTONS_WIDTH,BUTTONS_HEIGHT,pygame.font.SysFont(None,BUTTON_FONT_SIZE),RED,BLACK),
        ]
        self.bot_difficulty = None
        self.bot_difficulty_2 = None
        self.piece_button = PieceButton(self.game.screen, BUTTONS_WIDTH, BUTTONS_HEIGHT, pygame.font.SysFont(None, BUTTON_FONT_SIZE), BLACK, WHITE)
        self.customize_initial_board_button = None
        self.difficulty_button_2 = None  # For AI vs AI mode

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.start_game.collidepoint(x, y) and self.gameMode == GameMode.PLAYER_VS_PLAYER:
                self.game.change_state("game", self.gameMode, self.board)
            elif self.back_button.collidepoint(x, y):
                self.game.change_state("options")
            elif self.customize_initial_board_button.collidepoint(x, y):
                self.game.change_state("initial_board_customization") # TODO
            elif self.start_game.collidepoint(x,y) and self.gameMode == GameMode.PLAYER_VS_AI and self.bot_difficulty is not None:
                self.game.change_state("game", self.gameMode, self.board, self.piece_button.state , self.bot_difficulty)
            elif self.gameMode == GameMode.PLAYER_VS_AI:
                if self.piece_button.collidepoint(x, y):
                    self.piece_button.toggle()
                for button in self.difficulty_buttons:
                    if button.collidepoint(x, y):
                        self.bot_difficulty = button.text
                        button.isSelected = True
                        for other_button in self.difficulty_buttons:
                            if other_button.text != button.text:
                                other_button.isSelected = False
            elif self.start_game.collidepoint(x,y) and self.gameMode == GameMode.AI_VS_AI and self.bot_difficulty is not None and self.bot_difficulty_2 is not None:
                self.game.change_state("game", self.gameMode, self.board, self.piece_button.state ,self.bot_difficulty, self.bot_difficulty_2)
            elif self.gameMode == GameMode.AI_VS_AI:
                for button in self.difficulty_buttons:
                    if button.collidepoint(x, y):
                        self.bot_difficulty = button.text
                        button.isSelected = True
                        for other_button in self.difficulty_buttons:
                            if other_button.text != button.text:
                                other_button.isSelected = False
                for button in self.difficulty_buttons_2:
                    if button.collidepoint(x, y):
                        self.bot_difficulty_2 = button.text
                        button.isSelected = True
                        for other_button in self.difficulty_buttons_2:
                            if other_button.text != button.text:
                                other_button.isSelected = False

    def draw(self):
        screen = self.game.screen
        font = pygame.font.SysFont(None, 50)
        small_font = pygame.font.SysFont(None, 30)

        # Draw the title of the screen
        draw_text(screen, "Game Customization", font, BLACK, SCREEN_WIDTH // 2 - font.size("Game Customization")[0] // 2, 60)

        match self.gameMode:
            case GameMode.PLAYER_VS_PLAYER:
                # Draw for player vs player mode
                self.start_game = draw_button(screen, "Start Game", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 3 + 50, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
                self.back_button = draw_button(screen, "Go Back", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTONS_HEIGHT + 50 , BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
                self.customize_initial_board_button = draw_button(screen, "Customize Initial Board", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 3 + 150, BUTTONS_WIDTH, BUTTONS_HEIGHT, small_font, BLACK, WHITE)
            
            case GameMode.PLAYER_VS_AI:
                # Draw for player vs AI mode
                font = pygame.font.SysFont(None, 50)
                y_offset = 160
                draw_text(screen, "Select Bot Difficulty", font, BLACK, SCREEN_WIDTH // 2 - font.size("Select Bot Difficulty")[0] // 2,  y_offset)
                y_offset += 20 + BUTTONS_HEIGHT
                x_offset = SCREEN_WIDTH // 9 - 2

                for button in self.difficulty_buttons:
                    button.draw(x_offset, y_offset)
                    x_offset += BUTTONS_WIDTH + 20

                y_offset += 100
                draw_text(screen, "Select Your Pieces", font, BLACK, SCREEN_WIDTH // 2 - font.size("Select Your Pieces")[0] // 2, y_offset)
                y_offset += 20 + BUTTONS_HEIGHT

                self.piece_button.draw(SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset)
                y_offset += 100
                self.customize_initial_board_button = draw_button(screen, "Customize Initial Board", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, small_font, BLACK, WHITE)
                y_offset += 100
                self.start_game = draw_button(screen, "Start Game", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
                y_offset += 100
                self.back_button = draw_button(screen, "Go Back", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)

            case GameMode.AI_VS_AI:
                font = pygame.font.SysFont(None, 50)
                y_offset = 160
                draw_text(screen, "Select Bot1 Difficulty", font, BLACK, SCREEN_WIDTH // 2 - font.size("Select Bot Difficulty")[0] // 2,  y_offset)
                y_offset += 20 + BUTTONS_HEIGHT
                x_offset = SCREEN_WIDTH // 9 - 2

                for button in self.difficulty_buttons:
                    button.draw(x_offset, y_offset)
                    x_offset += BUTTONS_WIDTH + 20

                y_offset += 100
                draw_text(screen, "Select Bot2 Difficulty", font, BLACK, SCREEN_WIDTH // 2 - font.size("Select Bot Difficulty")[0] // 2,  y_offset)
                y_offset += 20 + BUTTONS_HEIGHT

                x_offset = SCREEN_WIDTH // 9 - 2
                for button in self.difficulty_buttons_2:
                    button.draw(x_offset, y_offset)
                    x_offset += BUTTONS_WIDTH + 20
                y_offset += 100

                self.start_game = draw_button(screen, "Start Game", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
                y_offset += 100

                self.customize_initial_board_button = draw_button(screen, "Customize Initial Board", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, small_font, BLACK, WHITE)
                y_offset += 100

                self.back_button = draw_button(screen, "Go Back", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
