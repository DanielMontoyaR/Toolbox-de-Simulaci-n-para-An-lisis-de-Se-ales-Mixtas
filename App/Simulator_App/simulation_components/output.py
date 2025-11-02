import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import io
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Output:
    def __init__(self, pid_object=None, plant_object=None, input_params=None, sensor_object=None):
        """
        Initialize Output with PID, Plant, Input Parameters, and Sensor objects
        Args:
            pid_object: PID controller object
            plant_object: Plant model object
            input_params: Input parameters for the simulation
            sensor_object: Sensor model object
        Returns:
            None
        """
        self.pid_object = pid_object
        self.plant_object = plant_object
        self.input_params = input_params
        self.sensor_object = sensor_object

    def get_pid_function(self):
        """"
        Return the PID controller object
        Args:
            None
        Returns:
            PID controller object
        """
        return self.pid_object

    def get_plant_function(self):
        """
        Return the Plant model object
        Args:
            None
        Returns:
            Plant model object
        """
        return self.plant_object
    
    def get_sensor_function(self):
        """
        Return the Sensor model object
        Args:
            None
        Returns:
            Sensor model object
        """
        return self.sensor_object

    def get_input_params(self):
        """
        Return the Input parameters for the simulation
        Args:
            None
        Returns:
            Input parameters object
        """
        return self.input_params
    

    
    # Métodos de transfer function
    def get_closed_loop_transfer_function(self):
        """
        Calculate the closed-loop transfer function: plant*pid / (1 + plant*pid*sensor)
        Args:
            None
        Returns:
            Closed-loop transfer function object
        """
        try:
            pid_tf = self.get_pid_function().get_transfer_function()
            plant_tf = self.get_plant_function().get_transfer_function()
            sensor_tf = self.get_sensor_function().get_transfer_function()

            open_loop = ctrl.series(plant_tf, pid_tf)
            #closed_loop = ctrl.feedback(open_loop, 1)
            closed_loop = ctrl.feedback(open_loop, sensor_tf) #plant*pid / (1 + plant*pid*sensor_tf)
            return closed_loop
        except Exception as e:
            #print(f"Error in calculating closed-loop transfer function: {e}")
            return None

    def get_open_loop_transfer_function(self):
        """
        Calculate the open-loop transfer function
        Args:
            None
        Returns:
            Open-loop transfer function object
        """
        try:
            pid_tf = self.get_pid_function().get_transfer_function()
            plant_tf = self.get_plant_function().get_transfer_function()

            open_loop = ctrl.series(plant_tf, pid_tf)
            return open_loop
        except Exception as e:
            #print(f"Error in calculating open-loop transfer function: {e}")
            return None

    # -------------------------------------- Plotting Methods     --------------------------------------
    def plot_step_response(self):
        """
        Plot Step Response and return the matplotlib Figure
        Args:
            None
        Returns:
            Matplotlib Figure object with the step response plot
        """
        try:
            closed_loop_tf = self.get_closed_loop_transfer_function()
            if closed_loop_tf is None:
                print("No closed-loop transfer function available")
                return None

            # Get input parameters
            params = self.input_params.get_parameters()
            step_time = params["step_time"]
            initial_value = params["initial_value"]
            final_value = params["final_value"]
            total_time = params["total_time"]
            sample_time = params["sample_time"]
            
            # Get PID parameters for title
            pid_params = self.pid_object.get_parameters()
            kp = pid_params["kp"]
            ki = pid_params["ki"]
            kd = pid_params["kd"]
            
            # Create time vector
            num_points = int(total_time / sample_time) + 1
            t = np.linspace(0, total_time, num_points)
            
            # Calculate step response
            _, y_step = ctrl.step_response(closed_loop_tf, T=t)
            
            # Create the custom response
            response = np.full_like(t, initial_value)
            step_index = np.argmax(t >= step_time)
            
            if step_index < len(t):
                step_duration = total_time - step_time
                step_time_points = int(step_duration / sample_time) + 1
                t_step = np.linspace(0, step_duration, step_time_points)
                
                _, y_step_actual = ctrl.step_response(closed_loop_tf, T=t_step)
                
                amplitude = final_value - initial_value
                response[step_index:] = initial_value + amplitude * y_step_actual[:len(response[step_index:])]
            
            # Create figure
            fig = Figure(figsize=(10, 6), dpi=80)
            ax = fig.add_subplot(111)
            
            # Plot
            ax.plot(t, response, 'b-', linewidth=2)
            ax.set_title(f'Step Response (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_facecolor((0.95, 0.95, 0.95))
            
            # Mark step point
            ax.axvline(x=step_time, color='r', linestyle='--', alpha=0.7, label=f'Step at {step_time}s')
            ax.legend()
            ax.set_xlim(0, total_time)
            
            fig.tight_layout()
            return fig

        except Exception as e:
            #print(f"Error plotting step response: {e}")
            return None

    def plot_impulse_response(self):
        """
        Plot Impulse Response and return the matplotlib Figure
        Args:
            None
        Returns:
            Matplotlib Figure object with the impulse response plot
        """
        try:
            closed_loop_tf = self.get_closed_loop_transfer_function()
            if closed_loop_tf is None:
                print("No closed-loop transfer function available")
                return None

            # Get relevant input parameters
            params = self.input_params.get_parameters()
            step_time = params["step_time"]
            total_time = params["total_time"]
            sample_time = params["sample_time"]
            
            # Get PID parameters for title
            pid_params = self.pid_object.get_parameters()
            kp = pid_params["kp"]
            ki = pid_params["ki"]
            kd = pid_params["kd"]
            
            # Create time vector from 0 to total_time
            num_points = int(total_time / sample_time) + 1
            t = np.linspace(0, total_time, num_points)
            
            # Calculate impulse response (siempre comienza en t=0)
            _, y_impulse = ctrl.impulse_response(closed_loop_tf, T=t)
            
            # Shift the impulse to step_time
            # Create a shifted response array
            response = np.zeros_like(t)
            
            # Find the index where the impulse occurs
            impulse_index = np.argmax(t >= step_time)
            
            if impulse_index < len(t):
                # Copy the shifted impulse response
                remaining_points = len(t) - impulse_index
                response[impulse_index:impulse_index + len(y_impulse)] = y_impulse[:remaining_points]
            
            # Create figure
            fig = Figure(figsize=(10, 6), dpi=80)
            ax = fig.add_subplot(111)
            
            # Plot
            ax.plot(t, response, 'r-', linewidth=2)
            ax.set_title(f'Impulse Response (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_facecolor((0.95, 0.95, 0.95))

            # Mark the impulse point
            ax.axvline(x=step_time, color='g', linestyle='--', alpha=0.7, label=f'Impulse at {step_time}s')
            ax.legend()

            # Set appropriate limits
            ax.set_xlim(0, total_time)
            
            # Adjust design
            fig.tight_layout()
            
            #print(f"Impulse response: impulse_time={step_time}, total_time={total_time}")
            return fig

        except Exception as e:
            #print(f"Error plotting impulse response: {e}")
            return None

    def plot_bode(self):
        """
        Plot Bode diagram and return the matplotlib Figure
        Args:
            None
        Returns:
            Matplotlib Figure object with the Bode plot
        """
        try:
            # Get transfer function from output
            closed_loop_tf = self.get_closed_loop_transfer_function()
            if closed_loop_tf is None:
                print("No closed-loop transfer function available")
                return None

            # Get PID parameters for title
            pid_params = self.pid_object.get_parameters()
            kp = pid_params["kp"]
            ki = pid_params["ki"]
            kd = pid_params["kd"]

            # Generate frequency range
            omega = np.logspace(-2, 3, 1000)
            
            # Calculate Bode data using control library
            magnitude, phase, omega = ctrl.bode(closed_loop_tf, omega=omega, plot=False, deg=False)
            
            # Create figure with subplots
            fig = Figure(figsize=(10, 8), dpi=80)
            
            # Create subplots for Bode
            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212)

            # Magnitude plot (convert to dB)
            ax1.semilogx(omega, 20 * np.log10(magnitude), 'b-', linewidth=2)
            ax1.set_title(f'Bode Diagram (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
            ax1.set_ylabel('Magnitude [dB]')
            ax1.grid(True, linestyle='--', alpha=0.7)
            
            # Phase plot (convert to degrees)
            ax2.semilogx(omega, np.degrees(phase), 'r-', linewidth=2)
            ax2.set_ylabel('Phase [deg]')
            ax2.set_xlabel('Frequency [rad/s]')
            ax2.grid(True, linestyle='--', alpha=0.7)

            fig.tight_layout()
            return fig

        except Exception as e:
            #print(f"Error plotting Bode diagram: {e}")
            return None

    def plot_nyquist(self):
        """
        Plot Nyquist diagram and return the matplotlib Figure
        Args:
            None
        Returns:
            Matplotlib Figure object with the Nyquist plot
        """
        try:
            # Get transfer function from output
            closed_loop_tf = self.get_closed_loop_transfer_function()
            if closed_loop_tf is None:
                print("No closed-loop transfer function available")
                return None

            # Get PID parameters for title
            pid_params = self.pid_object.get_parameters()
            kp = pid_params["kp"]
            ki = pid_params["ki"]
            kd = pid_params["kd"]

            # Create figure
            fig = Figure(figsize=(8, 8), dpi=80)
            ax = fig.add_subplot(111)

            # Use control's built-in nyquist_plot
            ctrl.nyquist_plot(closed_loop_tf, 
                            omega_limits=(1e-2, 1e2),
                            omega_num=500,
                            plot=True,
                            ax=ax)

            # Customize the plot
            ax.set_title(f'Nyquist Diagram (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
            ax.grid(True, linestyle='--', alpha=0.7)

            fig.tight_layout()
            return fig

        except Exception as e:
            #print(f"Error plotting Nyquist diagram: {e}")
            return None

    def plot_root_locus(self):
        """
        Plot Root Locus and return the matplotlib Figure
        Args:
            None
        Returns:
            Matplotlib Figure object with the Root Locus plot
        """
        try:
            # Get open-loop transfer function from output
            open_loop_tf = self.get_open_loop_transfer_function()
            if open_loop_tf is None:
                print("No open-loop transfer function available")
                return None

            # Get PID parameters for title
            pid_params = self.pid_object.get_parameters()
            kp = pid_params["kp"]
            ki = pid_params["ki"]
            kd = pid_params["kd"]

            # Create figure
            fig = Figure(figsize=(8, 8), dpi=80)
            ax = fig.add_subplot(111)

            # Use control's built-in root_locus
            ctrl.root_locus(open_loop_tf, plot=True, grid=True, ax=ax)
            
            # Customize the plot
            ax.set_title(f'Root Locus (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
            ax.grid(True, linestyle='--', alpha=0.7)

            fig.tight_layout()
            return fig

        except Exception as e:
            #print(f"Error plotting Root Locus: {e}")
            return None

    """
    def plot_real_time_response(self):
        # Plot Real Time Response and return the matplotlib Figure
        #print("Real time response plot not implemented yet")
        #return None
    """

    # auxiliary method to convert figure to QPixmap (Optional)
    def figure_to_qpixmap(self, fig):
        """
        Convert matplotlib figure to QPixmap
        Args:
            fig: Matplotlib Figure object
            
        Returns:
            QPixmap object
        """
        if fig is None:
            return None
            
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=80, bbox_inches='tight')
        buf.seek(0)
        
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue(), 'PNG')
        return pixmap