import src.nbody.physics as physics

A = (0, 0)
B = (1, 0)

positions = [A, B]
masses = [1.0, 1.0]

def test_calculate_force():
    force = []
    for index in range(len(positions)):
        force.append(physics.calculate_force(index, positions, masses))
    
    fx_A, fy_A = force[0]
    fx_B, fy_B = force[1]
    
    assert fx_A > 0
    assert fx_B < 0
    assert abs(fy_A) < 1e-6
    assert abs(fy_B) < 1e-6
    assert abs(fx_A + fx_B) < 1e-6
    assert abs(fy_A + fy_B) < 1e-6
    
def test_calculate_acceleration():
    force = [2, 4]
    mass = 2.0
    acceleration = physics.calculate_acceleration(mass, force[0], force[1])
    
    ax, ay = acceleration
    
    assert abs(ax - 1.0) < 1e-6
    assert abs(ay - 2.0) < 1e-6

def test_calculate_velocity():
    vx, vy = 0.0, 0.0
    ax, ay = 1.0, 2.0
    dt = 0.1
    
    new_vx, new_vy = physics.calculate_velocity(vx, vy, ax, ay, dt)
    
    assert abs(new_vx - 0.1) < 1e-6
    assert abs(new_vy - 0.2) < 1e-6
    
def test_calculate_position():
    position = (0.0, 0.0)
    vx, vy = (1.0, 2.0)
    dt = 0.1
    
    new_x, new_y = physics.calculate_position(position, vx, vy, dt)
    
    assert abs(new_x - 0.1) < 1e-6
    assert abs(new_y - 0.2) < 1e-6

def main():
    test_calculate_force()
    test_calculate_acceleration()
    test_calculate_velocity()
    test_calculate_position()
    print("All tests passed!")
    

if __name__ == "__main__":
    main()

    
