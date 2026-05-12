import matplotlib.pyplot as plt
import pandas as pd

def load_results(file_path):
    return pd.read_csv(file_path)

def process_naive_results(df):
    df2 = (df.groupby(['num_of_particles', 'steps'])
            .agg({
                'total_runtime_s': 'mean',
                'interactions_per_s': 'mean'
                })
            .reset_index()
           )
    # print(df2)
    return df2

def plot_results(naive_df):
    # plot runtime vs number of particles
    plt.figure()
    plt.title('Runtime vs Number of Particles')
    plt.xlabel('Number of Particles')
    plt.ylabel('Total Runtime (s)')
    plt.yscale('log')
    for step in naive_df['steps'].unique():
        step_df = naive_df[naive_df['steps'] == step]
        plt.plot(step_df['num_of_particles'], step_df['total_runtime_s'], marker='o', label=f'Steps: {step}')
    plt.grid(True)  
    plt.legend()
    plt.show()
    
    # plot interactions per second vs number of particles
    plt.figure()
    plt.title('Interactions per Second vs Number of Particles')
    plt.xlabel('Number of Particles')
    plt.ylabel('Interactions per Second')
    plt.yscale('log')
    for step in naive_df['steps'].unique():
        step_df = naive_df[naive_df['steps'] == step]
        plt.plot(step_df['num_of_particles'], step_df['interactions_per_s'], marker='o', label=f'Steps: {step}')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    return 0

def main():
    naive_results = load_results('results/data/simulation_results.csv')
    processed_naive_results = process_naive_results(naive_results)
    # plot_results(processed_naive_results)
    return 0

if __name__ == "__main__":
    main()
