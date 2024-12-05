import matplotlib.pyplot as plt

def visualize_optimal_transport_modes(locations, optimal_modes, title="Optimal Transport Modes Visualization"):
    """
    Visualizes the optimal transport modes for a journey.

    Parameters:
        locations (dict): Dictionary of location names and their coordinates (latitude, longitude).
                          Example: {"A": (lat, lon), "B": (lat, lon)}.
        optimal_modes (list): List of tuples containing the segments and transport modes in the form:
                              [(start, end, mode), ...].
                              Example: [("A", "B", "Bus"), ("B", "C", "Walking")].
        title (str): Title for the visualization graph (default is "Optimal Transport Modes Visualization").
    """
    # Set the size of the plot for better visibility
    plt.figure(figsize=(14, 9))  # Width and height of the figure in inches

    # Define colors for each transport mode to differentiate visually
    mode_colors = {
        "Bus": "blue",
        "Train": "green",
        "Bicycle": "orange",
        "Walking": "red"
    }

    # Plot each segment and use a distinct color for each transport mode
    for segment in optimal_modes:
        start_name, end_name, mode = segment  # Unpack the segment data
        start = locations[start_name]  # Get the coordinates for the start location
        end = locations[end_name]  # Get the coordinates for the end location

        # Assign a color based on the transport mode, default to gray if mode is unknown
        color = mode_colors.get(mode, "gray")

        # Plot the segment as a line connecting the start and end points
        plt.plot(
            [start[1], end[1]],  # Longitude values for the x-axis
            [start[0], end[0]],  # Latitude values for the y-axis
            marker="o",  # Add circular markers at each endpoint
            color=color,  # Line color based on transport mode
            linewidth=2  # Line thickness for better visibility
        )

    # Highlight Tarjan's home if it's included in the locations
    if "Tarjan" in locations:
        tarjan_coords = locations["Tarjan"]  # Get Tarjan's home coordinates
        plt.scatter(
            tarjan_coords[1], tarjan_coords[0],  # Longitude and latitude for the point
            color="green",  
            s=150,  # Size of the marker
            label="Tarjan's Home"  # Add label for legend
        )

    # Add text labels for all locations at their respective coordinates
    for name, coord in locations.items():
        plt.text(
            coord[1], coord[0],  # Longitude and latitude for the text position
            name,  # Name of the location
            fontsize=10,  # Font size for the text
            ha="center",  # Horizontal alignment of the text
            va="bottom"  # Vertical alignment of the text
        )

    # Create legend handles for transport modes
    mode_legend_handles = [
        plt.Line2D([0], [0], color=color, lw=2, label=mode)
        for mode, color in mode_colors.items()
    ]

    # Add a legend handle for Tarjan's home
    tarjan_home_handle = plt.Line2D(
        [0], [0], color="green", marker="o", linestyle="", markersize=9, label="Tarjan's Home"
    )

    # Combine transport modes and Tarjan's home handles into the legend
    mode_legend_handles.append(tarjan_home_handle)
    plt.legend(
        handles=mode_legend_handles,  # Legend entries
        loc="upper right",  # Position of the legend
        fontsize=10,  # Font size for the legend text
        title="Transport Modes and Locations"  # Title of the legend
    )

    # Add a title and axis labels to the plot
    plt.title(title, fontsize=18)  # Title with larger font size
    plt.xlabel("Longitude", fontsize=16)  # Label for x-axis
    plt.ylabel("Latitude", fontsize=16)  # Label for y-axis

    # Enable grid for better readability
    plt.grid(True, linestyle="--", alpha=0.6)  # Dashed grid lines with slight transparency

    # Display the plot
    plt.show()
