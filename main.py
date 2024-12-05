import time
import csv
import re
from colorama import Fore, Style, init
from calculate_journey import calculate_journey
from shortest_path_calculation import genetic_algorithm, TransportMode
from journey_visualization import visualize_optimal_transport_modes
from collections import Counter
from exceptions_and_decorators import execution_time_decorator, logging_decorator, error_handling_decorator

# Initialize colorama for colored console output
init(autoreset=True)

# Load location coordinates from a CSV file
@logging_decorator
@error_handling_decorator
def load_locations(file_path):
    """
    Loads location data from a CSV file, validating each row for proper format.

    Parameters:
        file_path (str): Path to the CSV file containing location data.

    Returns:
        dict: Dictionary of location names and their coordinates (latitude, longitude).
    """
    locations = {}
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)  # Automatically handles headers
            for row in reader:
                match = re.match(r"^([\w\s-]+),([-+]?\d*\.\d+),([-+]?\d*\.\d+)$",
                                 f"{row['Name']},{row['Latitude']},{row['Longitude']}")
                if match:
                    name, latitude, longitude = match.groups()
                    locations[name] = (float(latitude), float(longitude))
                else:
                    print(Fore.RED + f"Invalid line in locations file: {row}")
    except FileNotFoundError:
        print(Fore.RED + f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(Fore.RED + f"An error occurred while reading the file {file_path}: {e}")
    return locations

# Load transport modes from a CSV file
@logging_decorator
@error_handling_decorator
def load_transport_modes(file_path):
    """
    Loads transport mode data from a CSV file, validating each row for proper format.

    Parameters:
        file_path (str): Path to the CSV file containing transport modes.

    Returns:
        list: List of TransportMode objects.
    """
    transport_modes = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)  # Automatically handles headers
            for row in reader:
                try:
                    name = row['Name']
                    speed_kmh = float(row['Speed_kmh'])
                    cost_per_km = float(row['Cost_per_km'])
                    transfer_time_min = int(row['Transfer_Time_min'])

                    # Append only valid data
                    transport_modes.append(TransportMode(name, speed_kmh, cost_per_km, transfer_time_min))
                except (ValueError, KeyError):
                    print(Fore.RED + f"Invalid line in transport modes file: {row}")
    except FileNotFoundError:
        print(Fore.RED + f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(Fore.RED + f"An error occurred while reading the file {file_path}: {e}")
    return transport_modes

# Main function to run the TarjanPlanner application
@execution_time_decorator
@error_handling_decorator
def main():
    """
    Main function for TarjanPlanner. Handles data loading, route optimization,
    user interaction, and results visualization.
    """
    # Start timing the program
    #program_start = time.time()

    print("\n" + Fore.GREEN + Style.BRIGHT + "*" * 73)
    print(Style.BRIGHT + Fore.CYAN + "\tWELCOME TO TarjanPlanner for Route Optimization in Seoul")
    print(Fore.GREEN + Style.BRIGHT + "*" * 73)

    # Load location and transport mode data
    locations = load_locations("locations.csv")
    transport_modes = load_transport_modes("transport_modes.csv")

    try:
        # Calculate the shortest route using a genetic algorithm
        total_distance, shortest_path = genetic_algorithm(locations, seed=120)

        # Prompt the user to choose optimization criteria
        criteria_mapping = {
            "1": "Minimum Cost",
            "2": "Minimum Time",
            "3": "Both Cost and Time"
        }

        chosen_criterion = None
        while not chosen_criterion:
            print(Fore.YELLOW + "\nPlease select optimization criteria or press Enter to exit:")
            print(Fore.CYAN + "1. Minimum Cost")
            print(Fore.CYAN + "2. Minimum Time")
            print(Fore.CYAN + "3. Both Time & Cost")
            choice = input(Fore.GREEN + "Please enter your choice (1/2/3) or hit Enter to exit: ").strip()

            if not choice:  # Exit if the user presses Enter without input
                print(Fore.CYAN + "Exiting program. Goodbye!\n")
                exit(0)

            # Validate user input using regex
            if re.match(r"^[123]$", choice):  
                chosen_criterion = criteria_mapping[choice]
            else:
                print(Fore.RED + "Invalid choice. Please enter 1, 2, or 3.")

        print(Fore.GREEN + f"\nYou selected: Optimize for: {Fore.YELLOW + Style.BRIGHT}{chosen_criterion}")

        # Optimize transport modes for the journey
        journey_results, journey_distance = calculate_journey(locations, transport_modes, shortest_path)

        print(Fore.GREEN + Style.BRIGHT + f"\nOptimal Route Summary ({chosen_criterion}):")
        total_cost = 0
        total_time = 0
        cumulative_distance = 0
        optimal_modes = []  # Store transport modes for visualization
        transport_mode_counter = Counter()

        for result in journey_results:
            mode_info = result[chosen_criterion]
            segment = result["Segment"].split(" -> ")
            cumulative_distance += result["Distance"]
            transport_mode_counter[mode_info["Mode"]] += 1
            optimal_modes.append((segment[0], segment[1], mode_info["Mode"]))

            total_cost += mode_info["Cost"]
            total_time += mode_info["Time"]

            segment_output = (
                f"{result['Segment']} (Mode: {mode_info['Mode']}, Cost: {mode_info['Cost']:.2f} KRW, "
                f"Time: {mode_info['Time']:.2f} hours, Cumulative Distance: {cumulative_distance:.2f} km)"
            )
            print("\n" + Style.BRIGHT + Fore.CYAN + segment_output)

        # Print final summary
        print(Fore.GREEN + Style.BRIGHT + "-" * 73)
        print(Fore.GREEN + f"Total shortest distance for the journey: {Fore.CYAN}{journey_distance:.2f} km")
        #print(Fore.GREEN + f"Shortest path (excluding Tarjan's home): {Fore.CYAN} 26.04 km")        
        print(Fore.GREEN + f"Total Cost: {Fore.CYAN}{total_cost:.2f} KRW")
        print(Fore.GREEN + f"Total Time: {Fore.CYAN}{total_time:.2f} hours")
        print(Fore.GREEN + f"Average Cost per km: {Fore.CYAN}{total_cost / journey_distance:.2f} KRW/km")
        print(Fore.GREEN + f"Average Time per km: {Fore.CYAN}{total_time / journey_distance:.2f} hours/km")
        most_frequent_mode = transport_mode_counter.most_common(1)[0]
        print(Fore.GREEN + f"Most Frequently Used Transport Mode: {Fore.CYAN}{most_frequent_mode[0]} "
              f"({most_frequent_mode[1]} segments)")
        print(Fore.GREEN + Style.BRIGHT + "-" * 73)
        # End timing before visualization
        #program_end = time.time()
        #elapsed_time = program_end - program_start
        #print(Fore.CYAN + f"\nProgram execution time including user interaction: {elapsed_time:.2f} seconds")

        #Visualize the optimal transportation route****************
        visualize_optimal_transport_modes(
            locations,
            optimal_modes,
            title="Tarjan's Transportation Network in Seoul with Starting Location"
        )

      
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}")

# Run the main function
main(suppress_output=True)  # Suppress final wrapper output for cleaner logs
