import pytest
from shortest_path_calculation import calculate_total_distance, TransportMode, Segment
from compare_transport_modes import compare_transport_modes
from main import load_locations, load_transport_modes

from math import isclose

# Project data: locations and transport modes for testing
locations = {
    "Tarjan": (37.5219, 126.9245),
    "Bukhan-ro": (37.58, 126.9844),
    "Hannam-daero": (37.534, 127.0026),
    "Seongsu-daero": (37.5443, 127.0557),
    "Apgujeong-ro": (37.5219, 127.0411),
    "Cheongdam-ro": (37.5172, 127.0391),
    "Sinsa-daero": (37.5172, 127.0286),
    "Gangnam-daero": (37.4979, 127.0276),
    "Yangjae-daero": (37.4833, 127.0322),
    "Samseong-ro": (37.511, 127.059),
    "Jamsil-ro": (37.5133, 127.1028)
}

# Transport modes with their respective values
transport_modes = [
    TransportMode("Bus", 40, 2, 5),
    TransportMode("Train", 80, 5, 2),
    TransportMode("Bicycle", 15, 0, 1),
    TransportMode("Walking", 5, 0, 0)
]

# Path for journey testing
path = [
    "Tarjan",
    "Bukhan-ro",
    "Hannam-daero",
    "Seongsu-daero",
    "Apgujeong-ro",
    "Cheongdam-ro",
    "Sinsa-daero",
    "Gangnam-daero",
    "Yangjae-daero",
    "Samseong-ro",
    "Jamsil-ro"
]

# 1. Test calculate_total_distance
def test_calculate_total_distance():
    """
    Test the total distance calculation for a given path.
    """
    result = calculate_total_distance(path, locations)
    expected = 34.38  # Example real-world distance in km
    assert isclose(result, expected, rel_tol=0.01), f"Expected {expected}, got {result}"

# 2. Test compare_transport_modes
def test_compare_transport_modes():
    """
    Test the compare_transport_modes function for correct transport mode selection.
    """
    segment = Segment("Tarjan", locations["Tarjan"], "Bukhan-ro", locations["Bukhan-ro"], distance=0.8)
    result = compare_transport_modes(segment, transport_modes)

    # Assert that Bicycle is chosen for Minimum Cost, as it has 0 cost and is faster than Walking
    assert result["Minimum Cost"]["Mode"] == "Bicycle", "Bicycle should be chosen for minimum cost as it is faster than Walking"

    # Assert that Walking is chosen for Minimum Time for distances under 1 km
    assert result["Minimum Time"]["Mode"] == "Walking", "Walking should be chosen for minimum time for very short distances"

# 3. Test load_locations with actual file
def test_load_locations():
    """
    Test loading locations from a CSV file.
    """
    result = load_locations("locations.csv")
    assert result == locations, f"Loaded locations do not match expected locations"

# 4. Test load_transport_modes with actual file
def test_load_transport_modes():
    """
    Test loading transport modes from a CSV file.
    """
    result = load_transport_modes("transport_modes.csv")
    assert len(result) == len(transport_modes), "Mismatch in number of transport modes"
    for i in range(len(result)):
        assert result[i].name == transport_modes[i].name, f"Mismatch in transport mode names: {result[i].name}"

# 5. Test TransportMode initialization
def test_transport_mode():
    """
    Test the initialization of a TransportMode object.
    """
    bus = TransportMode("Bus", 40, 2, 5)
    assert bus.name == "Bus", "TransportMode name should be Bus"
    assert bus.speed_kmh == 40, "Speed should be 40 km/h"
    assert bus.cost_per_km == 2, "Cost per km should be 2"

# 6. Test Segment initialization
def test_segment():
    """
    Test the initialization of a Segment object.
    """
    segment = Segment("Tarjan", locations["Tarjan"], "Bukhan-ro", locations["Bukhan-ro"], distance=8.34)
    assert segment.start_name == "Tarjan", "Segment start should be Tarjan"
    assert segment.end_name == "Bukhan-ro", "Segment end should be Bukhan-ro"
    assert segment.distance == 8.34, "Segment distance should be 8.34 km"

# 7. Test error handling for load_locations
def test_load_locations_error(capsys):
    """
    Test error handling for missing location files.
    """
    load_locations("missing.csv")
    captured = capsys.readouterr()  # Capture stdout and stderr
    assert "Error: The file missing.csv was not found." in captured.out
