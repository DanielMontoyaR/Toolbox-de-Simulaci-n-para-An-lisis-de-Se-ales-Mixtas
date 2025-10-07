
import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
class Output:
    def __init__(self, pid_function=None, plant_function=None, input_params=None):
        self.pid_function = pid_function
        self.plant_function = plant_function
        self.input_params = input_params

    def get_pid_function(self):
        return self.pid_function

    def get_plant_function(self):
        return self.plant_function

    def get_input_params(self):
        return self.input_params
    
    def set_pid_function(self, pid_function):
        self.pid_function = pid_function
    
    def set_plant_function(self, plant_function):
        self.plant_function = plant_function

    def set_input_params(self, input_params):
        self.input_params = input_params


    #Output methods

    def get_plot_data(self, plot_type):
        if plot_type == "Step Response":
            time, response = self.plot_step_response()
            return {"time": time, "response": response, "type": "step"}
        elif plot_type == "Impulse Response":
            self.plot_impulse_response()
        elif plot_type == "Bode Plot":
            self.plot_bode()
        elif plot_type == "Nyquist Plot":
            self.plot_nyquist()
        elif plot_type == "Root Locus":
            self.plot_root_locus()
        elif plot_type == "Real Time Response":
            self.plot_real_time_response()
        else:
            print("Unknown plot type")

    def get_closed_loop_transfer_function(self):
        """Calculate the closed-loop transfer function: plant*pid / (1 + plant*pid)"""

        try:
            pid_tf = self.get_pid_function().get_transfer_function()
            plant_tf = self.get_plant_function().get_transfer_function()

            open_loop = ctrl.series(plant_tf, pid_tf)
            closed_loop = ctrl.feedback(open_loop, 1)

            return closed_loop
        except Exception as e:
            print(f"Error in calculating closed-loop transfer function: {e}")
            return None



    def plot_step_response(self):

        try:
            time_range = self.get_input_params().get_parameters()["total_time"]
            closed_loop_tf = self.get_closed_loop_transfer_function()
            print("Closed-loop TF:", closed_loop_tf)
            if closed_loop_tf is None:
                print("Closed-loop transfer function is None.")
                return None, None
            
            #Calculate step response
            input_amplitude = self.get_input_params().get_parameters()["amplitude"]
            time, response = ctrl.step_response(input_amplitude*closed_loop_tf, T=time_range)
            print("Step response calculated.")
            print("Time:", time)
            print("Response:", response)
            return time, response
        
        except Exception as e:
            print(f"Error in plotting step response: {e}")
            return None, None



    def plot_impulse_response(self):
        print("Plotting impulse response...")
        pass

    def plot_bode(self):
        print("Plotting Bode plot...")
        pass

    def plot_nyquist(self):
        print("Plotting Nyquist plot...")
        pass

    def plot_root_locus(self):
        print("Plotting root locus...")
        pass

    def plot_real_time_response(self):
        print("Plotting real-time response...")
        pass