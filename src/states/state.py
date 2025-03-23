import pygame

class State:
    def __init__(self, game):
        self.game = game  
        self.buttons = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.exit_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click(event)

            self.handle_child_events(event)

    def handle_child_events(self,event):
        pass

    def draw(self):
        for button in self.buttons:
            button.draw(self.game.screen)

