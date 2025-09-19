
class ControllerPID:
    def __init__(self, Kp=0.0, Ki=0.0, Kd=0.0):
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.Kd = Kd  # Derivative gain
        self.Kp_description = ("Proportional Gain (Kp):\n"
                                    "Determines the reaction to the current error.\n"
                                    "Higher Kp values result in a larger control action for a given error,\n"
                                    "which can reduce rise time but may increase overshoot and lead to instability.")
        
        self.Kd_description = ("Derivative Gain (Kd):\n"
                                    "Influences the system's response to the rate of change of the error.\n"
                                    "Higher Kd values can help reduce overshoot and improve stability,\n"
                                    "but may also lead to increased sensitivity to noise.")
        
        self.Ki_description = ("Integral Gain (Ki):\n"
                                    "Addresses accumulated past errors.\n"
                                    "Higher Ki values can eliminate steady-state error,\n"
                                    "but may also lead to increased overshoot and oscillations.")

    def set_parameters(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def get_parameters(self):
        return {"kp": self.Kp, "ki": self.Ki, "kd": self.Kd}
    
    def get_descriptions(self):
        return {"kp": self.Kp_description, "ki": self.Ki_description, "kd": self.Kd_description}