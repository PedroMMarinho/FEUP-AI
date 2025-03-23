import random
import json
import os

# Function to load the boards from the JSON file
def load_boards(filename='src/json/boards.json'):
    if not os.path.exists(filename):
        return {}  # Return an empty dictionary if the file does not exist
    with open(filename, 'r') as file:
        return json.load(file)

# Function to create a random board with constraints
def create_random_board(default_board):
    new_board = []
    count_3, count_4 = 0, 0  # Counters for 3s and 4s

    for row in default_board:
        new_row = []
        for val in row:
            if val == 0:
                possible_values = [0, 1, 2]

                # Only allow 3 if there are fewer than 5
                if count_3 < 5:
                    possible_values.append(3)
                
                # Only allow 4 if there are fewer than 5
                if count_4 < 5:
                    possible_values.append(4)

                chosen_value = random.choice(possible_values)

                # Update counters
                if chosen_value == 3:
                    count_3 += 1
                elif chosen_value == 4:
                    count_4 += 1

                new_row.append(chosen_value)
            else:
                new_row.append(val)
        new_board.append(new_row)

    return new_board

# Function to save the new board with an incremented name
def save_board_to_json(board, filename='src/json/boards.json'):
    data = load_boards(filename)
    
    # Find the next available board name
    board_number = 1
    while f'Board{board_number}' in data:
        board_number += 1
    
    # Add the new board
    data[f'Board{board_number}'] = {'layout': board}
    
    # Save back to the JSON file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Load the boards
boards_data = load_boards()

# Load the default board
default_board = boards_data.get('Default', {}).get('layout', [])

if default_board:
    # Create the random board
    random_board = create_random_board(default_board)

    # Save the new board with an incremented name
    save_board_to_json(random_board)
    print(f"New board added as 'Board{len(boards_data)}'")
else:
    print("Error: Default board not found in JSON file.")
