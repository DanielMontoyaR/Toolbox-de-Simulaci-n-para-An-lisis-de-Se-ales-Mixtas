import control as ctrl
from utils.input_utils import cannot_be_zero

class Sensor:
    """
    Clase para modelar sensores como sistemas LTI
    Similar a PersonalizedPlant pero simplificado
    """
    
    def __init__(self, num=None, den=None):
        self.name = "Sensor"
        self.num_coeffs = self._ensure_list(num or [1])
        self.den_coeffs = self._ensure_list(den or [1])

        self.num_coeffs_description = "Numerator: Numerator coefficients (list)"
        self.den_coeffs_description = "Denominator: Denominator coefficients (list)"
    
    def _ensure_list(self, coeffs):
        """Convert input to list of numbers if needed"""
        if coeffs is None:
            return [1]
        
        if isinstance(coeffs, list):
            return coeffs
        
        if isinstance(coeffs, (int, float)):
            return [coeffs]
        
        if isinstance(coeffs, str):
            items = coeffs.split(",")
            result = []
            for item in items:
                item = item.strip()
                if item == "":
                    continue
                try:
                    result.append(float(item))
                except ValueError:
                    raise ValueError(f"Invalid coefficient: {item}. Only numbers allowed.")
            return result
        
        return [coeffs]
    
    def get_transfer_function(self):
        """Return the transfer function of the sensor"""
        if all(coef == 0 for coef in self.den_coeffs):
            return "Error: Denominator cannot be all zeros."
        
        error = cannot_be_zero("Denominator", sum(self.den_coeffs))
        if error:
            return error
        
        try:
            return ctrl.TransferFunction(self.num_coeffs, self.den_coeffs)
        except Exception as e:
            return f"Error creating transfer function: {e}"
    
    def get_latex_equation(self, **kwargs):
        """Return LaTeX representation, optionally using provided coefficients"""
        if kwargs:
            # Use provided coefficients for preview
            num_coeffs = self._ensure_list(kwargs.get('Numerator', self.num_coeffs))
            den_coeffs = self._ensure_list(kwargs.get('Denominator', self.den_coeffs))
        else:
            # Use current coefficients
            num_coeffs = self.num_coeffs
            den_coeffs = self.den_coeffs
        
        num_str = self._coeffs_to_latex(num_coeffs)
        den_str = self._coeffs_to_latex(den_coeffs)
        return f"$\\frac{{{num_str}}}{{{den_str}}}$"
    
    def _coeffs_to_latex(self, coeffs):
        """Convert coefficients to LaTeX polynomial string"""
        if not coeffs:
            return "0"
        
        terms = []
        n = len(coeffs)
        
        for i, coef in enumerate(coeffs):
            power = n - i - 1
            
            if coef == 0:
                continue
                
            if power == 0:
                term = f"{coef}"
            elif power == 1:
                term = f"{coef}s" if coef != 1 else "s"
            else:
                term = f"{coef}s^{{{power}}}" if coef != 1 else f"s^{{{power}}}"
            
            terms.append(term)
        
        return " + ".join(terms) if terms else "0"
    
    def set_coefficients(self, num=None, den=None):
        """Update sensor coefficients"""
        if num is not None:
            self.num_coeffs = self._ensure_list(num)
        if den is not None:
            self.den_coeffs = self._ensure_list(den)
    
    def get_parameters(self):
        return {
            'Numerator': self.num_coeffs,
            'Denominator': self.den_coeffs
        }
    
    def get_parameter_descriptions(self):
        return{
            'Numerator': self.num_coeffs_description,
            'Denominator': self.den_coeffs_description
        }