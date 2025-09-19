from simulation_components.plant import ball_and_beam, motor_speed_control, motor_position_control
import sympy as sp

#Tests for predefined plants
def test_ball_and_beam():
    m = 0.5
    R = 0.05
    d = 0.1
    g = 9.81
    L = 1.0
    J = 0.002

    plant = ball_and_beam(m, R, d, g, L, J)

    print("\nPlant Name:", plant.name)
    print("\nSimplified TF:", plant.get_transfer_function())
    print("\nLaTeX Expression:", plant.get_symbolic_transfer_function())
    print("\nParameters:", plant.parameters)


def test_motor_speed():
    J = 0.01
    b = 0.1
    K = 0.01
    R = 1.0
    L = 0.5

    plant = motor_speed_control(J, b, K, R, L)

    print("\nPlant Name:", plant.name)
    print("\nSimplified TF:", plant.get_transfer_function())
    print("\nLaTeX Expression:", plant.get_symbolic_transfer_function())
    print("\nParameters:", plant.parameters)


def test_motor_position():
    J = 0.01
    b = 0.1
    K = 0.01
    R = 1.0
    L = 0.5

    plant = motor_position_control(J, b, K, R, L)

    print("\nPlant Name:", plant.name)
    print("\nSimplified TF:", plant.get_transfer_function())
    print("\nLaTeX Expression:", plant.get_symbolic_transfer_function())
    print("\nParameters:", plant.parameters)

test_ball_and_beam()
test_motor_speed()
test_motor_position()