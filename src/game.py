import pygame
from settings import WIDTH, HEIGHT
from model.game_state import GameState
from controller.menu_controller import main_menu, instructions_menu, game_options, game_mode_selection_menu
import sys

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT - 50))
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
                gameState = game_mode_selection_menu(screen, background_image)  
            case GameState.HUMAN_HUMAN:
                gameState = game_options(screen, background_image ,mode="human_human")  
            case GameState.AI_HUMAN:
                gameState = game_options(screen, background_image, mode="ai_human")
            case GameState.AI_AI:
                gameState = game_options(screen, background_image, mode="ai_ai")
            case GameState.EXIT:
                running = False
    
    pygame.quit()
    sys.exit()
    