import pygame
import config
from states.main_menu_state import MainMenuState
from states.game_state import GameState
# from states.instructions_state import InstructionsState



class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Yinsh")
        self.running = True
        self.states = {
            "menu": MainMenuState(self),
            "game": GameState(self),
           #"instructions": InstructionsState(self)
        }
        self.current_state = self.states["menu"]

    def change_state(self, new_state):
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


