import matplotlib
import sympy as sp
import numpy as np
import control as ct

def plot_results(results, title):
    print (f"Plotting results for {title}")
    # Placeholder for plotting logic
    # This function would contain the logic to plot the results using matplotlib
    


def get_controller_coefficients():
    coefficients = input("Enter controller coefficients (kd, kp, ki) separated by commas: ")
    kd, kp, ki = map(float, coefficients.split(','))
    print(f"Controller coefficients set: kd={kd}, kp={kp}, ki={ki}")
    return kd, kp, ki

def instert_plant_equation():
    input_equation = input("Enter the plant equation (e.g., 's^2 + 3*s + 2'): ")
    s = sp.symbols('s')
    plant_equation = sp.sympify(input_equation)
    print(f"Plant equation set: {plant_equation}")
    return plant_equation

def calculate_pid(plant_equation, kd, kp, ki):
    s = sp.symbols('s')
    # Define the PID controller transfer function
    pid_controller = kp + ki/s + kd*s
    # Calculate the closed-loop transfer function
    closed_loop_tf = plant_equation * pid_controller / (1 + plant_equation * pid_controller)
    print(f"Closed-loop transfer function: {closed_loop_tf}")
    return closed_loop_tf

def main():
    print("Welcome to the PID Calculator")
    coefficients = get_controller_coefficients()
    plant_equation = instert_plant_equation()
    closed_loop_tf = calculate_pid(plant_equation, coefficients[0], coefficients[1], coefficients[2])
    plot_results(closed_loop_tf, "Closed-Loop Transfer Function")


main()