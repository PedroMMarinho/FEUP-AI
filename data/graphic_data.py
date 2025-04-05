import matplotlib.pyplot as plt
import csv
from collections import defaultdict

def plot_minimax_depth_times(csv_file, save_as="minimax_depth_plot.png"):
    """
    Reads a CSV file with player turn start times and plots the average time
    for different minimax depths. The CSV is expected to have filenames
    containing depth information (e.g., minimax_depth1.csv). Saves the plot
    as an image.

    Args:
        csv_file (str): The path to the CSV file. The filename should
                        contain "depth_1", "depth_2", or "depth_3".
        save_as (str, optional): The filename to save the plot as.
                                 Defaults to "minimax_depth_plot.png".
    """
    depth_times = defaultdict(list)
    depth = None

    if "depth_1" in csv_file.lower():
        depth = 1
    elif "depth_2" in csv_file.lower():
        depth = 2
    elif "depth_3" in csv_file.lower():
        depth = 3
    else:
        print(f"Warning: Could not determine depth from filename '{csv_file}'. Skipping.")
        return

    try:
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            total_time = 0
            count = 0
            for row in reader:
                try:
                    time = float(row[1])
                    total_time += time
                    count += 1
                except ValueError:
                    print(f"Warning: Skipping invalid time value '{row[1]}' in '{csv_file}'.")
                except IndexError:
                    print(f"Warning: Skipping row with insufficient data in '{csv_file}'.")

            if count > 0:
                average_time = total_time / count
                depth_times[depth].append(average_time)
            else:
                print(f"Warning: No valid time data found for depth {depth} in '{csv_file}'.")

    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_file}'.")
    except Exception as e:
        print(f"An error occurred while reading '{csv_file}': {e}")

    return depth_times, depth  # Return depth as well

if __name__ == "__main__":
    csv_files = ["data/minimax_depth_1.csv", "data/minimax_depth_2.csv", "data/minimax_depth_3.csv"]
    all_depth_averages = defaultdict(float)

    plt.style.use('dark_background')
    plt.figure(figsize=(8, 6))

    for file in csv_files:
        depth_averages, depth = plot_minimax_depth_times(file)
        for d, avg_times in depth_averages.items():
            if avg_times:
                all_depth_averages[d] = sum(avg_times) / len(avg_times)

    if all_depth_averages:
        depths = sorted(all_depth_averages.keys())
        average_times = [all_depth_averages[d] for d in depths]

        plt.plot(depths, average_times, marker='o', linestyle='-', color='cyan')
        plt.xlabel("Minimax Depth", color='white')
        plt.ylabel("Average Turn Time (seconds)", color='white')
        plt.title("Average Turn Start Time vs. Minimax Depth", color='white')
        plt.xticks(depths, color='white')
        plt.yticks(color='white')
        plt.grid(True, color='gray', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("minimax_depth_plot.png")  # Save the plot as 'minimax_depth_plot.png'
        plt.show()
        print("Plot saved as minimax_depth_plot.png")
    else:
        print("No data found to plot.")