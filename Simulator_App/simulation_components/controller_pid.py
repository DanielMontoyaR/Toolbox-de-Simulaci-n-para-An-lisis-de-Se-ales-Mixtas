#Scientific imports
import control as ctrl

class ControllerPID:
    def __init__(self, Kp=1.0, Ki=1.0, Kd=1.0):
        """
        Initialize a PID controller with given parameters.
        Args:
            Kp (float): Proportional gain
            Ki (float): Integral gain
            Kd (float): Derivative gain
        Returns:
            None
        """
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
        
        self.Controller_PID_description = ("PID Controller:\n"
                                "A control system that combines three corrective actions to minimize error:\n"
                                "Proportional (P): Kp responds to the current error\n"
                                "Integral (I): Ki removes accumulated (steady-state) error\n"
                                "Derivative (D): Kd anticipates future error based on the rate of change\n\n"
                                "Overall Transfer Function: Kp + Ki/s + Kd·s")


    def set_parameters(self, Kp, Ki, Kd):
        """
        Set the PID controller parameters.
        Args:
            Kp (float): Proportional gain
            Ki (float): Integral gain
            Kd (float): Derivative gain
        Returns:
            None
        """

        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def get_parameters(self):
        """
        Get the current PID controller parameters.
        Args:
            None
        Returns:
            dict: Dictionary with keys 'kp', 'ki', 'kd' and their corresponding values
        """
        return {
            "kp": self.Kp, 
            "ki": self.Ki, 
            "kd": self.Kd
        }
    
    def get_descriptions(self):
        """
        Get the descriptions of the PID controller parameters.
        Args:
            None
        Returns:
            dict: Dictionary with keys 'kp', 'ki', 'kd' and their corresponding descriptions
        """
        return {
            "kp": self.Kp_description, 
            "ki": self.Ki_description, 
            "kd": self.Kd_description
        }
    
    def get_transfer_function(self):
        """
        Return the PID controller transfer function: Kp + Ki/s + Kd*s
        Args:
            None
        Returns:
            ctrl.TransferFunction: The PID transfer function
        """
        s = ctrl.TransferFunction.s
        pid_tf = self.Kp + self.Ki / s + self.Kd * s
        return pid_tf
    
    def get_latex_equation(self, kp=None, ki=None, kd=None):
        """
        Return the LaTex equation using actual values or alternatives
        Args:
            kp: Value to use for Kp in the equation (str or float). If None, uses self.Kp or "Kp"
            ki: Value to use for Ki in the equation (str or float). If None, uses self.Ki or "Ki"
            kd: Value to use for Kd in the equation (str or float). If None, uses self.Kd or "Kd"
        Returns:
            str: LaTex formatted PID equation
        """
        kp_str = str(kp) if kp is not None else (str(self.Kp) if self.Kp != 0 else "Kp")
        ki_str = str(ki) if ki is not None else (str(self.Ki) if self.Ki != 0 else "Ki")
        kd_str = str(kd) if kd is not None else (str(self.Kd) if self.Kd != 0 else "Kd")

        return r"$%s + \frac{%s}{s} + %s\,s$" % (kp_str, ki_str, kd_str)
    
    def get_component_description(self):
        """
        Get the description of the PID controller component
        Args:
            None
        Returns:
            str: Description of the PID controller component
        """
        return self.Controller_PID_description