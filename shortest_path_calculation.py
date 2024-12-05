import random
from math import radians, sin, cos, sqrt, atan2
from exceptions_and_decorators import execution_time_decorator, error_handling_decorator

# Class to define a transport mode with attributes for speed, cost, and transfer time
class TransportMode:
    def __init__(self, name, speed_kmh, cost_per_km, transfer_time_min):
        """
        Initialize a transport mode.
        :param name: Name of the transport mode (e.g., "Car", "Train").
        :param speed_kmh: Average speed in kilometers per hour.
        :param cost_per_km: Cost per kilometer in chosen currency.
        :param transfer_time_min: Time required for transfer in minutes.
        """
        self.name = name
        self.speed_kmh = speed_kmh
        self.cost_per_km = cost_per_km
        self.transfer_time_min = transfer_time_min

# Class to represent a segment of a journey
class Segment:
    def __init__(self, start_name, start_coords, end_name, end_coords, distance=0, transport_mode=None):
        """
        Initialize a journey segment between two locations.
        :param start_name: Name of the starting location.
        :param start_coords: Coordinates of the starting location (latitude, longitude).
        :param end_name: Name of the ending location.
        :param end_coords: Coordinates of the ending location (latitude, longitude).
        :param distance: Distance of the segment (default is 0 if not calculated).
        :param transport_mode: Transport mode used for the segment.
        """
        self.start_name = start_name
        self.start = {"latitude": start_coords[0], "longitude": start_coords[1]}
        self.end_name = end_name
        self.end = {"latitude": end_coords[0], "longitude": end_coords[1]}
        self.distance = distance
        self.transport_mode = transport_mode

# Decorated function to calculate the haversine distance between two geographical points
@error_handling_decorator
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the haversine distance between two geographical points.
    :param lat1: Latitude of the first point.
    :param lon1: Longitude of the first point.
    :param lat2: Latitude of the second point.
    :param lon2: Longitude of the second point.
    :return: Distance in kilometers.
    """
    R = 6371.0  # Earth's radius in kilometers
    dlat = radians(lat2 - lat1)  # Delta latitude in radians
    dlon = radians(lon2 - lon1)  # Delta longitude in radians
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Function to calculate the total distance of a given path
def calculate_total_distance(path, locations):
    """
    Calculate the total distance of a path using haversine formula.
    :param path: List of location names representing the path.
    :param locations: Dictionary of locations with their coordinates.
    :return: Total distance of the path in kilometers.
    """
    total_distance = 0
    for i in range(len(path) - 1):
        loc1 = locations[path[i]]
        loc2 = locations[path[i + 1]]
        total_distance += haversine(loc1[0], loc1[1], loc2[0], loc2[1])
    return total_distance

# Decorated function implementing the genetic algorithm for path optimization
@execution_time_decorator
def genetic_algorithm(locations, population_size=100, generations=500, mutation_rate=0.01, seed=42):
    """
    Solve the traveling salesman problem using a genetic algorithm.
    :param locations: Dictionary of location names and their coordinates.
    :param population_size: Number of individuals in the population.
    :param generations: Number of generations to evolve.
    :param mutation_rate: Probability of mutation for each individual.
    :param seed: Seed for random number generation for reproducibility.
    :return: Best distance and path found by the algorithm.
    """
    random.seed(seed)
    location_names = list(locations.keys())

    # Create an initial population by generating random permutations of locations
    def create_population():
        return [random.sample(location_names, len(location_names)) for _ in range(population_size)]

    # Fitness function: Inverse of the total distance to favor shorter paths
    def fitness(individual):  
        return 1 / calculate_total_distance(individual, locations)

    # Select two parents using a tournament selection approach
    def select_parents(population):  
        tournament_size = 5
        selected = random.sample(population, tournament_size)
        selected.sort(key=fitness, reverse=True)
        return selected[0], selected[1]

    # Perform ordered crossover to combine parents into offspring
    def crossover(parent1, parent2): 
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = [None] * len(parent1)
        child[start:end] = parent1[start:end]
        for gene in parent2:
            if gene not in child:
                for i in range(len(child)):
                    if child[i] is None:
                        child[i] = gene
                        break
        return child

    # Mutate an individual by swapping two random cities
    def mutate(individual):  
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(individual)), 2)
            individual[i], individual[j] = individual[j], individual[i]

    # Generate the initial population
    population = create_population()

    # Evolution loop: Evolve population over a specified number of generations
    for generation in range(generations):
        new_population = []
        for _ in range(population_size // 2):  # Create pairs of children
            parent1, parent2 = select_parents(population)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])
        population = new_population

    # Find the best individual in the final population
    best_individual = max(population, key=fitness)
    best_distance = calculate_total_distance(best_individual, locations)

    return best_distance, best_individual
