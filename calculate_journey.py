from shortest_path_calculation import calculate_total_distance, haversine, Segment
from compare_transport_modes import compare_transport_modes

def calculate_journey(locations, transport_modes, journey_path):
    """
    Calculates the journey details including transport mode optimization for each segment.

    Parameters:
        locations (dict): Dictionary of location names and their coordinates (latitude, longitude).
                          Example: {"A": (lat, lon), "B": (lat, lon)}.
        transport_modes (list): List of available TransportMode objects, each representing a mode of transportation.
                                Example: [TransportMode("Bus", speed_kmh=50, cost_per_km=1.5, transfer_time_min=5)].
        journey_path (list): List of location names in the order of travel.
                             Example: ["A", "B", "C"].

    Returns:
        results (list): A list of dictionaries containing segment-wise journey details, including:
                        - Segment name (start -> end).
                        - Minimum Cost, Minimum Time, and Both Cost and Time results.
                        - Distance for the segment.
        total_distance (float): The total distance for the entire journey in kilometers.
    """
    results = []  # List to store detailed results for each segment
    total_distance = calculate_total_distance(journey_path, locations)  # Calculate total journey distance

    # Iterate through the journey path to process each segment
    for i in range(len(journey_path) - 1):
        start_name = journey_path[i]  # Starting location name
        end_name = journey_path[i + 1]  # Ending location name
        start_coords = locations[start_name]  # Coordinates of the starting location
        end_coords = locations[end_name]  # Coordinates of the ending location

        # Calculate the distance between the two locations using the haversine formula
        distance = haversine(start_coords[0], start_coords[1], end_coords[0], end_coords[1])

        # Create a Segment object to represent the journey between the two locations
        segment = Segment(start_name, start_coords, end_name, end_coords, distance=distance)

        # Compare transport modes for the segment, using custom logic for optimization
        segment_results = compare_transport_modes(segment, transport_modes, use_custom_logic=True)

        # Append the segment results to the results list
        results.append({
            "Segment": f"{start_name} -> {end_name}",  # Name of the segment
            "Minimum Cost": segment_results["Minimum Cost"],  # Best option for minimum cost
            "Minimum Time": segment_results["Minimum Time"],  # Best option for minimum time
            "Both Cost and Time": segment_results["Both Cost and Time"],  # Best balanced option
            "Distance": distance  # Distance for the segment
        })

    return results, total_distance  # Return the segment-wise results and total distance
