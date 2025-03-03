from enum import Enum

class GameState(Enum):
    MAIN_MENU = "main_menu"
    INSTRUCTIONS_MENU = "instructions_menu"
    GAME = "game"
    AI_AI = "AIvsAI"
    AI_HUMAN = "AIvsHuman"
    HUMAN_HUMAN = "HumanvsHuman"
    EXIT = "exit"
    GAME_MODE_SELECTION = "game_mode_selection"
