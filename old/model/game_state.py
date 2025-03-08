from enum import Enum

class GameState(Enum):
    MAIN_MENU = "main_menu"
    INSTRUCTIONS_MENU = "instructions_menu"
    GAME = "game"
    AI_AI = "ai_ai"
    AI_HUMAN = "ai_human"
    HUMAN_HUMAN = "human_human"
    EXIT = "exit"
    GAME_MODE_SELECTION = "game_mode_selection"
