import pygame
from model.button import Button
from model.game_state import GameState
from view.menu_view import render_main_menu, render_instructions_menu, render_game_screen, render_settings_menu
from settings import WIDTH, HEIGHT

def main_menu(screen):
    buttons = [
        Button("Play", WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 60, (0, 100, 200), (0, 150, 255), lambda: GameState.GAME),
        Button("Instructions", WIDTH // 2 - 150, HEIGHT // 2 - 20, 300, 60, (0, 100, 200), (0, 150, 255), lambda: GameState.INSTRUCTIONS_MENU),
        Button("Settings", WIDTH // 2 - 150, HEIGHT // 2 + 60, 300, 60, (0, 100, 200), (0, 150, 255), lambda: GameState.SETTINGS_MENU),
        Button("Exit", WIDTH // 2 - 150, HEIGHT // 2 + 140, 300, 60, (200, 0, 0), (255, 0, 0), lambda: GameState.EXIT)
    ]

    running = True
    while running:
        render_main_menu(screen, buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            for button in buttons:
                if button.is_clicked(event):
                    return button.action()
    
    return GameState.MAIN_MENU

def instructions_menu(screen):
    running = True
    while running:
        render_instructions_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return GameState.MAIN_MENU
    return GameState.INSTRUCTIONS_MENU

def game_screen(screen):
    running = True
    while running:
        render_game_screen(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return GameState.MAIN_MENU
    return GameState.GAME

def settings_menu(screen):
    global FULLSCREEN
    running = True
    while running:
        render_settings_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return GameState.MAIN_MENU
    return GameState.SETTINGS_MENU