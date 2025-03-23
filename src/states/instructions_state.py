import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BUTTONS_HEIGHT, BUTTONS_WIDTH, FONT
from config import LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, CADET_BLUE, WHITE, BLACK
from states.state import State
from ui import draw_button, draw_text
from button import ClickButton

class InstructionsState(State):

    def __init__(self, game):
        super().__init__(game)
        self.buttons = []

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.click(event) 

    def draw(self):
        screen = self.game.screen
        font = pygame.font.SysFont(None, 50)  # Regular font for content
        small_font = pygame.font.SysFont(None, 30)

        # Title
        title_text = "Game Instructions"
        draw_text(screen, title_text, font, STEEL_BLUE, SCREEN_WIDTH // 2 - font.size(title_text)[0] // 2, 40)

        # Instructions box
        instructions_text = [
            ("Objective", "Be the first player to remove three of your rings from the board by forming rows of five markers of your color."),
            ("Setup", "Each player starts with five rings.\nPlayers alternate placing their rings on the board until all ten are placed."),
            ("Gameplay", "Move: On your turn, place a marker in one of your rings, then move that ring in a straight line:\nYou can move over empty spaces or jump over a line of markers (flipping the jumped markers).\nYou cannot jump over rings.\nRows: If you form a straight row of five markers of your color, remove the row and one of your rings.\nOpponent's Rows: If you create a row for your opponent, they remove it and one of their rings.\nWinning: The first player to remove three of their rings wins."),
            ("Key Points", "Think ahead and anticipate marker flips.\nDisrupt your opponent's potential rows.\nRing removal limits your future moves.\nIt is the third row that counts.")
        ]

        y_offset = 120  # Start drawing the instructions below the title

        for topic, content in instructions_text:
            # Draw the topic with STEEL_BLUE color and bold style
            draw_text(screen, topic, font, STEEL_BLUE, SCREEN_WIDTH // 2 - font.size(topic)[0] // 2, y_offset)
            y_offset += font.get_height() + 20  # Add space after topic

            # Draw the content in WHITE with a slight off-white background (CADET_BLUE)
            lines = content.splitlines()
            for line in lines:
                draw_text(screen, line.strip(), small_font, BLACK, (SCREEN_WIDTH - small_font.size(line.strip())[0]) // 2, y_offset)
                y_offset += small_font.get_height() + 10  # Add space between lines
        
        # Back button to return to the main menu (centered at the bottom)
        self.buttons.append(  
                      ClickButton("Back", 
                        BUTTONS_WIDTH // 6, y_offset -20,
                        BUTTONS_HEIGHT, BUTTONS_WIDTH,
                        FONT,
                        LIGHT_CYAN, STEEL_BLUE, POWER_BLUE, WHITE, CADET_BLUE, CADET_BLUE,
                        action=lambda: self.game.go_back())
                    )

        for button in self.buttons:
            button.draw(screen)