import physics as phy
import numpy as np
import csv
import time

def create_particles(num_of_particles):
    positions = []
    velocities = []
    masses = []
    rng = np.random.default_rng(seed=42)

    for _ in range(num_of_particles):
        positions.append([rng.uniform(low=-1.0, high=1.0), rng.uniform(low=-1.0, high=1.0)])
        velocities.append([0, 0])
        masses.append(1.0)

    return (positions, velocities, masses)
    
def simulate(implementation, num_of_particles, steps, dt):
    positions, velocities, masses = create_particles(num_of_particles)
    total_runtime_s = 0
    
    start = time.perf_counter()
    for _ in range(steps):
        forces = []
        new_positions = []
        new_velocities = []
        
        for i in range(len(positions)):
            forces.append(phy.calculate_force(i, positions, masses))
        for i in range(len(positions)):
            cur_vx, cur_vy = velocities[i]
            fx, fy = forces[i]
            ax, ay = phy.calculate_acceleration(masses[i], fx, fy)
            new_vx, new_vy = phy.calculate_velocity(cur_vx, cur_vy, ax, ay, dt)
            new_x, new_y = phy.calculate_position(positions[i], new_vx, new_vy, dt)
            new_positions.append([new_x, new_y])
            new_velocities.append([new_vx, new_vy])
        positions = new_positions
        velocities = new_velocities
    end = time.perf_counter()
    total_runtime_s = end - start
    interactions = num_of_particles * (num_of_particles - 1) * steps
    interactions_per_s = interactions / total_runtime_s

    return [implementation, num_of_particles, steps, dt, total_runtime_s, interactions, interactions_per_s]

def save_results(results):
    with open('results/simulation_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["implementation", "num_of_particles", "steps", "dt", "total_runtime_s", "interactions", "interactions_per_s"])
        writer.writerows(results)
    return 0

def main():
    implementation = 'naive'
    num_of_particles = [10, 50, 100, 200, 500]
    steps = [1, 5, 10]
    dt =0.01
    all_results = []
    
    for particle in num_of_particles:
        for step in steps:
            result = (simulate(implementation, particle, step, dt))
            all_results.append(result)
    save_results(all_results)

    return 0
    
if __name__ == "__main__":
    main()
