import pygame
from model.button import Button, ToggleButton
from model.game_state import GameState
from view.menu_view import render_main_menu, render_instructions_menu, render_game_screen, render_game_mode_selection_menu, render_ai_vs_human_menu
from settings import WIDTH, HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, LIGHT_BLUE, GREY, LIGHT_GREY, RED, LIGHT_RED, GREEN, LIGHT_GREEN, YELLOW, LIGHT_YELLOW
from model.board import Board
from view.board_view import BoardView



def main_menu(screen,background_image):
    buttons = [
        Button("Play", WIDTH // 2 - 125, HEIGHT // 3 , BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, LIGHT_BLUE, lambda: GameState.GAME_MODE_SELECTION),
        Button("Instructions", WIDTH // 2 - 125, HEIGHT // 3 + 80, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, LIGHT_BLUE, lambda: GameState.INSTRUCTIONS_MENU),
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


    buttons = [
        Button(
            "Go Back",
            70,  
            HEIGHT - BUTTON_HEIGHT - 100,  
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            GREY,
            LIGHT_GREY,
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
    difficulty_buttons = [
        ToggleButton("Easy", WIDTH // 2 - 320, 300, 200, BUTTON_HEIGHT, GREEN, LIGHT_GREEN, (0, 150, 0), None),
        ToggleButton("Medium", WIDTH // 2 - 80 , 300, 200, BUTTON_HEIGHT, YELLOW, LIGHT_YELLOW, (150, 150, 0), None),
        ToggleButton("Hard", WIDTH // 2 + 1 + 160,300, 200, BUTTON_HEIGHT, RED, LIGHT_RED, (150, 0, 0), None),
    ]

    other_buttons = [
        Button("Go Back", 70, HEIGHT - BUTTON_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT, GREY, LIGHT_GREY, lambda: GameState.GAME_MODE_SELECTION),
        Button("Play", WIDTH // 2 - 125, HEIGHT - 400, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, LIGHT_BLUE, lambda: GameState.GAME),
    ]

    # Assign group reference so buttons can deselect each other
    for button in difficulty_buttons:
        button.group = difficulty_buttons

    running = True
    pygame.event.clear()
    while running:
        render_ai_vs_human_menu(screen, difficulty_buttons, background_image, other_buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            
            # Handle clicks on difficulty buttons
            for button in difficulty_buttons:
                button.is_clicked(event)
            
            # Handle clicks on other buttons
            for other_b in other_buttons:
                if other_b.is_clicked(event):
                    if other_b.action() == GameState.GAME:
                        if any(button.active for button in difficulty_buttons):
                            return game_screen(screen, "ai_human")
                    else:
                        return other_b.action()

    return GameState.GAME_MODE_SELECTION



def game_screen_options(screen, background_image ,mode):
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
                return ai_human_menu(screen, background_image)
            case "ai_ai":
                # Call the function to choose the AI difficulty
                pass
            case _:
                pass
        
    return GameState.GAME




def game_mode_selection_menu(screen, background_image):
    buttons = [
        Button("Player vs Player", WIDTH // 2 - 125, HEIGHT // 3, 300, 60, BLUE, LIGHT_BLUE, lambda: GameState.HUMAN_HUMAN),
        Button("AI vs Human", WIDTH // 2 - 125, HEIGHT // 3 + 80, 300, 60, BLUE, LIGHT_BLUE, lambda: GameState.AI_HUMAN),
        Button("AI vs AI", WIDTH // 2 - 125, HEIGHT // 3 + 160, 300, 60, RED, LIGHT_RED, lambda: GameState.AI_AI),
        Button("Back", WIDTH // 2 - 125, HEIGHT // 3 + 240, 300, 60, GREY, LIGHT_GREY, lambda: GameState.MAIN_MENU),
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