import pygame
from model.button import Button
from model.game_state import GameState
from view.menu_view import render_main_menu, render_instructions_menu, render_game_screen, render_settings_menu
from settings import WIDTH, HEIGHT
from model.board import Board
from view.board_view import BoardView

def main_menu(screen):
    buttons = [
        Button("Play", WIDTH // 3, HEIGHT // 3, 200, 60, (0, 100, 200), (0, 150, 255), lambda: GameState.GAME),
        Button("Instructions", WIDTH // 3, HEIGHT // 3 + 80, 200, 60, (0, 100, 200), (0, 150, 255), lambda: GameState.INSTRUCTIONS_MENU),
        Button("Settings", WIDTH // 3, HEIGHT // 3 + 160, 200, 60, (0, 100, 200), (0, 150, 255), lambda: GameState.SETTINGS_MENU),
        Button("Exit", WIDTH // 3, HEIGHT // 3 + 240, 200, 60, (200, 0, 0), (255, 0, 0), lambda: GameState.EXIT)
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
    board = Board()
    view = BoardView(board)
    while running:
        render_game_screen(screen,board,view)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameState.MAIN_MENU
                if event.key == pygame.K_f:
                    FULLSCREEN = not FULLSCREEN
                    return GameState.SETTINGS_MENU
    return GameState.SETTINGS_MENU