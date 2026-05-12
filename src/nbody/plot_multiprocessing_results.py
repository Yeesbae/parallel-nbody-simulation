import matplotlib.pyplot as plt
from plot_results import load_results

def process_multiprocessing_results(df):
    worker_scaling_df = df[(df['steps'] == 10) & (df['worker_count'] == df['num_chunks'])]
    chunk_scaling_df = df[(df['steps'] == 10) & (df['worker_count'] == 4)]
    # print(chunk_scaling_df)
    return worker_scaling_df, chunk_scaling_df

def process_naive_results(df):
    # Return a fixed step = 10
    naive_df = df[df['steps'] == 10]
    
    return naive_df

def plot_comparison(naive_df, multiprocessing_df):
    # plot runtime comparison using fixed step and worker count = num_chunks
    worker_scaling_df, chunk_scaling_df = multiprocessing_df
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
    plt.show()
    
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
