import pygame
from model.button import Button
from model.game_state import GameState
from view.menu_view import render_main_menu, render_instructions_menu, render_game_screen, render_game_mode_selection_menu, render_ai_vs_human_menu
from settings import WIDTH, HEIGHT
from model.board import Board
from view.board_view import BoardView

def main_menu(screen,background_image):
    buttons = [
        Button("Play", WIDTH // 2 - 125, HEIGHT // 3 , 300, 60, (0, 100, 200), (0, 150, 255), lambda: GameState.GAME_MODE_SELECTION),
        Button("Instructions", WIDTH // 2 - 125, HEIGHT // 3 + 80, 300, 60, (0, 100, 200), (0, 150, 255), lambda: GameState.INSTRUCTIONS_MENU),
        #Button("Exit", WIDTH // 2 - 125, HEIGHT // 3 + 160, 300, 60, (200, 0, 0), (255, 0, 0), lambda: GameState.EXIT),
    ]
    running = True
    pygame.event.clear()
    while running:
        render_main_menu(screen, buttons, background_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            for button in buttons:
                if button.is_clicked(event):
                    return button.action()
    
    return GameState.MAIN_MENU

def instructions_menu(screen,background_image):
    button_width = 250
    button_height = 60 

    buttons = [
        Button(
            "Go Back",
            70,  
            HEIGHT - button_height - 100,  
            button_width,
            button_height,
            (200, 0, 0),
            (255, 0, 0),
            lambda: GameState.MAIN_MENU,
        ),
    ]
    running = True
    pygame.event.clear()
    while running:
        render_instructions_menu(screen,buttons,background_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            for button in buttons:
                if button.is_clicked(event):
                    return button.action()
    return GameState.INSTRUCTIONS_MENU


def game_screen(screen, mode):
    board = Board()
    view = BoardView(board)
    running = True
    while running:
        render_game_screen(screen, board, view)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return GameState.MAIN_MENU
        
    return GameState.GAME

def ai_human_menu(screen, background_image):
    buttons = [
        Button("Easy", WIDTH // 2 - 125, HEIGHT // 3, 300, 60, (0, 100, 200), (0, 150, 255), lambda: GameState.AI_HUMAN),
        Button("Medium", WIDTH // 2 - 125, HEIGHT // 3 + 80, 300, 60, (0, 100, 200), (0, 150, 255), lambda: GameState.AI_HUMAN),
        Button("Hard", WIDTH // 2 - 125, HEIGHT // 3 + 160, 300, 60, (200, 0, 0), (255, 0, 0), lambda: GameState.AI_HUMAN),
        Button("Back", WIDTH // 2 - 125, HEIGHT // 3 + 240, 300, 60, (100, 100, 100), (150, 150, 150), lambda: GameState.GAME_MODE_SELECTION),
    ]
    running = True
    pygame.event.clear()
    while running:
        render_ai_vs_human_menu(screen, buttons, background_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            for button in buttons:
                if button.is_clicked(event):
                    return button.action()
    
    return GameState.GAME_MODE_SELECTION


def game_screen_options(screen, mode):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
        # Handle Mode
        match mode:
            case "human_human":
                return game_screen(screen, mode)
            case "ai_human":
                # Call the function to choose the AI difficulty
                pass
            case "ai_ai":
                # Call the function to choose the AI difficulty
                pass
            case _:
                pass
        
    return GameState.GAME




def game_mode_selection_menu(screen, background_image):
    buttons = [
        Button("Player vs Player", WIDTH // 2 - 125, HEIGHT // 3, 300, 60, (0, 100, 200), (0, 150, 255), lambda: GameState.HUMAN_HUMAN),
        Button("AI vs Human", WIDTH // 2 - 125, HEIGHT // 3 + 80, 300, 60, (0, 100, 200), (0, 150, 255), lambda: GameState.AI_HUMAN),
        Button("AI vs AI", WIDTH // 2 - 125, HEIGHT // 3 + 160, 300, 60, (200, 0, 0), (255, 0, 0), lambda: GameState.AI_AI),
        Button("Back", WIDTH // 2 - 125, HEIGHT // 3 + 240, 300, 60, (100, 100, 100), (150, 150, 150), lambda: GameState.MAIN_MENU),
    ]

    running = True
    pygame.event.clear()
    while running:
        
        render_game_mode_selection_menu(screen, buttons, background_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            for button in buttons:
                if button.is_clicked(event):
                    return button.action()
    
    return GameState.GAME_MODE_SELECTION