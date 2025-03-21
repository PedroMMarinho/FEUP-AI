import pygame
import config
from states.main_menu_state import MainMenuState
from states.game_state import GameState
from states.instructions_state import InstructionsState
from states.option_menu_state import OptionMenuState
from states.game_customization_menu_state import GameCustomizationMenu
from states.board_customization_menu_state import BoardCustomizationMenu
from states.board_creation_state import BoardCreationMenu

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Yinsh")
        self.running = True
        self.selected_board = "Default"
        self.state_stack = []  # Stack to track state history
        self.states = {
            "menu": MainMenuState(self),
            "instructions": InstructionsState(self),
            "options" : OptionMenuState(self),
            "initial_board_customization": BoardCustomizationMenu(self),
            "board_creation_menu": BoardCreationMenu(self)
        }
        self.current_state = self.states["menu"]

    def change_state(self, new_state, *args, **kwargs):

        if self.current_state:
            self.state_stack.append(self.current_state)  # Save the current state

        if new_state == "customization":
            self.current_state = GameCustomizationMenu(self,*args, **kwargs)
        elif new_state == "game":
            for i in args:
                print (i)
            self.current_state = GameState(self,*args, **kwargs)
        elif new_state == "initial_board_customization":
            self.current_state = BoardCustomizationMenu(self)
        elif new_state == "board_creation_menu":
            self.current_state = BoardCreationMenu(self)
        else:
            self.current_state = self.states[new_state]

    def change_without_save(self,new_state):
        self.state_stack.pop()
        if new_state == "initial_board_customization":
            self.current_state = BoardCustomizationMenu(self)

    def go_back(self):
        """Return to the previous state if available."""
        if self.state_stack:
            self.current_state = self.state_stack.pop()
    
    def exit_game(self):
        self.running = False

    def draw_gradient_background(self, color_top, color_bottom):
        for y in range(config.SCREEN_HEIGHT):
            color = (
                color_top[0] + (color_bottom[0] - color_top[0]) * y // config.SCREEN_HEIGHT,
                color_top[1] + (color_bottom[1] - color_top[1]) * y // config.SCREEN_HEIGHT,
                color_top[2] + (color_bottom[2] - color_top[2]) * y // config.SCREEN_HEIGHT
            )
            pygame.draw.line(self.screen, color, (0, y), (config.SCREEN_WIDTH, y))

        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_state.handle_events(event)
            
            self.draw_gradient_background((222, 247, 247), (240, 247, 255))
            self.current_state.draw()
            pygame.display.flip()

        pygame.quit()


