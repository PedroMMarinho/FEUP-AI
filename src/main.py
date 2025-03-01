import shutil
import os

# Remove __pycache__ directories before running the game
for root, dirs, files in os.walk(".", topdown=False):
    for name in dirs:
        if name == "__pycache__":
            shutil.rmtree(os.path.join(root, name))

from game import run_game

if __name__ == "__main__":
    run_game()