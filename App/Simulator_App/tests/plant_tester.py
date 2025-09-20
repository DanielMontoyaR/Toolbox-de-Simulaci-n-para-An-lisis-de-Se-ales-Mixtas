import sympy as sp
from simulation_components.plant import *


#Tests for predefined plants
def test_ball_and_beam():
    m = 0.5
    R = 0.05
    d = 0.1
    g = 9.81
    L = 1.0
    J = 0.002

    ball_beam = Plant.ball_and_beam(m, R, d, g, L, J)
    print("\nPlant Name:", ball_beam.name)
    print("\nSimplified TF:", ball_beam.get_transfer_function())
    print("\nLaTeX Expression:", ball_beam.get_symbolic_transfer_function())
    print("\nParameters:", ball_beam.parameters)
    print(len(ball_beam.parameters))
    print("\nParameters Description:")
    print(ball_beam.get_parameter_description("m"))
    print(ball_beam.get_parameter_description("R"))
    print(ball_beam.get_parameter_description("d"))
    print(ball_beam.get_parameter_description("g"))
    print(ball_beam.get_parameter_description("L"))
    print(ball_beam.get_parameter_description("J"))


def test_motor_speed():
    J = 0.01
    b = 0.1
    K = 0.01
    R = 1.0
    L = 0.5

    speed_motor = Plant.motor_speed_control(J, b, K, R, L)
    print("\n\n\n\n\n######################## Motor Speed Control ########################")
    print("\nPlant Name:", speed_motor.name)
    print("\nSimplified TF:", speed_motor.get_transfer_function())
    print("\nLaTeX Expression:", speed_motor.get_symbolic_transfer_function())
    print("\nParameters:", speed_motor.parameters)
    print(len(speed_motor.parameters))
    print("\nParameters Description:")
    print(speed_motor.get_parameter_description("J"))
    print(speed_motor.get_parameter_description("b"))
    print(speed_motor.get_parameter_description("K"))
    print(speed_motor.get_parameter_description("R"))
    print(speed_motor.get_parameter_description("L"))


def test_motor_position():
    J = 0.01
    b = 0.1
    K = 0.01
    R = 1.0
    L = 0.5

    position_motor = Plant.motor_position_control(J, b, K, R, L)
    print("\n\n\n\n\n######################## Motor Position Control ########################")
    print("\nPlant Name:", position_motor.name)
    print("\nSimplified TF:", position_motor.get_transfer_function())
    print("\nLaTeX Expression:", position_motor.get_symbolic_transfer_function())
    print(len(position_motor.parameters))
    print("\nParameters:", position_motor.parameters)
    print(position_motor.get_parameter_description("J"))
    print(position_motor.get_parameter_description("b"))
    print(position_motor.get_parameter_description("K"))
    print(position_motor.get_parameter_description("R"))
    print(position_motor.get_parameter_description("L"))



def run_all_tests():
    test_ball_and_beam()
    test_motor_speed()
    test_motor_position()









