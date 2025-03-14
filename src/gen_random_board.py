import json
import random
import os

BOARDS_FILE = "src/boards.json"

def generate_valid_board():
    """Generates a board where 0s are replaced with random values from 1 to 4."""
    base_board = [
        [-1,-1,-1,-1,0,-1,0,-1,-1,-1,-1], 
        [-1,-1,-1,0,-1,0,-1,0,-1,-1,-1], 
        [-1,-1,0,-1,0,-1,0,-1,0,-1,-1], 
        [-1,0,-1,0,-1,0,-1,0,-1,0,-1], 
        [-1,-1,0,-1,0,-1,0,-1,0,-1,-1], 
        [-1,0,-1,0,-1,0,-1,0,-1,0,-1],
        [0,-1,0,-1,0,-1,0,-1,0,-1,0],
        [-1,0,-1,0,-1,0,-1,0,-1,0,-1],
        [0,-1,0,-1,0,-1,0,-1,0,-1,0],
        [-1,0,-1,0,-1,0,-1,0,-1,0,-1],
        [0,-1,0,-1,0,-1,0,-1,0,-1,0],
        [-1,0,-1,0,-1,0,-1,0,-1,0,-1], 
        [0,-1,0,-1,0,-1,0,-1,0,-1,0], 
        [-1,0,-1,0,-1,0,-1,0,-1,0,-1], 
        [-1,-1,0,-1,0,-1,0,-1,0,-1,-1], 
        [-1,0,-1,0,-1,0,-1,0,-1,0,-1], 
        [-1,-1,0,-1,0,-1,0,-1,0,-1,-1], 
        [-1,-1,-1,0,-1,0,-1,0,-1,-1,-1], 
        [-1,-1,-1,-1,0,-1,0,-1,-1,-1,-1]
    ]
    
    for row in range(len(base_board)):
        for col in range(len(base_board[row])):
            if base_board[row][col] == 0:
                base_board[row][col] = random.randint(0, 4)
    
    return base_board

def add_board_to_json():
    """Loads boards.json, adds a new generated board with a proper name, and saves it back."""
    boards = []

    # Check if the file exists and load existing data
    if os.path.exists(BOARDS_FILE):
        with open(BOARDS_FILE, "r", encoding="utf-8") as file:
            try:
                boards = json.load(file)
            except json.JSONDecodeError:
                print("Warning: boards.json was empty or invalid. Starting fresh.")

    # Determine the new board's name
    existing_board_numbers = [
        int(board["name"].replace("Board ", "")) 
        for board in boards if board["name"].startswith("Board ")
    ]
    new_board_number = max(existing_board_numbers, default=0) + 1
    new_board_name = f"Board {new_board_number}"

    # Generate and add a new board
    new_board = {
        "name": new_board_name,
        "layout": generate_valid_board()
    }
    boards.append(new_board)

    # Save back to JSON file
    with open(BOARDS_FILE, "w", encoding="utf-8") as file:
        json.dump(boards, file, indent=4)

    print(f"New board '{new_board_name}' added successfully!")

# Example usage:
add_board_to_json()
