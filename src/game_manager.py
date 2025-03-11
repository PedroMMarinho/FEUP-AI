import pygame
import config
from states.main_menu_state import MainMenuState
from states.game_state import GameState
from states.instructions_state import InstructionsState
from states.option_menu_state import OptionMenuState
from states.game_customization_menu_state import GameCustomizationMenu


class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Yinsh")
        self.running = True
        self.states = {
            "menu": MainMenuState(self),
            "instructions": InstructionsState(self),
            "options" : OptionMenuState(self),
        }
        self.current_state = self.states["menu"]

    def change_state(self, new_state, *args):
        if new_state == "customization":
            self.current_state = GameCustomizationMenu(self,*args)
        elif new_state == "game":
            for i in args:
                print (i)
            self.current_state = GameState(self,*args)
        else:
            self.current_state = self.states[new_state]

    def run(self):
        while self.running:
            self.screen.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_state.handle_events(event)
            
            self.current_state.draw()
            pygame.display.flip()

        pygame.quit()


