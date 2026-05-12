import matplotlib.pyplot as plt
from plot_results import load_results

def process_multiprocessing_results(df):
    mp_df = df[(df['steps'] == 10) & (df['worker_count'] == df['num_chunks'])]
    print(mp_df)
    return mp_df

def process_naive_results(df):
    # Return a fixed step = 10
    naive_df = df[df['steps'] == 10]
    
    return naive_df

def plot_comparison(naive_df, multiprocessing_df):
    # plot runtime comparison
    plt.figure()
    plt.title('Runtime Comparison')
    plt.xlabel('Number of Particles')
    plt.ylabel('Total Runtime (s)')
    plt.yscale('log')
    for worker in multiprocessing_df['worker_count'].unique():
        plt.plot(multiprocessing_df[multiprocessing_df['worker_count'] == worker]['num_of_particles'], multiprocessing_df[multiprocessing_df['worker_count'] == worker]['total_runtime_s'], label=f'Multiprocessing ({worker} workers)', marker='o')
    plt.plot(naive_df['num_of_particles'], naive_df['total_runtime_s'], label='Naive', marker='o')
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
