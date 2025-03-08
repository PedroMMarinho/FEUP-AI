import pygame
from enum import Enum
from model.board import Board, BoardSpaceType
from view.board_view import BoardView
from model.game_state import GameState
from view.menu_view import render_game_screen

class GamePhase (Enum):
    PREP_PHASE = 0
    PLAYING_PHASE = 1
    END = 2

def game_screen(screen, mode, botDifficulty1=None, botDifficulty2=None, pieces=None):
    board = Board()
    view = BoardView(board)
    player = 'white'
    game_phase = GamePhase.PREP_PHASE 
    print(f"Mode {mode}" )
    print(f"Bot1 {botDifficulty1}")
    print(f"Bot2 {botDifficulty2}")
    print(f"Pieces {pieces}")

    while True:
        render_game_screen(screen, board, view)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return GameState.MAIN_MENU
        
        match mode:
            case "human_human":
                if game_phase == GamePhase.PREP_PHASE:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        
                    if player == 'white' :
                        board.placePiece((x,y),BoardSpaceType.PLAYER1_RING)
                    elif player == 'black':
                        board.placePiece((x,y),BoardSpaceType.PLAYER2_RING)
                        
            
