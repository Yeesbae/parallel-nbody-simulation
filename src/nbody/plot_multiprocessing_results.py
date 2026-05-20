import matplotlib.pyplot as plt
import numpy as np
from plot_results import load_results

def process_multiprocessing_results(df):
    worker_scaling_df = df[(df['steps'] == 10) & (df['worker_count'] == df['num_chunks'])].copy()
    chunk_scaling_df = df[(df['steps'] == 10) & (df['worker_count'] == 4)].copy()
    speed_up_df = df[(df['steps'] == 10) & (df['worker_count'] == df['num_chunks']) & (df['num_of_particles'] == 100)].copy()
    
    baseline_runtime = speed_up_df[speed_up_df['worker_count'] == 1]['total_runtime_s'].values[0]
    

    speed_up_df['baseline_runtime_100p'] = baseline_runtime
    speed_up_df['speedup'] = baseline_runtime / speed_up_df['total_runtime_s']

    efficiency_df = speed_up_df.copy()
    efficiency_df['efficiency'] = efficiency_df['speedup'] / efficiency_df['worker_count']
    
    runtime_chunks_df = chunk_scaling_df[chunk_scaling_df['num_of_particles'] == 100].copy()
    chunk_baseline = runtime_chunks_df[runtime_chunks_df['num_chunks'] == 4]['total_runtime_s'].values[0]
    
    efficiency_chunk_df = runtime_chunks_df.copy()
    efficiency_chunk_df['speedup'] = chunk_baseline / runtime_chunks_df['total_runtime_s']
    efficiency_chunk_df['efficiency'] = efficiency_chunk_df['speedup'] / efficiency_chunk_df['num_chunks']

    best_mp_df = worker_scaling_df[worker_scaling_df['worker_count'] == 8]
    
    # print(efficiency_df)
    return worker_scaling_df, chunk_scaling_df, speed_up_df, efficiency_df, runtime_chunks_df, efficiency_chunk_df, best_mp_df

def process_naive_results(df):
    # Return a fixed step = 10
    naive_df = df[df['steps'] == 10]
    
    return naive_df

def plot_comparison(naive_df, multiprocessing_df):
    # plot runtime comparison using fixed step and worker count = num_chunks
    worker_scaling_df, chunk_scaling_df, speed_up_df, efficiency_df, runtime_chunks_df, efficiency_chunk_df, best_mp_df = multiprocessing_df
    
    particles = naive_df['num_of_particles'].values
    naive_runtime = naive_df['total_runtime_s'].values
    
    coeffs = np.polyfit(particles**2, naive_runtime, 1) 
    fitted = coeffs[0] * particles**2 + coeffs[1]
    
    plt.figure()
    plt.title('Runtime Comparison Worker scaling')
    plt.xlabel('Number of Particles')
    plt.ylabel('Total Runtime (s)')
    plt.yscale('log')
    for worker in worker_scaling_df['worker_count'].unique():
        plt.plot(worker_scaling_df[worker_scaling_df['worker_count'] == worker]['num_of_particles'], worker_scaling_df[worker_scaling_df['worker_count'] == worker]['total_runtime_s'], label=f'Multiprocessing ({worker} workers)', marker='x')
    plt.plot(naive_df['num_of_particles'], naive_df['total_runtime_s'], label='Naive', marker='.')
    
    plt.grid(True)  
    plt.legend()
    
    plt.figure()
    plt.title('Runtime Comparison Chunk scaling')
    plt.xlabel('Number of Particles')
    plt.ylabel('Total Runtime (s)')
    plt.yscale('log')
    for chunk in chunk_scaling_df['num_chunks'].unique():
        plt.plot(chunk_scaling_df[chunk_scaling_df['num_chunks'] == chunk]['num_of_particles'], chunk_scaling_df[chunk_scaling_df['num_chunks'] == chunk]['total_runtime_s'], label=f'Multiprocessing ({chunk} chunks)', marker='x')
    plt.plot(naive_df['num_of_particles'], naive_df['total_runtime_s'], label='Naive', marker='.')
    
    plt.grid(True)
    plt.legend()
    
    plt.figure()
    plt.title('Speed up comparison')
    plt.xlabel('Worker Count')
    plt.ylabel('Speedup (s)')
    plt.plot(speed_up_df['worker_count'], speed_up_df['speedup'], label='Varying workers', marker='o')
    plt.plot(speed_up_df['worker_count'], speed_up_df['worker_count'], label='Ideal', marker='x')
    plt.grid(True)
    plt.legend()
    
    plt.figure()
    plt.title('Efficiency vs Worker Count')
    plt.xlabel('Worker Count')
    plt.ylabel('Efficiency')
    plt.plot(efficiency_df['worker_count'], efficiency_df['efficiency'], label='Varying workers', marker='x')
    plt.legend()
    
    plt.figure()
    plt.title('Runtime vs Chunks')
    plt.xlabel('Number of Chunks')
    plt.ylabel('Runtime (s)')
    plt.plot(runtime_chunks_df['num_chunks'], runtime_chunks_df['total_runtime_s'], label='100 particles', marker='o')
    plt.legend()
    
    plt.figure()
    plt.title('Efficiency vs Number of Chunks')
    plt.xlabel('Number of Chunks')
    plt.ylabel('Efficiency')
    plt.plot(efficiency_chunk_df['num_chunks'], efficiency_chunk_df['efficiency'], label='Efficiency vs Number of Chunks', marker='x')
    plt.legend()
    
    plt.figure()
    plt.title('Runtime Complexity')
    plt.xlabel('Number of Particles')
    plt.ylabel('Runtime (s)')
    plt.plot(particles, naive_runtime, marker='o', label='Naive')
    plt.plot(particles, fitted, linestyle='--', label='O(n²) fit')
    plt.plot(best_mp_df['num_of_particles'], best_mp_df['total_runtime_s'], marker='x', label='Multiprocessing (8 workers)')
    plt.legend()
    
    plt.show()
    
    return 0

def main():
    naive_results = load_results('results/data/simulation_results.csv')
    multiprocessing_results = load_results('results/data/simulation_multiprocessing_results.csv')
    processed_naive_results = process_naive_results(naive_results)
    processed_multiprocessing_results = process_multiprocessing_results(multiprocessing_results)
    plot_comparison(processed_naive_results, processed_multiprocessing_results)
    return 0

if __name__ == "__main__":
    main()
