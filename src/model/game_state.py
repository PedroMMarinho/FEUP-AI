from enum import Enum

class GameState(Enum):
    MAIN_MENU = "main_menu"
    INSTRUCTIONS_MENU = "instructions_menu"
    GAME = "game"
    EXIT = "exit"
    SETTINGS_MENU = "settings_menu"