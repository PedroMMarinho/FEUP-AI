import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BUTTONS_HEIGHT, BUTTONS_WIDTH, FONT
from config import LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, CADET_BLUE, WHITE
from states.state import State
from ui import draw_text
from button import ClickButton
import os
import json

class GameOver(State):

    def __init__(self, game, winner=None,player_moves=None,p1_rings=None, p2_rings=None):
        super().__init__(game)
        self.winner = winner
        self.player_moves = player_moves
        self.p1_rings = p1_rings
        self.p2_rings = p2_rings
        self.buttons = [
            ClickButton("Export game",SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 + 3*BUTTONS_HEIGHT + 130,
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.export_to_file()),
            ClickButton("Back to menu", 
                SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 + BUTTONS_HEIGHT + 60,
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.change_state("menu")),
            ClickButton("Exit", 
                SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 + 2*BUTTONS_HEIGHT + 95,
                BUTTONS_HEIGHT, BUTTONS_WIDTH,
                FONT,
                LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                action=lambda: self.game.exit_game())
        ]    

    def draw(self):
        screen = self.game.screen
        font = pygame.font.Font(None, 60)
        fontSmall = pygame.font.Font(None, 50)
        draw_text(screen,"Game Over",font,(60, 100, 140), SCREEN_WIDTH // 2 - font.size("Game Over")[0] // 2, 160)

        if self.winner == 1:
            draw_text(screen,"White Player Wins",fontSmall,(60, 100, 140), SCREEN_WIDTH // 2 - fontSmall.size("White Player Wins")[0] // 2, 320)
        elif self.winner == 2:
            draw_text(screen,"Black Player Wins",fontSmall,(60, 100, 140), SCREEN_WIDTH // 2 - fontSmall.size("Black Player Wins")[0] // 2, 320)
        else:
            draw_text(screen,"Draw",fontSmall,(60, 100, 140), SCREEN_WIDTH // 2 - fontSmall.size("Draw")[0] // 2, 260)
            
        #Buttons
        super().draw()

    def export_to_file(self):
        dic = {}
        dic['player_moves'] = self.player_moves
        game_time = 0 
        for move in self.player_moves: 
            game_time += move[2]
        
        dic['game_time']  = game_time
        dic['rings'] = {'Player 1': self.p1_rings, 'Player 2': self.p2_rings}

        if os.path.exists("src/json/saves.json"):
            with open("src/json/saves.json", "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []  # If file is empty, start with an empty list
        else:
            data = []
        data.append(dic)
        with open("src/json/saves.json", "w") as file:
            json.dump(data,file,indent=4)

        self.game.change_state("menu")
        


    

