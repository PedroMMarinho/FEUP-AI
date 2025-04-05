import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Specify the filename
filename = "data/montecarlo_vs_minimax.csv"

try:
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(filename)

    # Create a new column combining Winner and Depth for Minimax only
    df['Winner_Depth'] = df.apply(
        lambda row: f"{row['Winner']} (Depth {row['Depth']})"
        if row['Winner'] == 'Minimax'
        else row['Winner'],
        axis=1
    )

    # Set the dark mode style using seaborn
    plt.style.use('dark_background')
    sns.set_palette("viridis")  # Color palette suitable for dark mode

    # Create figure and axes
    plt.figure(figsize=(12, 7))
    
    # Get all unique time values
    all_times = sorted(df['Avg Turn Time'].unique())
    
    # Function to determine the order priority
    def get_order_priority(winner_depth):
        if 'MonteCarlo' in winner_depth:
            return 0
        elif 'Minimax' in winner_depth:
            # Extract depth number
            try:
                depth = int(winner_depth.split('Depth ')[1].strip(')'))
                return 1 + depth  # Return 2, 3, 4 etc. based on depth
            except:
                return 1
        elif 'Draw' in winner_depth:
            return 999  # Put Draw at the end
        else:
            return 500  # Other cases
    
    # Custom colormap
    colors = plt.cm.viridis(np.linspace(0, 1, 10))  # Generate 10 colors from viridis
    color_map = {
        'MonteCarlo': colors[0],
        'Draw': colors[-1]
    }
    # Assign colors for Minimax depths
    for i in range(1, 6):  # Assuming depths 1-5
        color_map[f'Minimax (Depth {i})'] = colors[i]
    
    # Initialize positions for legend handles
    legend_handles = []
    legend_labels = []
    seen_winners = set()
    
    # Initialize positions for x-ticks
    x_positions = []
    x_labels = []
    bar_count = 0
    
    # Loop through each time value
    for time_val in all_times:
        # Filter data for this time value
        time_data = df[df['Avg Turn Time'] == time_val]
        
        # Get unique winners for this time and sort them according to priority
        winners_for_time = sorted(
            time_data['Winner_Depth'].unique(),
            key=get_order_priority
        )
        
        # If there are winners for this time
        if len(winners_for_time) > 0:
            # Add the time label to x-axis
            time_position = bar_count + (len(winners_for_time) - 1) / 2
            x_positions.append(time_position)
            x_labels.append(time_val)
            
            # For each winner in this time, create a bar
            for winner in winners_for_time:
                # Count occurrences
                count = len(time_data[time_data['Winner_Depth'] == winner])
                
                # Determine color
                if winner in color_map:
                    color = color_map[winner]
                else:
                    # Default color for unknown categories
                    color = colors[5]
                
                # Plot bar with appropriate color
                bar = plt.bar(
                    bar_count,
                    count,
                    width=0.8,
                    color=color
                )
                
                # Add to legend if not seen before
                if winner not in seen_winners:
                    legend_handles.append(bar[0])
                    legend_labels.append(winner)
                    seen_winners.add(winner)
                
                # Increment bar position
                bar_count += 1
            
            # Add a gap between time groups
            bar_count += 1
    
    # Set x-ticks at the center of each group
    plt.xticks(x_positions, x_labels, rotation=45, ha='right')
    
    # Add legend
    plt.legend(legend_handles, legend_labels, title="Winner", loc='upper right')
    
    # Add labels and title
    plt.xlabel("Avg Turn Execution Time (seconds)", fontsize=12)
    plt.ylabel("Number of Games")
    plt.title("Number of Games by Execution Time and Winner (Minimax Depth)")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Ensure y-axis ticks are integers
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    # Show the plot
    plt.tight_layout()
    plt.savefig("data/montecarlo_vs_minimax_plot.png")  
    plt.show()

except FileNotFoundError:
    print(f"Error: CSV file not found at {filename}")
except Exception as e:
    print(f"An error occurred: {e}")