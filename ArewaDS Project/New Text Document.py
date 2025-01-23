import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from my_noise import pnoise2
import pandas as pd

# Constants for city grid size
GRID_SIZE = 50  # 50x50 city grid

# Generate terrain using Perlin noise
def generate_terrain(grid_size, scale=10, octaves=6, persistence=0.5, lacunarity=2.0):
    terrain = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            terrain[i][j] = pnoise2(i / scale,
                                    j / scale,
                                    octaves=octaves,
                                    persistence=persistence,
                                    lacunarity=lacunarity,
                                    repeatx=grid_size,
                                    repeaty=grid_size,
                                    base=42)
    return terrain

# Classify terrain into land types
def classify_terrain(terrain):
    classified = np.zeros_like(terrain, dtype=str)
    for i in range(terrain.shape[0]):
        for j in range(terrain.shape[1]):
            if terrain[i][j] < -0.05:
                classified[i][j] = 'Water'
            elif terrain[i][j] < 0.05:
                classified[i][j] = 'Parks'
            elif terrain[i][j] < 0.2:
                classified[i][j] = 'Residential'
            elif terrain[i][j] < 0.4:
                classified[i][j] = 'Commercial'
            else:
                classified[i][j] = 'Industrial'
    return classified

# Initialize population grid
def initialize_population(grid_size, land_grid):
    population = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            if land_grid[i][j] == 'Residential':
                population[i][j] = random.randint(50, 200)  # Residential areas start with population
    return population

# Simulate population growth
def simulate_population_growth(population_grid, land_grid, growth_rate=0.02, disaster_chance=0.01):
    for i in range(population_grid.shape[0]):
        for j in range(population_grid.shape[1]):
            if land_grid[i][j] == 'Residential':
                # Apply growth rate
                population_grid[i][j] *= (1 + growth_rate)
                # Apply random disaster
                if random.random() < disaster_chance:
                    population_grid[i][j] *= 0.5  # Disaster halves the population
    return population_grid

# Visualize the city map
def visualize_city_map(terrain, population):
    plt.figure(figsize=(10, 10))
    sns.heatmap(population, cmap="YlGnBu", annot=False, cbar_kws={'label': 'Population'})
    plt.title("City Population Map")
    plt.show()

    plt.figure(figsize=(10, 10))
    sns.heatmap(terrain, cmap="terrain", annot=False, cbar_kws={'label': 'Terrain'})
    plt.title("City Terrain Map")
    plt.show()

# Main simulation
terrain_raw = generate_terrain(GRID_SIZE)
terrain_classified = classify_terrain(terrain_raw)
population = initialize_population(GRID_SIZE, terrain_classified)

# Run simulation for 10 iterations
for step in range(10):
    print(f"Simulation Step: {step + 1}")
    population = simulate_population_growth(population, terrain_classified)

# Visualization of results
visualize_city_map(terrain_raw, population)

# Save simulation data to a DataFrame
data = {
    "Terrain": terrain_classified.flatten(),
    "Population": population.flatten()
}
data_df = pd.DataFrame(data)
print(data_df.head())

# Save to CSV
data_df.to_csv("city_simulation.csv", index=False)
print("Simulation data saved to city_simulation.csv")
