import json
import matplotlib.pyplot as plt
from collections import defaultdict
import argparse

def main(input_file, x_axis, y_axis):
    # Load JSON data from a file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Initialize a dictionary to store the cumulative values for the y-axis
    axis_data = defaultdict(list)

    # Process each entry in the JSON data
    for entry in data:
        x_value = entry.get(f"@{x_axis}")
        y_value = entry.get(f"@{y_axis}")

        if x_value is not None and y_value is not None:
            try:
                x_value = float(x_value)
                y_value = float(y_value)
                axis_data[x_value].append(y_value)
            except ValueError:
                print(f"Invalid data: x_value or y_value cannot be converted to float. Skipping entry.")
    
    # Compute the mean of y-axis values for each x-axis value
    mean_y_values = {x: sum(values) / len(values) for x, values in axis_data.items()}

    # Sort data by x-axis values
    sorted_x_values = sorted(mean_y_values.keys())
    sorted_y_values = [mean_y_values[x] for x in sorted_x_values]

    # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_x_values, sorted_y_values, marker='o', linestyle='-', color='b')
    plt.xlabel(x_axis.replace('@', '').replace('_', ' ').title())
    plt.ylabel(y_axis.replace('@', '').replace('_', ' ').title())
    plt.title(f'{y_axis.replace("@", "").replace("_", " ").title()} vs {x_axis.replace("@", "").replace("_", " ").title()}')
    plt.grid(True)
    plt.savefig(f'{x_axis.replace("@", "")}_vs_{y_axis.replace("@", "")}.png')
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a plot from JSON data.')
    parser.add_argument('input_file', type=str, help='Path to the input JSON file.')
    parser.add_argument('x_axis', type=str, help='The parameter to use for the x-axis (e.g., @population_size).')
    parser.add_argument('y_axis', type=str, help='The parameter to use for the y-axis (e.g., @avg_solution_optimality).')

    args = parser.parse_args()
    main(args.input_file, args.x_axis, args.y_axis)

