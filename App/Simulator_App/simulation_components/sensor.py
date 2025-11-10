from .plant import PersonalizedPlant

class Sensor(PersonalizedPlant):
    """
    Class representing a sensor component in a simulation environment.
    Inherits from PersonalizedPlant to utilize transfer function capabilities.
    """
    
    def __init__(self, Numerator=None, Denominator=None):
        """
        Initialize the Sensor with given numerator and denominator coefficients.
        Args:
            Numerator (list): Numerator coefficients of the sensor transfer function
            Denominator (list): Denominator coefficients of the sensor transfer function
        Returns:
            None
        """
        super().__init__(Numerator, Denominator)
        self.name = "Sensor"
        self.sensor_description = ("Sensor Block:\n"
                    "A component that measures the system output and provides feedback to the controller.\n"
                    "It converts the physical quantity (e.g., temperature, speed, position) into a measurable signal.\n"
                    "This signal is compared with the reference input to calculate the control error.\n"
                    "The sensor's accuracy and response time directly affect the system's performance.\n\n"
                    "An ideal sensor is modeled with a transfer function of 1")

        
        # Personalize descriptions for sensor parameters
        self.DESCRIPTIONS = {
            'Numerator': 'Numerator: Sensor numerator coefficients (list)',
            'Denominator': 'Denominator: Sensor denominator coefficients (list)'
        }

    def get_component_description(self):
        """
        Get the description of the Sensor component
        Args:
            None
        Returns:
            str: Description of the Sensor component

        """
        return self.sensor_description