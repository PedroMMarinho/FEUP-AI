import pygame
from settings import WIDTH, HEIGHT
from model.game_state import GameState
from controller.menu_controller import main_menu, instructions_menu, game_screen, settings_menu

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("YINSH")
    gameState = GameState.MAIN_MENU
    while True:
        match gameState:
            case GameState.MAIN_MENU:
                gameState = main_menu(screen)
            case GameState.INSTRUCTIONS_MENU:
                gameState = instructions_menu(screen)
            case GameState.GAME:
                gameState = game_screen(screen)
            case GameState.SETTINGS_MENU:
                gameState = settings_menu(screen)
            case GameState.EXIT:
                pygame.quit()
                return
    