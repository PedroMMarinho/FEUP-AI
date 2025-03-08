import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BUTTONS_HEIGHT, BUTTONS_WIDTH, BLACK, WHITE
from states.state import State
from ui import draw_button, draw_text


class MainMenuState(State):

    def __init__(self, game):
        super().__init__(game)
        self.play_button = None
        self.instructions_button = None
        self.exit_button = None

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.play_button.collidepoint(x, y):
                self.game.change_state("game")  
            elif self.instructions_button.collidepoint(x, y):
                pass
                # self.game.change_state("instructions")
            elif self.exit_button.collidepoint(x, y):
                self.game.running = False

    def draw(self):
        screen = self.game.screen
        font = pygame.font.SysFont(None, 50)
        draw_text(screen,"Yinsh",font,BLACK, SCREEN_WIDTH // 2 - font.size("Yinsh")[0] // 2, 150)
        self.play_button = draw_button(screen, "Play", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 - BUTTONS_HEIGHT - 30, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
        self.instructions_button = draw_button(screen, "Instructions", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)
        self.exit_button = draw_button(screen, "Exit", SCREEN_WIDTH // 2 - BUTTONS_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTONS_HEIGHT // 2 + BUTTONS_HEIGHT + 30, BUTTONS_WIDTH, BUTTONS_HEIGHT, font, BLACK, WHITE)



'''

    def __init__(self):
        self.font = pygame.font.SysFont(None, 50)
    
    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Transition to the game state (e.g., clicking 'Start')
            game_state_manager.change_state(GameStatePlay())
    
    def draw(self):
        screen.fill((0, 0, 0))
        title_text = self.font.render("Yinsh Game", True, (255, 255, 255))
        start_text = self.font.render("Start Game", True, (255, 255, 255))
        screen.blit(title_text, (320, 100))
        screen.blit(start_text, (320, 300))
        pygame.display.flip()


'''