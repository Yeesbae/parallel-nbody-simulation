import math as ma

G = 1.0
SOFTENING = 1e-5

def calculate_force(i, positions, masses):
    # Gravitational force formula, F = (G * m1 * m2) / r^2
    
    total_force_x = 0.0
    total_force_y = 0.0
    x, y = positions[i]
    
    for index, position in enumerate(positions):
        xj, yj = position
        
        if index != i:
            dx = xj - x
            dy = yj - y

            distance_squared = dx * dx + dy * dy + SOFTENING
            distance = ma.sqrt(distance_squared)

            magnitude = G * masses[i] * masses[index] / distance_squared
            
            fx = magnitude * dx / distance
            fy = magnitude * dy / distance
            
            total_force_x += fx
            total_force_y += fy
        
    return total_force_x, total_force_y

def calculate_acceleration(mass, fx, fy):
    # Acceleration formula, F = M * A
    ax = fx / mass
    ay = fy / mass
    
    return ax, ay 

def calculate_velocity (vx, vy, ax, ay, dt):
    # Velocity formula, new_v = v + a × dt
    new_vx = vx + ax * dt
    new_vy = vy + ay * dt

    return new_vx, new_vy

def calculate_position(position, vx, vy, dt):
    # change in position = velocity × time
    x, y = position
    
    new_x = x + vx * dt
    new_y = y + vy * dt
    
    return new_x, new_y
