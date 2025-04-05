import csv
import json
import os

def analyze_game_data(json_data):
    """
    Analyzes the game data to determine the winner for each turn based on the number of rings.

    Args:
        json_data: A Python list containing the game data (loaded from JSON).

    Returns:
        A list of dictionaries, where each dictionary represents a turn and contains
        'Turn Time', 'Winner', and 'Depth'.
    """
    results = []

    for turn in json_data:
        turn_time = turn.get("turn_time", 0.6)  # Default to 0.05 if not present
        rings = turn.get("rings", {})
        depth = 2  # Depth is always 1 in this case

        player1_rings = rings.get("Player 1")
        player2_rings = rings.get("Player 2")

        winner = ""
        if player1_rings is not None and player2_rings is not None:
            if player1_rings < player2_rings:
                winner = "MonteCarlo"
            elif player2_rings < player1_rings:
                winner = "Minimax"
            else:
                winner = "Draw"
        else:
            winner = "Incomplete Data"  # Handle cases where ring data is missing

        results.append({"Avg Turn Time": turn_time, "Winner": winner, "Depth": depth})

    return results

def write_to_csv(data, filename="data/montecarlo_vs_minimax.csv"):
    """
    Writes the analyzed game data to a CSV file, appending if the file exists.

    Args:
        data: A list of dictionaries containing the game results.
        filename: The name of the CSV file to create or append to.
    """
    fieldnames = ["Avg Turn Time", "Winner", "Depth"]
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Only write header if the file is new
        writer.writerows(data)

if __name__ == "__main__":
    # Construct the full file path
    json_file_path = os.path.join("src", "json", "saves.json")

    try:
        # Read the JSON data from the file
        with open(json_file_path, 'r') as f:
            json_data = json.load(f)

        # Analyze the game data
        analysis_results = analyze_game_data(json_data)

        # Write the results to a CSV file
        write_to_csv(analysis_results)

        print("CSV file 'game_results.csv' has been created.")
        print("Contents of the CSV file:")
        with open("data/montecarlo_vs_minimax.csv", 'r') as f:
            print(f.read())

    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")