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
