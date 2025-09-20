import sympy as sp

s = sp.symbols('s')

class Plant:
    PARAM_DESCRIPTIONS = {
        'ball_and_beam':{
            'm': 'm: Mass of the ball (kg)',
            'R': 'R: Radius of the ball (m)',
            'd': 'd: Distance from the pivot to the center of the ball (m)',
            'g': 'g: Acceleration due to gravity (m/s^2)',
            'L': 'L: Length of the beam (m)',
            'J': 'J: Moment of inertia of the beam (kg*m^2)'
        },
        'motor': { # Used for motor_speed_control and motor_position_control
            'J' : 'J: Moment of inertia of the rotor (kg*m^2)',
            'b' : 'b: Motor viscous friction constant (N*m*s)',
            'K' : 'K: Electromotive force constant (V/rad/s)',
            'R' : 'R: Electric resistance (Ohm)',
            'L' : 'L: Electric inductance (H)'
        }
    }

    def __init__(self, name,plant_type, transfer_function=None, symbolic_expression=None, parameters=None):
        self.name = name
        self.plant_type = plant_type # For now: ball_and_beam and motor
        self.transfer_function = transfer_function
        self.symbolic_expression = symbolic_expression
        self.parameters = parameters or {}

    def get_transfer_function(self):
        return self.transfer_function
    
    def get_symbolic_transfer_function(self):
        return self.symbolic_expression
    
    def get_parameter_description(self, param_name):
        return self.PARAM_DESCRIPTIONS.get(self.plant_type, {}).get(param_name, "No description")

    @classmethod
    def ball_and_beam(cls, m, R, d, g, L, J):
        """
        Ball and Beam plant model
        P(s) = -m * g * d / ( L*(J / R^2 + m) * s^2 )
        """
        numerator = -m * g * d
        denominator = L * (J / R**2 + m) * s**2
        transfer_function = numerator / denominator
        
        params = {'m': m, 'R': R, 'd': d, 'g': g, 'L': L, 'J': J}
        symbolic_expression = r"$\frac{-" + str(m) + r" \cdot " + str(g) + r" \cdot " + str(d) + "}{" + str(L) + r" \cdot \left(\frac{" + str(J) + "}{" + str(R) + "^2} + " + str(m) + r"\right) \cdot s^2}$"
        
        return cls(name="Ball and Beam",
                   plant_type="ball_and_beam",
                   transfer_function=transfer_function, 
                   symbolic_expression=symbolic_expression, 
                   parameters=params)
    
    @classmethod
    def motor_speed_control(cls, J, b, K, R, L):
        """
        Creates a DC Motor Speed Control plant model.
        P(s) = K / ( (J*s + b) * (L*s + R) + K^2 )
        """
        numerator = K
        denominator = ( (J*s + b) * (L*s + R) + K**2 )
        transfer_function = numerator / denominator

        params = {'J': J, 'b': b, 'K': K, 'R': R, 'L': L}
        symbolic_expression = r"$\frac{" + str(K) + "}{" + r"\left(" + str(J) + "s + " + str(b) + r"\right) \cdot \left(" + str(L) + "s + " + str(R) + r"\right) + " + str(K) + "^2}$"

        return cls(name="DC Motor Speed Control", 
                   plant_type="motor",
                   transfer_function=transfer_function, 
                   symbolic_expression=symbolic_expression, 
                   parameters=params)
    
    @classmethod
    def motor_position_control(cls, J, b, K, R, L):
        """
        Creates a DC Motor Position Control plant model.
        P(s) = K / (s * ( (J*s + b) * (L*s + R) + K^2 ))
        """
        numerator = K
        denominator = (s * ( (J*s + b) * (L*s + R) + K**2 ))
        transfer_function = numerator / denominator

        params = {'J': J, 'b': b, 'K': K, 'R': R, 'L': L}
        symbolic_expression = r"$\frac{" + str(K) + "}{s \\left( \\left(" + str(J) + "s + " + str(b) + "\\right) \\left(" + str(L) + "s + " + str(R) + "\\right) + " + str(K) + "^2 \\right)}$"

        return cls(name="DC Motor Position Control", 
                   plant_type="motor",
                   transfer_function=transfer_function, 
                   symbolic_expression=symbolic_expression, 
                   parameters=params)
    

