import pygame
from settings import WIDTH, HEIGHT
import view.board_view as bv

def render_main_menu(screen,buttons):
    screen.fill((255, 255, 255))
    for button in buttons:
        button.draw(screen)
    pygame.display.flip()

def render_instructions_menu(screen):
    font = pygame.font.Font(None, 50)
    text = font.render("Instructions - Press ESC to go back", True, (0, 0, 0))
    screen.fill((255, 255, 255))
    screen.blit(text, (WIDTH//6, HEIGHT//2))
    pygame.display.flip()


def render_game_screen(screen,board,view):
    font = pygame.font.Font(None, 50)
    text = font.render("Game Screen - Press ESC to go back", True, (0, 0, 0))
    screen.fill((255, 255, 255))
    screen.blit(text, (WIDTH - 1500, HEIGHT - 820 ))
    view.draw_board(screen,board)
    
    pygame.display.flip()


def render_settings_menu(screen):
    font = pygame.font.Font(None, 50)
    text = font.render("Settings - Press F to toggle fullscreen, ESC to go back", True, (0, 0, 0))
    screen.fill((255, 255, 255))
    screen.blit(text, (WIDTH//6, HEIGHT//2))
    pygame.display.flip()