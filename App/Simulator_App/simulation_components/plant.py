import sympy as sp


s = sp.symbols('s')

class Plant:
    def __init__(self, name, transfer_function=None, symbolic_expression=None, parameters=None):
        self.name = name
        self.transfer_function = transfer_function #Simplified expression
        self.symbolic_expression = symbolic_expression # Symbolic expression
        self.parameters = parameters or {} 

    def get_transfer_function(self):
        return self.transfer_function
    
    def get_symbolic_transfer_function(self):
        return self.symbolic_expression
        

#Predefineed Plants

def ball_and_beam(m, R, d, g, L, J):
    """
    Creates a Ball and Beam plant model.

    Parameters:
        m (float): Mass of the ball (kg)
        R (float): Radius of the ball (m)
        d (float): Distance from the pivot to the center of the ball (m)
        g (float): Acceleration due to gravity (m/s^2)
        L (float): Length of the beam (m)
        J (float): Moment of inertia of the beam (kg*m^2)

        Returns:
        Plant: An instance of the Plant class representing the Ball and Beam system.
        """
    #P(s) = -m*g*d / ( L * (J/R^2 + m) * s^2 )

    s = sp.symbols('s')

    #Simplified expression (for calculations)
    numerator = -m * g * d
    denominator = L * (J / R**2 + m) * ( s**2 )
    transfer_function = numerator / denominator

    
    params = {'m': m,'R': R,'d': d,'g': g,'L': L,'J': J}

    # Symbolic expression in LaTeX format
    symbolic_expression = r"$\frac{-" + str(m) + r" \cdot " + str(g) + r" \cdot " + str(d) + "}{" + str(L) + r" \cdot \left(\frac{" + str(J) + "}{" + str(R) + "^2} + " + str(m) + r"\right) \cdot s^2}$"

    return Plant(name="Ball and Beam", transfer_function=transfer_function, symbolic_expression=symbolic_expression, parameters=params)


def motor_speed_control(J, b, K, R, L):
    """
    Creates a DC Motor Speed Control plant model.

    Parameters:
        J (float): Moment of inertia of the rotor (kg*m^2)
        b (float): Motor viscous friction constant (N*m*s)
        K (float): Electromotive force constant (V/rad/s)
        R (float): Electric resistance (Ohm)
        L (float): Electric inductance (H)

    Returns:
        Plant: An instance of the Plant class representing the DC Motor Speed Control system.
    """
    #P(s) = K / ( (J*s + b) * (L*s + R) + K^2 )

    s = sp.symbols('s')

    #Simplified expression (for calculations)
    numerator = K
    denominator = ( (J*s + b) * (L*s + R) + K**2 )
    transfer_function = numerator / denominator

    params = {'J': J,'b': b,'K': K,'R': R,'L': L}

    # Symbolic expression in LaTeX format
    symbolic_expression = r"$\frac{" + str(K) + "}{" + r"\left(" + str(J) + "s + " + str(b) + r"\right) \cdot \left(" + str(L) + "s + " + str(R) + r"\right) + " + str(K) + "^2}$"

    return Plant(name="DC Motor Speed Control", transfer_function=transfer_function, symbolic_expression=symbolic_expression, parameters=params)


def motor_position_control(J, b, K, R, L):
    """
    Creates a DC Motor Position Control plant model.

    Parameters:
        J (float): Moment of inertia of the rotor (kg*m^2)
        b (float): Motor viscous friction constant (N*m*s)
        K (float): Electromotive force constant (V/rad/s)
        R (float): Electric resistance (Ohm)
        L (float): Electric inductance (H)

    Returns:
        Plant: An instance of the Plant class representing the DC Motor Position Control system.
    """
    #P(s) = K / (s * ( (J*s + b) * (L*s + R) + K**2 ))

    s = sp.symbols('s')

    #Simplified expresssion (for calculations)
    numerator = K
    denominator = (s * ( (J*s + b) * (L*s + R) + K**2 ))
    transfer_function = numerator / denominator

    params = {'J': J,'b': b,'K': K,'R': R,'L': L}

    # Symbolic expression in LaTeX format
    symbolic_expression = r"$\frac{" + str(K) + "}{" + "s( \left(" + str(J) + "s + " + str(b) + r"\right) \left(" + str(L) + "s + " + str(R) + r"\right) + " + str(K) + "^2)}$"

    return Plant(name="DC Motor Position Control", transfer_function=transfer_function, symbolic_expression=symbolic_expression, parameters=params)