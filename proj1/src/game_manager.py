import pygame
import config
from states.main_menu_state import MainMenuState
from states.game import Game
from states.game_state import GameState
from states.instructions_state import InstructionsState
from states.option_menu_state import OptionMenuState
from states.game_customization_menu_state import GameCustomizationMenu
from states.board_customization_menu_state import BoardCustomizationMenu
from states.board_creation_state import BoardCreationMenu
from states.game_over import GameOver
from board import Board
from json_actions import load_game, save_game, clear_game
from mode import GameMode

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Yinsh")
        self.running = True
        self.ai_thread = None
        self.ai_thinking = False
        self.stop_ai = False
        self.selected_board = "Default"
        self.state_stack = []  # Stack to track state history
        self.states = {
            "menu": MainMenuState(self),
            "instructions": InstructionsState(self),
            "initial_board_customization": BoardCustomizationMenu(self),
            "board_creation_menu": BoardCreationMenu(self),
        }
        self.current_state = self.states["menu"]

    def change_state(self, new_state, *args, **kwargs):
        self.stop_ai = True
        if self.current_state:
            self.state_stack.append(self.current_state)  # Save the current state
        if new_state == "customization":
            self.current_state = GameCustomizationMenu(self,*args, **kwargs)
        elif new_state == "game":
            self.ai_thread = None
            self.ai_thinking = False
            self.stop_ai = False
            self.current_state = Game(self,*args, **kwargs)
        elif new_state == "game_over":
            self.current_state = GameOver(self,*args, **kwargs)
        elif new_state == "initial_board_customization":
            self.current_state = BoardCustomizationMenu(self)
        elif new_state == "board_creation_menu":
            self.current_state = BoardCreationMenu(self,*args)
        elif new_state == "options":
            self.state_stack.pop()
            self.state_stack.append(MainMenuState(self))
            self.current_state = OptionMenuState(self)
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

    def save_exit(self):
        save_game("src/json/game_state.json", self.current_state.state.to_dict())
        self.exit_game()

    def load_game_state(self):
        loaded_state = load_game("src/json/game_state.json")
        game_mode = GameMode(loaded_state['game_mode'])
        self.change_state("game", game_mode)
        self.current_state.state = GameState.from_dict(loaded_state,Board)
    
    def clear_game_state(self):
        clear_game("src/json/game_state.json")
        self.change_state("options")

    def exit_game(self):
        self.stop_ai = True
        if self.ai_thread and self.ai_thread.is_alive():
            self.ai_thread.join() 
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
            
            self.current_state.handle_events()
         
            self.draw_gradient_background((222, 247, 247), (240, 247, 255))
            self.current_state.draw()
            pygame.display.flip()

        pygame.quit()


