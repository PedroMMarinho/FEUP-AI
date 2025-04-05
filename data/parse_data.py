import json
import csv

def parse_alternate_player_turns_ordered_to_csv(json_file, csv_file):
    turn_starts = []
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            for game_data in data:
                is_first_player = None
                player_moves = game_data.get("player_moves")
                if player_moves:
                    for move in player_moves:
                        if len(move) == 4:
                            _, _, timestamp, current_player = move
                            if current_player != is_first_player:
                                turn_starts.append({'player': current_player, 'timestamp': timestamp})
                                is_first_player = current_player
                        else:
                            break

        # Write to CSV, maintaining the order of turn starts
        with open(csv_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Player', 'Turn Start Time (seconds)'])
            for turn in turn_starts:
                csv_writer.writerow([turn['player'], f"{turn['timestamp']:.6f}"])

    except FileNotFoundError as e:
        print(f"Error: File not found at {json_file}: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {json_file}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    json_file_path = "../src/json/saves.json"
    csv_file_path = "minimax_depth_3.csv"
    parse_alternate_player_turns_ordered_to_csv(json_file_path, csv_file_path)
    print(f"Player turn start times (in original order) written to {csv_file_path}")