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


def render_game_mode_selection_menu(screen, buttons, background_image):
    screen.blit(background_image, (0, 0))
    for button in buttons:
        button.draw(screen)
    # Render what is needed for the game mode selection menu
    pygame.display.flip()

def render_ai_vs_ai_menu(screen, difficulty_buttons_bot1, difficulty_buttons_bot2 ,background_image, other_buttons):
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Choose the first AI difficulty", True, (0, 0, 0))
    bg_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 650))
    pygame.draw.rect(screen, (255, 255, 255, 150), bg_rect.inflate(20, 10))  

    screen.blit(text, bg_rect)

    text = font.render("Choose the second AI difficulty", True, (0, 0, 0))
    bg_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 450))
    pygame.draw.rect(screen, (255, 255, 255, 150), bg_rect.inflate(20, 10))  

    screen.blit(text, bg_rect)
    for button in difficulty_buttons_bot1:
        button.draw(screen)
    for button in difficulty_buttons_bot2:
        button.draw(screen)
    for button in other_buttons:
        button.draw(screen)
    
    # Render what is needed for the AI vs AI menu
    pygame.display.flip()

def render_ai_vs_human_menu(screen, buttons, background_image, other_buttons,switch_button):
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Choose the AI difficulty", True, (0, 0, 0))
    bg_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 650))
    pygame.draw.rect(screen, (255, 255, 255, 150), bg_rect.inflate(20, 10))  # Semi-transparent black

    screen.blit(text, bg_rect)

    text = font.render("Choose your piece color", True, (0, 0, 0))
    bg_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 450))
    pygame.draw.rect(screen, (255, 255, 255, 150), bg_rect.inflate(20, 10))  # Semi-transparent black

    screen.blit(text, bg_rect)
    for button in buttons:
        button.draw(screen)
        
    for button in other_buttons:
        button.draw(screen)

    switch_button.draw(screen)

    pygame.display.flip()