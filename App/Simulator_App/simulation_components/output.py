

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

    def plot_output(self, plot_type):
        if plot_type == "Step Response":
            self.plot_step_response()
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


    def plot_step_response(self):
        print("Plotting step response...")
        pass

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