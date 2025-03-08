import pygame
from model.button import Button, ToggleButton, SwitchButton
from model.game_state import GameState
from view.menu_view import render_main_menu, render_instructions_menu, render_game_mode_selection_menu, render_ai_vs_human_menu, render_ai_vs_ai_menu
from settings import WIDTH, HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, LIGHT_BLUE, GREY, LIGHT_GREY, RED, LIGHT_RED, GREEN, LIGHT_GREEN, YELLOW, LIGHT_YELLOW, BLACK
from controller.game_controller import game_screen


def main_menu(screen,background_image):
    buttons = [
        Button("Play", WIDTH // 2 - 125, HEIGHT // 3 , BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, LIGHT_BLUE, lambda: GameState.GAME_MODE_SELECTION),
        Button("Instructions", WIDTH // 2 - 125, HEIGHT // 3 + 80, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, LIGHT_BLUE, lambda: GameState.INSTRUCTIONS_MENU),
        Button("Exit", WIDTH // 2 - 125, HEIGHT // 3 + 160, 300, 60, (200, 0, 0), (255, 0, 0), lambda: GameState.EXIT),
    ]
        
    while True:
        render_main_menu(screen, buttons, background_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            for button in buttons:
                if button.is_clicked(event):
                    return button.action()
    

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
   
    while True:
        render_instructions_menu(screen,buttons,background_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            for button in buttons:
                if button.is_clicked(event):
                    return button.action()



        
def ai_human_menu(screen, background_image):
    difficulty_buttons = [
        ToggleButton("Easy", WIDTH // 2 - 320, 300, 200, BUTTON_HEIGHT, GREEN, LIGHT_GREEN, (0, 150, 0), None),
        ToggleButton("Medium", WIDTH // 2 - 80 , 300, 200, BUTTON_HEIGHT, YELLOW, LIGHT_YELLOW, (150, 150, 0), None),
        ToggleButton("Hard", WIDTH // 2 + 1 + 160,300, 200, BUTTON_HEIGHT, RED, LIGHT_RED, (150, 0, 0), None),
    ]

    other_buttons = [
        Button("Go Back", 70, HEIGHT - BUTTON_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT, GREY, LIGHT_GREY, lambda: GameState.GAME_MODE_SELECTION),
        Button("Play", WIDTH // 2 - 125, HEIGHT - 200, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, LIGHT_BLUE, lambda: GameState.GAME),
    ]

    switch_button = SwitchButton("Black Pieces", "White Pieces", WIDTH // 2 - 125, HEIGHT // 2 + 30, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    # Assign group reference so buttons can deselect each other
    for button in difficulty_buttons:
        button.group = difficulty_buttons

    while True:
        render_ai_vs_human_menu(screen, difficulty_buttons, background_image, other_buttons, switch_button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            
            switch_button.handle_click(event)
          

            # Handle clicks on difficulty buttons
            for button in difficulty_buttons:
                button.is_clicked(event)
            
            # Handle clicks on other buttons
            for other_b in other_buttons:
                if other_b.is_clicked(event):
                    if other_b.action() == GameState.GAME:
                        for button in difficulty_buttons:
                            if button.active:
                                return game_screen(screen, "ai_human", button.text,None, switch_button.selected_piece)
                    else:
                        return other_b.action()




def game_options(screen, background_image ,mode):
    
    while True:
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
                return ai_ai_menu(screen, background_image)
            case _:
                pass
        

def ai_ai_menu(screen, background_image):
    difficulty_buttons_bot1 = [
        ToggleButton("Easy", WIDTH // 2 - 320, 300, 200, BUTTON_HEIGHT, GREEN, LIGHT_GREEN, (0, 150, 0), None),
        ToggleButton("Medium", WIDTH // 2 - 80 , 300, 200, BUTTON_HEIGHT, YELLOW, LIGHT_YELLOW, (150, 150, 0), None),
        ToggleButton("Hard", WIDTH // 2 + 1 + 160,300, 200, BUTTON_HEIGHT, RED, LIGHT_RED, (150, 0, 0), None),
    ]

    difficulty_buttons_bot2 = [
        ToggleButton("Easy", WIDTH // 2 - 320, 500, 200, BUTTON_HEIGHT, GREEN, LIGHT_GREEN, (0, 150, 0), None),
        ToggleButif event.type == pygame.QUIT:
                return GameState.EXIT
            for button in buttons:
                if button.is_clicked(event):
                    return button.action()
    ton("Medium", WIDTH // 2 - 80 , 500, 200, BUTTON_HEIGHT, YELLOW, LIGHT_YELLOW, (150, 150, 0), None),
        ToggleButton("Hard", WIDTH // 2 + 1 + 160,500, 200, BUTTON_HEIGHT, RED, LIGHT_RED, (150, 0, 0), None),
    ]

    other_buttons = [
        Button("Go Back", 70, HEIGHT - BUTTON_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT, GREY, LIGHT_GREY, lambda: GameState.GAME_MODE_SELECTION),
        Button("Play", WIDTH // 2 - 125, HEIGHT - 200, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, LIGHT_BLUE, lambda: GameState.GAME),
    ]

    # Assign group reference so buttons can deselect each other
    for button in difficulty_buttons_bot1:
        button.group = difficulty_buttons_bot1

    for button in difficulty_buttons_bot2:
        button.group = difficulty_buttons_bot2

    while True:
        render_ai_vs_ai_menu(screen, difficulty_buttons_bot1, difficulty_buttons_bot2 ,background_image, other_buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            
            # Handle clicks on difficulty buttons
            for button in difficulty_buttons_bot1:
                button.is_clicked(event)
            
            for button in difficulty_buttons_bot2:
                button.is_clicked(event)

            # Handle clicks on other buttons
            for other_b in other_buttons:
                if other_b.is_clicked(event):
                    if other_b.action() == GameState.GAME:
                        b1 = None
                        b2 = None
                        for button1 in difficulty_buttons_bot1:
                            if button1.active:
                                b1 = button1.text
                        for button2 in difficulty_buttons_bot2:
                            if button2.active:
                                b2 = button2.text
                        if b1 and b2:
                            return game_screen(screen, "ai_ai", b1, b2)
                        
                    else:
                        return other_b.action()


def game_mode_selection_menu(screen, background_image):
    buttons = [
        Button("Player vs Player", WIDTH // 2 - 125, HEIGHT // 3, 300, 60, BLUE, LIGHT_BLUE, lambda: GameState.HUMAN_HUMAN),
        Button("AI vs Human", WIDTH // 2 - 125, HEIGHT // 3 + 80, 300, 60, BLUE, LIGHT_BLUE, lambda: GameState.AI_HUMAN),
        Button("AI vs AI", WIDTH // 2 - 125, HEIGHT // 3 + 160, 300, 60, RED, LIGHT_RED, lambda: GameState.AI_AI),
        Button("Back", WIDTH // 2 - 125, HEIGHT // 3 + 240, 300, 60, GREY, LIGHT_GREY, lambda: GameState.MAIN_MENU),
    ]
    
    while True:
        render_game_mode_selection_menu(screen, buttons, background_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            for button in buttons:
                if button.is_clicked(event):
                    return button.action()
    
