from multiprocessing import Pool
import time
import csv
import numpy as np
import physics as phy
import utils
import naive

IMPLEMENTATION = 'multiprocessing'
WORKERS = [1, 2, 4, 8]
CHUNKS_MULTIPLIER = [1, 2, 4, 8]
STEPS = [1, 5, 10]
NUM_OF_PARTICLES = [10, 50, 100, 200, 500]
DT = 0.01

def worker(task):
    N, positions, masses = task
    forces = []
    
    for i in N:
        forces.append((i, (phy.calculate_force(i, positions, masses))))
    
    return forces

def simulate(implementation, particle, step, dt, worker_count, num_chunks):
    positions, velocities, masses = utils.create_particles(particle)
    total_runtime_s = 0
    start = time.perf_counter()
    
    with Pool(worker_count) as pool:
        for _ in range(step):
            tasks = []
            forces = [None] * len(positions)
            
            chunks = np.array_split(range(len(positions)), num_chunks)
            for chunk in chunks:
                tasks.append((chunk, positions, masses))
            
            results = pool.map(worker, tasks)
            for result in results:
                for k, force in result:
                    forces[k] = force
                        
            new_positions = []
            new_velocities = []
            
            for j in range(len(positions)):
                cur_vx, cur_vy = velocities[j]
                fx, fy = forces[j]
                ax, ay = phy.calculate_acceleration(masses[j], fx, fy)
                new_vx, new_vy = phy.calculate_velocity(cur_vx, cur_vy, ax, ay, dt)
                new_x, new_y = phy.calculate_position(positions[j], new_vx, new_vy, dt)
                new_positions.append([new_x, new_y])
                new_velocities.append([new_vx, new_vy])
            positions = new_positions
            velocities = new_velocities
    end = time.perf_counter()
    total_runtime_s = end - start
    interactions = particle * (particle - 1) * step
    interactions_per_s = interactions / total_runtime_s
    return [implementation, particle, step, dt, worker_count, num_chunks, total_runtime_s, interactions, interactions_per_s]
    
def save_results(results):
    with open('results/data/simulation_multiprocessing_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["implementation", "num_of_particles", "steps", "dt", "worker_count", "num_chunks", "total_runtime_s", "interactions", "interactions_per_s"])
        writer.writerows(results)
    return 0


def main():
    results = []
    for worker in WORKERS:
        for multiplier in CHUNKS_MULTIPLIER:
            num_chunks = multiplier * worker
            for particle in NUM_OF_PARTICLES:
                for step in STEPS:
                    results.append(simulate(IMPLEMENTATION, particle, step, DT, worker, num_chunks))
    save_results(results)
    return 0

if __name__ == "__main__":
    main()
                
            
        