
import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
class Output:
    def __init__(self, pid_object=None, plant_object=None, input_params=None):
        self.pid_object = pid_object
        self.plant_object = plant_object
        self.input_params = input_params

    def get_pid_function(self):
        return self.pid_object

    def get_plant_function(self):
        return self.plant_object

    def get_input_params(self):
        return self.input_params
    
    def set_pid_function(self, pid_function):
        self.pid_object = pid_function
    
    def set_plant_function(self, plant_function):
        self.plant_object = plant_function

    def set_input_params(self, input_params):
        self.input_params = input_params


    #Output methods

    def get_plot_data(self, plot_type):
        """Get plot data based on the specified plot type
        
        Args:
            plot_type (str): Type of plot to generate
            
        Returns:
            dict: Plot data in a format specific to the plot type
        """
        if plot_type == "Step Response":
            time, response = self.plot_step_response()
            return {"time": time, "response": response, "type": "step"}
        
        elif plot_type == "Impulse Response":
            time, response = self.plot_impulse_response()
            return {"time": time, "response": response, "type": "impulse"}
        
        elif plot_type == "Bode Plot":
            magnitude, phase, omega = self.plot_bode()
            return {"magnitude": magnitude, "phase": phase, "frequency": omega, "type": "bode"}
        
        elif plot_type == "Nyquist Plot":
            nyquist_data = self.plot_nyquist()
            return nyquist_data
        
        elif plot_type == "Root Locus":
            root_locus_data = self.plot_root_locus()
            return root_locus_data

        elif plot_type == "Real Time Response":
            self.plot_real_time_response()

        else:
            print("Unknown plot type")
            return None

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


    def get_open_loop_transfer_function(self):
        """Calculate the open-loop transfer function"""
        try:
            pid_tf = self.get_pid_function().get_transfer_function()
            plant_tf = self.get_plant_function().get_transfer_function()

            open_loop = ctrl.series(plant_tf, pid_tf)

            return open_loop
        except Exception as e:
            print(f"Error in calculating closed-loop transfer function: {e}")
            return None


    def plot_step_response(self):
        try:
            params = self.get_input_params().get_parameters()
            total_time = params["total_time"]
            sample_time = params["sample_time"]
            closed_loop_tf = self.get_closed_loop_transfer_function()

            if closed_loop_tf is None:
                return None, None
            
            # Use sample_time for appropriate resolution
            num_points = int(total_time / sample_time) + 1
            t = np.linspace(0, total_time, num_points)
            
            # Calculate basic step response (from 0 to 1)
            _, y = ctrl.step_response(closed_loop_tf, T=t)
            
            # Apply custom step parameters
            amplitude = params["final_value"] - params["initial_value"]
            response = params["initial_value"] + amplitude * y
            
            # Adjust time for step_time offset
            time = t + params["step_time"]
            
            #print("Step response calculated with sample_time:", sample_time)
            return time, response
            
        except Exception as e:
            print(f"Error in plotting step response: {e}")
            return None, None



    def plot_impulse_response(self):
        """Calculate impulse response data using sample_time"""
        try:
            params = self.get_input_params().get_parameters()
            total_time = params["total_time"]
            sample_time = params["sample_time"]
            
            closed_loop_tf = self.get_closed_loop_transfer_function()
            
            if closed_loop_tf is None:
                return None, None
            
            # Use sample_time to create appropriate time vector
            # Number of points based on total_time and sample_time
            num_points = int(total_time / sample_time) + 1
            time = np.linspace(0, total_time, num_points)
            
            # Calculate impulse response
            time, response = ctrl.impulse_response(closed_loop_tf, T=time)
            
            print("Impulse response calculated with sample_time:", sample_time)
            return time, response
            
        except Exception as e:
            print(f"Error in plotting impulse response: {e}")
            return None, None

    def plot_bode(self):
        """Calculate Bode plot data using the old reliable method"""
        try:
            params = self.get_input_params().get_parameters()
            total_time = params["total_time"]
            
            closed_loop_tf = self.get_closed_loop_transfer_function()
            
            if closed_loop_tf is None:
                return None, None, None
            
            # Generate frequency range
            omega_min = 0.1
            omega_max = 1000.0
            omega = np.logspace(np.log10(omega_min), np.log10(omega_max), 1000)
            
            # ctrt.bode 
            magnitude, phase, omega = ctrl.bode(closed_loop_tf, omega=omega, plot=False, deg=False)
            
            # Flatten if necesary
            magnitude = np.squeeze(magnitude)
            phase = np.squeeze(phase)
            
            print("Bode plot calculated.")
            return magnitude, phase, omega
            
        except Exception as e:
            print(f"Error in plotting Bode: {e}")
            return None, None, None

    def plot_nyquist(self):
        """Compute Nyquist plot data instead of directly plotting it"""
        try:
            closed_loop_tf = self.get_closed_loop_transfer_function()
            if closed_loop_tf is None:
                return None

            # Frequency range
            omega = np.logspace(-2, 3, 1000)

            # Compute response for each frequency point
            response = [ctrl.evalfr(closed_loop_tf, 1j * w) for w in omega]

            # Extract real and imaginary parts
            real_part = np.real(response)
            imag_part = np.imag(response)

            return {
                "real": real_part,
                "imag": imag_part,
                "omega": omega,
                "type": "nyquist"
            }

        except Exception as e:
            print(f"Error in Nyquist calculation: {e}")
            return None


    def plot_root_locus(self):
        """Calculate Root Locus plot data
        
        Returns:
            dict: Indicator that root locus should be plotted
        """
        try:
            # Just return an indicator, the actual plotting happens in output_plotter
            return {
                "type": "root_locus",
                "plot_ready": True
            }
        except Exception as e:
            print(f"Error in Root Locus calculation: {e}")
            return None

    def plot_real_time_response(self):
        print("Plotting real-time response...")
        pass