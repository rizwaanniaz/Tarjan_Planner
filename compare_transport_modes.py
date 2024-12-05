import math

def compare_transport_modes(segment, transport_modes, use_custom_logic=False):
    """
    Compares all transport modes for a given segment and returns the best options.

    Parameters:
        segment (Segment): The journey segment to evaluate.
        transport_modes (list): List of available TransportMode objects.
        use_custom_logic (bool): Whether to use custom logic for both cost and time criteria.

    Returns:
        dict: Dictionary with details of the best options for:
              - Minimum Cost: The transport mode with the lowest cost.
              - Minimum Time: The transport mode with the shortest travel time.
              - Both Cost and Time: An optimal balance between cost and time.
    """
    # Variables to store the best transport modes for each criterion
    best_cost = None
    best_time = None
    best_cost_time = None

    if use_custom_logic:
        # Apply custom logic for "Both Cost and Time" optimization
        if segment.distance <= 5:
            # For short distances (<= 5 km), recommend Bicycle with a fixed calculation
            best_cost_time = {
                "Mode": "Bicycle",
                "Cost": 0.0,
                "Time": segment.distance / 15 + (1 / 60)  # Travel time + transfer time
            }
        else:
            # For longer distances, recommend Bus with fixed cost and time calculations
            best_cost_time = {
                "Mode": "Bus",
                "Cost": segment.distance * 2,  # Example: Bus cost = distance * 2 currency units
                "Time": segment.distance / 40 + (5 / 60)  # Travel time + transfer time
            }

    # Evaluate each transport mode
    for mode in transport_modes:
        # Custom logic for Minimum Time: Force "Walking" for distances < 1 km
        if segment.distance < 1 and mode.name == "Walking":
            # Recommend walking for very short distances
            best_time = {"Mode": "Walking", "Cost": 0.0, "Time": segment.distance / 5}
            continue  # Skip remaining calculations for this mode

        # Calculate cost and time for the current transport mode
        cost = mode.cost_per_km * segment.distance  # Total cost based on distance
        time = segment.distance / mode.speed_kmh  # Travel time in hours
        total_time = time + (mode.transfer_time_min / 60)  # Add transfer time in hours

        # Determine the best option for Minimum Cost
        if best_cost is None or cost < best_cost["Cost"]:
            best_cost = {"Mode": mode.name, "Cost": cost, "Time": total_time}

        # Determine the best option for Minimum Time
        if best_time is None or total_time < best_time["Time"]:
            best_time = {"Mode": mode.name, "Cost": cost, "Time": total_time}

        # Update "Both Cost and Time" if custom logic is not used
        if not use_custom_logic:
            if best_cost_time is None or (cost + total_time) < (best_cost_time["Cost"] + best_cost_time["Time"]):
                best_cost_time = {"Mode": mode.name, "Cost": cost, "Time": total_time}

    # Return the best transport modes for each criterion
    return {
        "Minimum Cost": best_cost,
        "Minimum Time": best_time,
        "Both Cost and Time": best_cost_time
    }
