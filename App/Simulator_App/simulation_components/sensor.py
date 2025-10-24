from .plant import PersonalizedPlant

class Sensor(PersonalizedPlant):
    """
    Class representing a sensor component in a simulation environment.
    Inherits from PersonalizedPlant to utilize transfer function capabilities.
    """
    
    def __init__(self, num=None, den=None):
        super().__init__(num, den)
        self.name = "Sensor"
        
        # Personalize descriptions for sensor parameters
        self.DESCRIPTIONS = {
            'Numerator': 'Numerator: Sensor numerator coefficients (list)',
            'Denominator': 'Denominator: Sensor denominator coefficients (list)'
        }