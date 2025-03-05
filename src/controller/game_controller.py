from model.board import Board
from view.board_view import BoardView
import pygame
from model.game_state import GameState
from view.menu_view import render_game_screen

def game_screen(screen, mode, botDifficulty1=None, botDifficulty2=None, pieces=None):
    board = Board()
    view = BoardView(board)
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