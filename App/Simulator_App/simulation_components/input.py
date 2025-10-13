
class Input:
    def __init__(self, step_time=1, initial_value=0, final_value=1, total_time=10, sample_time=0.01):
        self.step_time = step_time
        self.initial_value = initial_value
        self.final_value = final_value
        self.total_time = total_time
        self.sample_time = sample_time
        self.step_time_description = ("Step Time:\nThe time at which the step changes from the initial value to the final value (seconds).\n")
        self.initial_value_description = ("Initial Value:\nThe value of the step input at the start of the simulation.\n")
        self.final_value_description = ("Final Value:\nThe value of the step input at the end of the simulation.\n")
        self.total_time_description = ("Total Time:\nThe total duration for which the step input is applied (seconds).\n")
        self.sample_time_description = ("Sample Time:\nThe discrete time interval (in seconds) between successive simulation points.\nThis parameter defines the sampling rate of the system and affects the accuracy of the response in discrete-time simulations."
        )


    def set_parameters(self, step_time, initial_value, final_value, total_time, sample_time):
        self.step_time = step_time
        self.initial_value = initial_value
        self.final_value = final_value
        self.total_time = total_time
        self.sample_time = sample_time
    
    def get_parameters(self):
        return {
            "step_time": self.step_time,
            "initial_value": self.initial_value,
            "final_value": self.final_value,
            "total_time": self.total_time,
            "sample_time": self.sample_time
        }
    
    def get_descriptions(self):
        return {
            "step_time": self.step_time_description,
            "initial_value": self.initial_value_description,
            "final_value": self.final_value_description,
            "total_time": self.total_time_description,
            "sample_time": self.sample_time_description
        }