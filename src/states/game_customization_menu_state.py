import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BUTTONS_HEIGHT, BUTTONS_WIDTH, BUTTON_FONT_SIZE, FONT
from config import LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, CADET_BLUE, WHITE, BLACK, GREEN, RED, YELLOW
from states.state import State
from ui import draw_button, draw_text
from mode import GameMode
from board import Board
from button import Button, PieceButton, ClickButton


class GameCustomizationMenu(State):

    def __init__(self, game, gameMode=None):
        super().__init__(game)
        self.start_game = None
        self.back_button = None
        self.gameMode = gameMode
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
        self.bot1_mode = "MinMax"
        self.bot2_mode = "MinMax"
        self.bot_difficulty = 2
        self.bot_difficulty_2 = 2
        self.piece_button = PieceButton(self.game.screen, BUTTONS_WIDTH, BUTTONS_HEIGHT, pygame.font.SysFont(None, BUTTON_FONT_SIZE), WHITE, BLACK)
        self.customize_initial_board_button = None
        self.difficulty_button_2 = None  # For AI vs AI mode
        self.buttons = []

        self.initialize_buttons()


    def initialize_buttons(self):
        match self.gameMode:
            case GameMode.PLAYER_VS_PLAYER:
                self.buttons.extend([
                    ClickButton("Start Game", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 3 + 50,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.change_state("game", self.gameMode)),
                    ClickButton("Custom Init Board", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 3 + 150,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.change_state("initial_board_customization")),
                    ClickButton("Go Back", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTONS_HEIGHT + 50,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.go_back())
                ])
            
            case GameMode.PLAYER_VS_AI:
                self.buttons.extend([
                    ClickButton("MinMax", 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - 2 * BUTTONS_HEIGHT,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.change_ai_mode(1,"MinMax")),
                    ClickButton("MonteCarlo", 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - 2 * BUTTONS_HEIGHT,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.change_ai_mode(1,"MonteCarlo")),
                    ClickButton("Start Game", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, 400 + 2 * BUTTONS_HEIGHT,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.change_state("game", self.gameMode, self.piece_button.state , self.bot_difficulty)),
                    ClickButton("Custom Init Board", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, 500 + 2 * BUTTONS_HEIGHT,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.change_state("initial_board_customization")),
                    ClickButton("Go Back", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, 600 + 2 * BUTTONS_HEIGHT,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.go_back())
                ])      

    def change_ai_mode(self, ai, mode):
        if ai == 1:
            self.bot1_mode = mode
        else:
            self.bot2_mode = mode

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.gameMode == GameMode.PLAYER_VS_PLAYER:
                for button in self.buttons:
                    button.click(event)

            elif self.gameMode == GameMode.PLAYER_VS_AI:
                for button in self.buttons:
                    if button.text == "Start Game" and self.bot_difficultyis is None:
                        return # Difficulty not selected 
                    button.click(event)


            x, y = event.pos
            if self.gameMode == GameMode.PLAYER_VS_AI:
                if self.piece_button.collidepoint(x, y):
                    self.piece_button.toggle()
                    '''
                for button in self.difficulty_buttons:
                    if button.collidepoint(x, y):
                        self.bot_difficulty = button.text
                        button.isSelected = True
                        for other_button in self.difficulty_buttons:
                            if other_button.text != button.text:
                                other_button.isSelected = False
                    '''
            elif self.gameMode == GameMode.AI_VS_AI and self.bot_difficulty is not None and self.bot_difficulty_2 is not None:
                self.game.change_state("game", self.gameMode, self.piece_button.state ,self.bot_difficulty, self.bot_difficulty_2)
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
        for button in self.buttons:
            button.draw(screen)
        match self.gameMode:
            case GameMode.PLAYER_VS_AI:
                # Draw for player vs AI mode
                font = pygame.font.SysFont(None, 50)
                y_offset = 160
                #draw_text(screen, "Select Bot Difficulty", font, BLACK, SCREEN_WIDTH // 2 - font.size("Select Bot Difficulty")[0] // 2,  y_offset)
                y_offset += 20 + BUTTONS_HEIGHT
                x_offset = SCREEN_WIDTH // 9 - 2

                #for button in self.difficulty_buttons:
                 #   button.draw(x_offset, y_offset)
                 #   x_offset += BUTTONS_WIDTH + 20

                y_offset += 100
                draw_text(screen, "Select Your Pieces", font, BLACK, SCREEN_WIDTH // 2 - font.size("Select Your Pieces")[0] // 2, y_offset)
                y_offset += 20 + BUTTONS_HEIGHT

                self.piece_button.draw(SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset)
                y_offset += 100

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

                #self.start_game = draw_button(screen, "Start Game", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
                y_offset += 100

                #self.customize_initial_board_button = draw_button(screen, "Customize Initial Board", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, small_font, BLACK, WHITE)
                y_offset += 100

                #self.back_button = draw_button(screen, "Back", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, y_offset, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
