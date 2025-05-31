import json


def load_boards(file):
    with open(file, "r") as f:
        return json.load(f)

def save_boards(file,boards):
    """Saves the current board list to the JSON file."""
    with open(file, "w") as f:
            json.dump(boards, f, indent=4)


def save_game(file,state):
    with open(file, "w") as f:
            json.dump(state, f, indent=4)

def load_game(file):
    with open(file, "r") as f:
        return json.load(f)
    
def clear_game(file):
    with open(file, 'w') as file:
        file.truncate(0)
