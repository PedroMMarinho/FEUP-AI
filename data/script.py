import csv
from collections import defaultdict

def calculate_average_depth_times(csv_files, output_csv_file):
    """
    Reads multiple CSV files with player turn start times, calculates the
    average time for each minimax depth (inferred from the filename), and
    writes these averages to a new CSV file.

    Args:
        csv_files (list): A list of paths to the CSV files (e.g.,
                          ["minimax_depth1.csv", "minimax_depth2.csv"]).
        output_csv_file (str): The path to the new CSV file where the
                               average times will be stored.
    """
    depth_total_times = defaultdict(float)
    depth_counts = defaultdict(int)
    depth_averages = {}

    for csv_file in csv_files:
        depth = None
        if "depth_1" in csv_file.lower():
            depth = 1
        elif "depth_2" in csv_file.lower():
            depth = 2
        elif "depth_3" in csv_file.lower():
            depth = 3

        if depth is not None:
            try:
                with open(csv_file, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip the header row
                    for row in reader:
                        try:
                            time = float(row[1])
                            depth_total_times[depth] += time
                            depth_counts[depth] += 1
                        except (ValueError, IndexError):
                            print(f"Warning: Skipping invalid data in '{csv_file}'.")
            except FileNotFoundError:
                print(f"Error: CSV file not found at '{csv_file}'.")
            except Exception as e:
                print(f"An error occurred while reading '{csv_file}': {e}")
        else:
            print(f"Warning: Could not determine depth from filename '{csv_file}'. Skipping.")

    # Calculate averages
    for depth, total_time in depth_total_times.items():
        if depth_counts[depth] > 0:
            depth_averages[depth] = total_time / depth_counts[depth]

    # Write averages to the new CSV file
    try:
        with open(output_csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Minimax Depth', 'Average Turn Start Time (seconds)'])
            for depth in sorted(depth_averages.keys()):
                writer.writerow([depth, f"{depth_averages[depth]:.6f}"])
        print(f"Average depth times written to '{output_csv_file}'")
    except Exception as e:
        print(f"An error occurred while writing to '{output_csv_file}': {e}")

if __name__ == "__main__":
    input_csv_files = ["data/minimax_depth_1.csv", "data/minimax_depth_2.csv", "data/minimax_depth_3.csv"]
    output_csv_file = "data/average_depth_times.csv"
    calculate_average_depth_times(input_csv_files, output_csv_file)