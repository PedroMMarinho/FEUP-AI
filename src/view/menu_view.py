import pygame
from settings import WIDTH, HEIGHT

def render_main_menu(screen,buttons, background_image):
    screen.blit(background_image, (0, 0))
    for button in buttons:
        button.draw(screen)
    pygame.display.flip()

def render_instructions_menu(screen, buttons,background_image):
    screen.blit(background_image, (0, 0))
    for button in buttons:
        button.draw(screen)
    # Render instructions
    pygame.display.flip()


def render_game_screen(screen,board,view):
    font = pygame.font.Font(None, 50)
    text = font.render("Game Screen - Press ESC to go back", True, (0, 0, 0))
    screen.fill((255, 255, 255))
    screen.blit(text, (WIDTH - 1500, HEIGHT - 820 ))
    view.draw_board(screen,board)
    pygame.display.flip()

