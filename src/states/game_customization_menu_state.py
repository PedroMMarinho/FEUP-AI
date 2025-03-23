import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BUTTONS_HEIGHT, BUTTONS_WIDTH, FONT, FONT_TITLE
from config import LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, CADET_BLUE, WHITE, SELECT_CYAN
from states.state import State
from ui import draw_text
from mode import GameMode
from board import Board
from button import ClickButton


class GameCustomizationMenu(State):

    def __init__(self, game, gameMode=None):
        super().__init__(game)
        self.start_game = None
        self.back_button = None
        self.gameMode = gameMode
        self.board = Board()
        self.bot1_mode = "MinMax"
        self.bot2_mode = "MinMax"
        self.bot1_minMax = 2
        self.bot2_minMax = 2
        self.bot1_monteCarlo = 5
        self.bot2_monteCarlo = 5
        self.start_piece = "White"
        self.customize_initial_board_button = None
        self.initialize_buttons()


    def initialize_buttons(self):
        match self.gameMode:
            case GameMode.PLAYER_VS_PLAYER:
                self.buttons.extend([
                    ClickButton(
                        "Start Game", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 3 + 50,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.change_state("game", mode=self.gameMode)),

                    ClickButton(
                        "Custom Init Board", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 3 + 150,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.change_state("initial_board_customization")),
                    ClickButton(
                        "Go Back", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTONS_HEIGHT + 50,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.go_back())
                ])
            
            case GameMode.PLAYER_VS_AI:
                self.buttons.extend([
                    ClickButton(
                        "MinMax", 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - 2 * BUTTONS_HEIGHT - 100,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        SELECT_CYAN, WHITE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_ai_mode(1,"MinMax"), selected=True, group="ALG_IA",
                        alt_button_color=LIGHT_CYAN, alt_text_color=STEEL_BLUE),
                    ClickButton(
                        "-", 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH // 2 + 1*BUTTONS_WIDTH/6, 160 + 2 * BUTTONS_HEIGHT,
                        4*BUTTONS_HEIGHT/6, BUTTONS_WIDTH/6,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_minmax_depth(1,"-")),
                    ClickButton(
                        "+", 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH // 2 + 4*BUTTONS_WIDTH/6, 160 + 2 * BUTTONS_HEIGHT,
                        4*BUTTONS_HEIGHT/6, BUTTONS_WIDTH/6,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_minmax_depth(1,"+")),
                    ClickButton(
                        "MonteCarlo", 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - 2 * BUTTONS_HEIGHT - 100,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_ai_mode(1,"MonteCarlo"), group="ALG_IA",
                        alt_button_color=SELECT_CYAN, alt_text_color=WHITE),
                    ClickButton(
                        "-", 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH // 2 + 1*BUTTONS_WIDTH/6, 160 + 2 * BUTTONS_HEIGHT,
                        4*BUTTONS_HEIGHT/6, BUTTONS_WIDTH/6,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_montecarlo_time(1,"-")),
                    ClickButton(
                        "+", 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH // 2 + 4*BUTTONS_WIDTH/6, 160 + 2 * BUTTONS_HEIGHT,
                        4*BUTTONS_HEIGHT/6, BUTTONS_WIDTH/6,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_montecarlo_time(1,"+")),
                    ClickButton(
                        "White", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, 290 + 2 * BUTTONS_HEIGHT,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        (243,243,243), (30,58,95), (235,235,235), (30,58,95), STEEL_BLUE, (91,123,155),
                        lambda: self.change_start_piece(),
                        "Black", (30,58,95), WHITE, (50,80,120), WHITE, CADET_BLUE, CADET_BLUE,
                        ),
                    ClickButton(
                        "Start Game", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, 425 + 2 * BUTTONS_HEIGHT,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.change_state("game", mode=self.gameMode, player=self.start_piece , bot1_mode=self.bot1_mode,
                                                              bot1_difficulty=self.bot1_minMax if self.bot1_mode == "MinMax" else self.bot1_monteCarlo)),
                    ClickButton(
                        "Custom Init Board", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, 505 + 2 * BUTTONS_HEIGHT,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.change_state("initial_board_customization")),
                    ClickButton(
                        "Go Back", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, 585 + 2 * BUTTONS_HEIGHT,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.go_back())
                ])

            case GameMode.AI_VS_AI:
                self.buttons.extend([ 
                    ClickButton(
                        "MinMax", 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - 2 * BUTTONS_HEIGHT - 100,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        SELECT_CYAN, WHITE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_ai_mode(1,"MinMax"), selected=True, group="ALG_IA1",
                        alt_button_color=LIGHT_CYAN, alt_text_color=STEEL_BLUE),
                    ClickButton(
                        "-", 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH // 2 + 1*BUTTONS_WIDTH/6, 160 + 2 * BUTTONS_HEIGHT,
                        4*BUTTONS_HEIGHT/6, BUTTONS_WIDTH/6,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_minmax_depth(1,"-")),
                    ClickButton(
                        "+", 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH // 2 + 4*BUTTONS_WIDTH/6, 160 + 2 * BUTTONS_HEIGHT,
                        4*BUTTONS_HEIGHT/6, BUTTONS_WIDTH/6,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_minmax_depth(1,"+")),
                    ClickButton(
                        "MonteCarlo", 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - 2 * BUTTONS_HEIGHT - 100,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_ai_mode(1,"MonteCarlo"), group="ALG_IA1",
                        alt_button_color=SELECT_CYAN, alt_text_color=WHITE),
                    ClickButton(
                        "-", 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH // 2 + 1*BUTTONS_WIDTH/6, 160 + 2 * BUTTONS_HEIGHT,
                        4*BUTTONS_HEIGHT/6, BUTTONS_WIDTH/6,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_montecarlo_time(1,"-")),
                    ClickButton(
                        "+", 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH // 2 + 4*BUTTONS_WIDTH/6, 160 + 2 * BUTTONS_HEIGHT,
                        4*BUTTONS_HEIGHT/6, BUTTONS_WIDTH/6,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_montecarlo_time(1,"+")),
                    ClickButton(
                        "MinMax", 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        SELECT_CYAN, WHITE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_ai_mode(2,"MinMax"), selected=True, group="ALG_IA2",
                        alt_button_color=LIGHT_CYAN, alt_text_color=STEEL_BLUE),
                    ClickButton(
                        "-", 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH // 2 + 1*BUTTONS_WIDTH/6, 260 + 4 * BUTTONS_HEIGHT,
                        4*BUTTONS_HEIGHT/6, BUTTONS_WIDTH/6,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_minmax_depth(2,"-")),
                    ClickButton(
                        "+", 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH // 2 + 4*BUTTONS_WIDTH/6, 260 + 4 * BUTTONS_HEIGHT,
                        4*BUTTONS_HEIGHT/6, BUTTONS_WIDTH/6,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_minmax_depth(2,"+")),
                    ClickButton(
                        "MonteCarlo", 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_ai_mode(2,"MonteCarlo"), group="ALG_IA2",
                        alt_button_color=SELECT_CYAN, alt_text_color=WHITE),
                    ClickButton(
                        "-", 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH // 2 + 1*BUTTONS_WIDTH/6, 260 + 4 * BUTTONS_HEIGHT,
                        4*BUTTONS_HEIGHT/6, BUTTONS_WIDTH/6,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_montecarlo_time(2,"-")),
                    ClickButton(
                        "+", 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH // 2 + 4*BUTTONS_WIDTH/6, 260 + 4 * BUTTONS_HEIGHT,
                        4*BUTTONS_HEIGHT/6, BUTTONS_WIDTH/6,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        lambda: self.change_montecarlo_time(2,"+")),                  
                    ClickButton(
                        "Start Game", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, 425 + 2 * BUTTONS_HEIGHT,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.change_state("game", mode=self.gameMode, bot1_mode=self.bot1_mode, bot2_mode=self.bot2_mode,
                                                              bot1_difficulty=self.bot1_minMax if self.bot1_mode == "MinMax" else self.bot1_monteCarlo,
                                                              bot2_difficulty=self.bot2_minMax if self.bot2_mode == "MinMax" else self.bot2_monteCarlo)),
                    ClickButton(
                        "Custom Init Board", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, 505 + 2 * BUTTONS_HEIGHT,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.change_state("initial_board_customization")),
                    ClickButton(
                        "Go Back", 
                        SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, 585 + 2 * BUTTONS_HEIGHT,
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

    def change_start_piece(self):
        if self.start_piece == "White":
            self.start_piece = "Black"
        else:
            self.start_piece = "White"

    def change_minmax_depth(self, bot, increment):
        if bot == 1:
            if increment == "+" and self.bot1_minMax < 10:
                self.bot1_minMax +=1
            elif increment == "-" and self.bot1_minMax > 1:
                self.bot1_minMax -=1
        else:
            if increment == "+" and self.bot2_minMax < 10:
                self.bot2_minMax +=1
            elif increment == "-" and self.bot2_minMax > 1:
                self.bot2_minMax -=1 
                
    def change_montecarlo_time(self, bot, increment):
        if bot == 1:
            if increment == "+" and self.bot1_monteCarlo < 60:
                self.bot1_monteCarlo +=1
            elif increment == "-" and self.bot1_monteCarlo > 1:
                self.bot1_monteCarlo -=1
        else:
            if increment == "+" and self.bot2_monteCarlo < 60:
                self.bot2_monteCarlo +=1
            elif increment == "-" and self.bot2_monteCarlo > 1:
                self.bot2_monteCarlo -=1 


    def draw(self):
        screen = self.game.screen
        # Draw the title of the screen
        draw_text(screen,"Game Customization",FONT_TITLE,(60, 100, 140), SCREEN_WIDTH // 2 - FONT_TITLE.size("Game Customization")[0] // 2, 50)
        # Draw buttons
        super().draw()
        # Draw texts
        match self.gameMode:
            case GameMode.PLAYER_VS_AI:
                draw_text(screen,"Player Color",FONT,(60, 100, 140), 
                        SCREEN_WIDTH // 2 - FONT.size("Player Color")[0] // 2, 240 + 2 * BUTTONS_HEIGHT)
                
                draw_text(screen,"Depth",FONT,(60, 100, 140), 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH //2 + 3*BUTTONS_WIDTH/6 - FONT.size(str("Depth"))[0] // 2, 115 + 2 * BUTTONS_HEIGHT)
                draw_text(screen,str(self.bot1_minMax),FONT,(60, 100, 140), 
                          SCREEN_WIDTH // 5 - BUTTONS_WIDTH //2 + 3*BUTTONS_WIDTH/6 - FONT.size(str(self.bot1_minMax))[0] // 2, 155 + 2 * BUTTONS_HEIGHT + FONT.size(str(self.bot1_minMax))[1] // 2)

                draw_text(screen,"Time(s)",FONT,(60, 100, 140), 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH //2 + 3*BUTTONS_WIDTH/6 - FONT.size("Time(s)")[0] // 2, 115 + 2 * BUTTONS_HEIGHT)
                draw_text(screen,str(self.bot1_monteCarlo),FONT,(60, 100, 140), 
                          SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH //2 + 3*BUTTONS_WIDTH/6 - FONT.size(str(self.bot1_monteCarlo))[0] // 2, 155 + 2 * BUTTONS_HEIGHT + FONT.size(str(self.bot1_monteCarlo))[1] // 2)
            
            case GameMode.AI_VS_AI:
                #AI 1
                draw_text(screen,"AI 1",FONT,(60, 100, 140), 
                        SCREEN_WIDTH // 2 - FONT.size("AI 1")[0] // 2, 115 + BUTTONS_HEIGHT)
                
                draw_text(screen,"Depth",FONT,(60, 100, 140), 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH //2 + 3*BUTTONS_WIDTH/6 - FONT.size(str("Depth"))[0] // 2, 115 + 2 * BUTTONS_HEIGHT)
                draw_text(screen,str(self.bot1_minMax),FONT,(60, 100, 140), 
                          SCREEN_WIDTH // 5 - BUTTONS_WIDTH //2 + 3*BUTTONS_WIDTH/6 - FONT.size(str(self.bot1_minMax))[0] // 2, 155 + 2 * BUTTONS_HEIGHT + FONT.size(str(self.bot1_minMax))[1] // 2)

                draw_text(screen,"Time(s)",FONT,(60, 100, 140), 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH //2 + 3*BUTTONS_WIDTH/6 - FONT.size("Time(s)")[0] // 2, 115 + 2 * BUTTONS_HEIGHT)
                draw_text(screen,str(self.bot1_monteCarlo),FONT,(60, 100, 140), 
                          SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH //2 + 3*BUTTONS_WIDTH/6 - FONT.size(str(self.bot1_monteCarlo))[0] // 2, 155 + 2 * BUTTONS_HEIGHT + FONT.size(str(self.bot1_monteCarlo))[1] // 2)

                #AI 2
                draw_text(screen,"AI 2",FONT,(60, 100, 140), 
                        SCREEN_WIDTH // 2 - FONT.size("AI 2")[0] // 2, 215 + 3 * BUTTONS_HEIGHT)
                
                draw_text(screen,"Depth",FONT,(60, 100, 140), 
                        SCREEN_WIDTH // 5 - BUTTONS_WIDTH //2 + 3*BUTTONS_WIDTH/6 - FONT.size(str("Depth"))[0] // 2, 215 + 4 * BUTTONS_HEIGHT)
                draw_text(screen,str(self.bot2_minMax),FONT,(60, 100, 140), 
                          SCREEN_WIDTH // 5 - BUTTONS_WIDTH //2 + 3*BUTTONS_WIDTH/6 - FONT.size(str(self.bot2_minMax))[0] // 2, 255 + 4 * BUTTONS_HEIGHT + FONT.size(str(self.bot1_minMax))[1] // 2)

                draw_text(screen,"Time(s)",FONT,(60, 100, 140), 
                        SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH //2 + 3*BUTTONS_WIDTH/6 - FONT.size("Time(s)")[0] // 2, 215 + 4 * BUTTONS_HEIGHT)
                draw_text(screen,str(self.bot2_monteCarlo),FONT,(60, 100, 140), 
                          SCREEN_WIDTH // 5 * 4 - BUTTONS_WIDTH //2 + 3*BUTTONS_WIDTH/6 - FONT.size(str(self.bot2_monteCarlo))[0] // 2, 255 + 4 * BUTTONS_HEIGHT + FONT.size(str(self.bot1_monteCarlo))[1] // 2)
            
              