import pygame
from pygame._sdl2 import Window
from settings import WIDTH, HEIGHT
from model.game_state import GameState
from controller.menu_controller import main_menu, instructions_menu, game_screen, game_mode_selection_menu
import sys
def run_game():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    Window.from_display_module().maximize()
    gameState = GameState.MAIN_MENU
    # Load background image
    background = pygame.image.load("src/assets/yinsh.png")
    background_image = pygame.transform.scale(background, (WIDTH, HEIGHT -50))
    running = True
    while running:
        match gameState:
            case GameState.MAIN_MENU:
                gameState = main_menu(screen,background_image)
            case GameState.INSTRUCTIONS_MENU:
                gameState = instructions_menu(screen,background_image)
            case GameState.GAME_MODE_SELECTION:
                gameState = game_mode_selection_menu(screen, background_image)  # NEW FUNCTION
            case GameState.HUMAN_HUMAN:
                gameState = game_screen(screen, mode="human_human")  
            case GameState.AI_HUMAN:
                gameState = game_screen(screen, mode="ai_human")
            case GameState.AI_AI:
                gameState = game_screen(screen, mode="ai_ai")
            case GameState.EXIT:
                running = False
    
    pygame.quit()
    sys.exit()
    