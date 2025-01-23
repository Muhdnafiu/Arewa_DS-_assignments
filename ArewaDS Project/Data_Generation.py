import numpy as np
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Constants for the grid and simulation
GRID_SIZE = 50
SIMULATION_STEPS = 10

# Generate terrain using Perlin Noise
def generate_terrain(grid_size, octaves=3):
    """Generates a terrain grid using Perlin noise."""
    noise = PerlinNoise(octaves=octaves)
    terrain = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            terrain[i, j] = noise([i / grid_size, j / grid_size])
    return terrain

# Classify terrain into land types
def classify_terrain(terrain):
    """Classifies terrain into different land types based on height."""
    classified = np.empty(terrain.shape, dtype=object)
    for i in range(terrain.shape[0]):
        for j in range(terrain.shape[1]):
            if terrain[i, j] < -0.05:
                classified[i, j] = 'Water'
            elif terrain[i, j] < 0.05:
                classified[i, j] = 'Parks'
            elif terrain[i, j] < 0.2:
                classified[i, j] = 'Residential'
            elif terrain[i, j] < 0.4:
                classified[i, j] = 'Commercial'
            else:
                classified[i, j] = 'Industrial'
    return classified

# Initialize population grid
def initialize_population(classified_terrain):
    """Initializes the population grid based on land types."""
    population = np.zeros(classified_terrain.shape, dtype=float)
    for i in range(classified_terrain.shape[0]):
        for j in range(classified_terrain.shape[1]):
            if classified_terrain[i, j] == 'Residential':
                population[i, j] = np.random.randint(50, 200)
    return population

# Simulate population growth
def simulate_population(population, growth_rate=0.05):
    """Simulates population growth over multiple steps."""
    for _ in range(SIMULATION_STEPS):
        growth = population * growth_rate
        disaster_effect = np.random.choice([0, -0.3, -0.1, 0.1], p=[0.8, 0.05, 0.1, 0.05])
        population += growth + disaster_effect * population
        population = np.maximum(population, 0)  # Avoid negative population
    return population

# Visualization of terrain and population
def visualize_terrain_and_population(terrain, classified, population):
    """Visualizes the terrain and population data as heatmaps."""
    # Terrain visualization
    plt.figure(figsize=(10, 8))
    sns.heatmap(terrain, cmap="terrain", cbar_kws={'label': 'Terrain Height'})
    plt.title("Generated Terrain Map")
    plt.show()

    # Population visualization
    plt.figure(figsize=(10, 8))
    sns.heatmap(population, cmap="coolwarm", cbar_kws={'label': 'Population Density'})
    plt.title("Population Distribution")
    plt.show()

# Export simulation data to CSV
def export_to_csv(classified_terrain, population):
    """Exports the classified terrain and population data to a CSV file."""
    data = []
    for i in range(classified_terrain.shape[0]):
        for j in range(classified_terrain.shape[1]):
            data.append([i, j, classified_terrain[i, j], population[i, j]])
    df = pd.DataFrame(data, columns=['Row', 'Column', 'Land Type', 'Population'])
    df.to_csv('simulation_data.csv', index=False)
    print("Simulation data exported to simulation_data.csv")

# Main execution
def main():
    """Main function to run the terrain simulation project."""
    print("Generating terrain...")
    terrain = generate_terrain(GRID_SIZE)

    print("Classifying terrain...")
    classified_terrain = classify_terrain(terrain)

    print("Initializing population...")
    population = initialize_population(classified_terrain)

    print("Simulating population growth...")
    population = simulate_population(population)

    print("Visualizing terrain and population...")
    visualize_terrain_and_population(terrain, classified_terrain, population)

    print("Exporting data to CSV...")
    export_to_csv(classified_terrain, population)

# Run the project
if __name__ == "__main__":
    main()
