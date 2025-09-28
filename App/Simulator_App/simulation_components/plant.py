import sympy as sp
from abc import ABC, abstractmethod

s = sp.symbols('s')


class Plant(ABC):
    """Abstract base class for all plants."""

    def __init__(self, name, parameters=None):
        self.name = name
        self.parameters = parameters or {}

    @abstractmethod
    def get_transfer_function(self):
        """Return the symbolic transfer function (sympy expression)."""
        pass

    @abstractmethod
    def get_latex_equation(self):
        """Return the LaTeX string representation of the transfer function."""
        pass

    @abstractmethod
    def get_parameter_descriptions(self):
        """Return dict of parameter descriptions."""
        pass

    def get_parameters(self):
        return self.parameters

    def set_parameters(self, **kwargs):
        """Update internal parameters with given values."""
        self.parameters.update(kwargs)


# ---------------- Specific Plants ---------------- #

class BallAndBeamPlant(Plant):
    DESCRIPTIONS = {
        'm': 'm: Mass of the ball (kg)',
        'R': 'R: Radius of the ball (m)',
        'd': 'd: Distance from the pivot to the center of the ball (m)',
        'g': 'g: Acceleration due to gravity (m/s^2)',
        'L': 'L: Length of the beam (m)',
        'J': 'J: Moment of inertia of the beam (kg*m^2)'
    }

    def __init__(self, m=1, R=1, d=1, g=9.81, L=1, J=1):
        params = {'m': m, 'R': R, 'd': d, 'g': g, 'L': L, 'J': J}
        super().__init__("Ball and Beam", params)

    def get_transfer_function(self):
        p = self.parameters
        numerator = -p['m'] * p['g'] * p['d']
        denominator = p['L'] * (p['J'] / p['R']**2 + p['m']) * s**2
        return numerator / denominator

    def get_latex_equation(self, m=None, R=None, d=None, g=None, L=None, J=None):
            """Return LaTeX equation, using provided values or defaults/symbols"""

            m_val = str(m) if m is not None else 'm'
            R_val = str(R) if R is not None else 'R'
            d_val = str(d) if d is not None else 'd'
            g_val = str(g) if g is not None else 'g'
            L_val = str(L) if L is not None else 'L'
            J_val = str(J) if J is not None else 'J'
            

            return (rf"$\frac{{-{m_val} \cdot {g_val} \cdot {d_val}}}"
                    rf"{{{L_val} \cdot \left(\frac{{{J_val}}}{{{R_val}^2}} + {m_val}\right) \cdot s^2}}$")

    def get_parameter_descriptions(self):
        return self.DESCRIPTIONS


class MotorSpeedPlant(Plant):
    DESCRIPTIONS = {
        'J': 'J: Moment of inertia of the rotor (kg*m^2)',
        'b': 'b: Motor viscous friction constant (N*m*s)',
        'K': 'K: Electromotive force constant (V/rad/s)',
        'R': 'R: Electric resistance (Ohm)',
        'L': 'L: Electric inductance (H)'
    }

    def __init__(self, J=1, b=1, K=1, R=1, L=1):
        params = {'J': J, 'b': b, 'K': K, 'R': R, 'L': L}
        super().__init__("DC Motor Speed Control", params)

    def get_transfer_function(self):
        p = self.parameters
        numerator = p['K']
        denominator = ( (p['J']*s + p['b']) * (p['L']*s + p['R']) + p['K']**2 )
        return numerator / denominator

    def get_latex_equation(self, J=None, b=None, K=None, R=None, L=None):
        """Return LaTeX equation, using provided values or symbols if None"""
        J_val = str(J) if J is not None else 'J'
        b_val = str(b) if b is not None else 'b'
        K_val = str(K) if K is not None else 'K'
        R_val = str(R) if R is not None else 'R'
        L_val = str(L) if L is not None else 'L'

        return rf"$\frac{{{K_val}}}{{({J_val}s + {b_val})({L_val}s + {R_val}) + {K_val}^2}}$"

    def get_parameter_descriptions(self):
        return self.DESCRIPTIONS


class MotorPositionPlant(MotorSpeedPlant):
    def __init__(self, J=1, b=1, K=1, R=1, L=1):
        super().__init__(J, b, K, R, L)
        self.name = "DC Motor Position Control"

    def get_transfer_function(self):
        p = self.parameters
        numerator = p['K']
        denominator = s * ( (p['J']*s + p['b']) * (p['L']*s + p['R']) + p['K']**2 )
        return numerator / denominator

    def get_latex_equation(self, J=None, b=None, K=None, R=None, L=None):
        """Return LaTeX equation for position control, using provided values or symbols if None"""
        J_val = str(J) if J is not None else 'J'
        b_val = str(b) if b is not None else 'b'
        K_val = str(K) if K is not None else 'K'
        R_val = str(R) if R is not None else 'R'
        L_val = str(L) if L is not None else 'L'

        return rf"$\frac{{{K_val}}}{{s \cdot (({J_val}s + {b_val})({L_val}s + {R_val}) + {K_val}^2)}}$"


class PersonalizedPlant(Plant):
    DESCRIPTIONS = {
        'Numerator': 'Numerator: Numerator coefficients (list)',
        'Denominator': 'Denominator: Denominator coefficients (list)'
    }

    def __init__(self, num=None, den=None):
        if num is None:
            num = [1]
        if den is None:
            den = [1]  # Default to gain 1
        params = {'Numerator': num, 'Denominator': den}
        super().__init__("Personalized Plant", params)

    def _ensure_list(self, coeffs):
        """Convert input to list of numbers/symbols if needed"""
        if coeffs is None:
            return [1]  # default to 1

        # If already a list, return as is
        if isinstance(coeffs, list):
            return coeffs

        # If single number, convert to list
        if isinstance(coeffs, (int, float)):
            return [coeffs]

        # If string, try to parse
        if isinstance(coeffs, str):
            items = coeffs.split(",")
            result = []
            for item in items:
                item = item.strip()
                try:
                    result.append(float(item))
                except ValueError:
                    # If not a number, treat as symbol
                    result.append(sp.Symbol(item))
            return result

        # Fallback case (already symbolic or something else)
        return [coeffs]


    def get_transfer_function(self, **kwargs):
        params = self.parameters.copy()
        params.update(kwargs)

        num_coeffs = self._ensure_list(params['Numerator'])
        den_coeffs = self._ensure_list(params['Denominator'])

        num_poly = sum(coef * s**i for i, coef in enumerate(reversed(num_coeffs)))
        den_poly = sum(coef * s**i for i, coef in enumerate(reversed(den_coeffs)))

        return num_poly / den_poly

    def get_latex_equation(self, **kwargs):
        params = self.parameters.copy()
        params.update(kwargs)

        num_coeffs = self._ensure_list(params['Numerator'])
        den_coeffs = self._ensure_list(params['Denominator'])

        num_poly = sum(coef * s**i for i, coef in enumerate(reversed(num_coeffs)))
        den_poly = sum(coef * s**i for i, coef in enumerate(reversed(den_coeffs)))

        expr = num_poly / den_poly
        return f"${sp.latex(expr)}$"

    def get_parameter_descriptions(self):
        return self.DESCRIPTIONS



PLANT_MAP = {
    "Ball and Beam": BallAndBeamPlant,
    "DC Motor Speed Control": MotorSpeedPlant,
    "DC Motor Position Control": MotorPositionPlant,
    "Personalized Plant": PersonalizedPlant
}

def get_plant(plant_type: str):
    """Factory method to create plant by name"""
    try:
        return PLANT_MAP[plant_type]()
    except KeyError:
        raise ValueError(f"Unknown plant type: {plant_type}")