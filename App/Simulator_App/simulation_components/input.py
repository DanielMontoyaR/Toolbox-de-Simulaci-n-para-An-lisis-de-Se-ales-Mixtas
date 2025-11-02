import math

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.input_utils import must_be_nonnegative, must_be_positive, cannot_be_zero, must_be_negative

MIN_SAMPLES = 10
MAX_SAMPLES = 10000
class Input:
    def __init__(self, step_time=1, initial_value=0, final_value=1, total_time=10, sample_time=0.01):
        """
        Initialize the input parameters for the simulation.
        Args:
            step_time (float): Time at which the step changes from initial to final value
            initial_value (float): Initial value of the step input
            final_value (float): Final value of the step input
            total_time (float): Total time for the simulation
            sample_time (float): Time interval between samples
        Returns:
            None
        """

        self.step_time = step_time
        self.initial_value = initial_value
        self.final_value = final_value
        self.total_time = total_time
        self.sample_time = sample_time
        self.step_time_description = ("Step Time:\nThe time at which the step changes from the initial value to the final value (seconds).\n")
        self.initial_value_description = ("Initial Value:\nThe value of the step input at the start of the simulation.\n")
        self.final_value_description = ("Final Value:\nThe value of the step input at the end of the simulation.\n")
        self.total_time_description = ("Total Time:\nThe total duration for which the step input is applied (seconds).\n")
        self.sample_time_description = ("Sample Time:\nThis parameter defines the sampling rate of the system and affects the accuracy of the response in simulations."
        )


    def set_parameters(self, step_time, initial_value, final_value, total_time, sample_time):
        """
        Set the input parameters for the simulation.
        Args:
            step_time (float): Time at which the step changes from initial to final value
            initial_value (float): Initial value of the step input
            final_value (float): Final value of the step input
            total_time (float): Total time for the simulation
            sample_time (float): Time interval between samples
        Returns:
            error_log (str): Error messages if any validations fail, empty string otherwise
        """
        
        #Handle logic in case of invalid inputs
        errors = [
            must_be_nonnegative("Step Time", step_time),
            must_be_positive("Total Time", total_time),
            must_be_positive("Sample Time", sample_time),
        ]

        if step_time >= total_time:
            errors.append("Step time cannot be greater or equal than total time.")

        if initial_value < -100 or initial_value > 100:
            errors.append("Initial value must be between -100 and 100.")

        if final_value < -100 or final_value > 100:
            errors.append("Final value must be between -100 and 100.")

        if total_time > 1000:
            errors.append("Total time must be less than or equal to 1000 seconds.")


        # Sample Time constraints
        num_samples = total_time / sample_time

        # Secure at least MIN_SAMPLES samples
        if num_samples < MIN_SAMPLES:
            errors.append(f"Sample time is too large for the given total time; there should be at least {MIN_SAMPLES} samples (sample_time <= total_time / {MIN_SAMPLES}).")

        # Secure at most MAX_SAMPLES samples
        if num_samples > MAX_SAMPLES:
            errors.append(f"Sample time is too small leading to an excessive number of samples (> {MAX_SAMPLES}); increase sample_time.")

        # Sample Time must be a finite number
        if math.isnan(sample_time) or math.isinf(sample_time):
            errors.append("Sample time must be a finite number.")

        error_log = "\n".join(e for e in errors if e)
        
        if error_log:
            return error_log
        else:
            self.step_time = step_time
            self.initial_value = initial_value
            self.final_value = final_value
            self.total_time = total_time
            self.sample_time = sample_time
    
    def get_parameters(self):
        """
        Get the current input parameters for the simulation.
        Args:
            None
        Returns:
            dict: Dictionary with current input parameters
        """

        return {
            "step_time": self.step_time,
            "initial_value": self.initial_value,
            "final_value": self.final_value,
            "total_time": self.total_time,
            "sample_time": self.sample_time
        }
    
    def get_descriptions(self):
        """
        Get the descriptions of the input parameters.
        Args:
            None
        Returns:
            dict: Dictionary with descriptions of input parameters
        """

        return {
            "step_time": self.step_time_description,
            "initial_value": self.initial_value_description,
            "final_value": self.final_value_description,
            "total_time": self.total_time_description,
            "sample_time": self.sample_time_description
        }