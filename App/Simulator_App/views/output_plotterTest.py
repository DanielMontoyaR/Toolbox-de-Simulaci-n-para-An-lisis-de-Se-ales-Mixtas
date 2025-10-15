import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5 import QtWidgets

import control as ctrl

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker

import numpy as np

from simulation_components.plant import Plant
from simulation_components.controller_pid import ControllerPID
from simulation_components.input import Input
from simulation_components.output import Output


matplotlib.use('Qt5Agg')

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

        fig.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.90)
        fig.tight_layout()

class OutputPlotterTest(QDialog):
    def __init__(self, plant_model: Plant, pid_controller: ControllerPID, input_signal: Input, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/output_plotter.ui")
        loadUi(ui_path, self)

        self.plant_model = plant_model
        self.pid_controller = pid_controller
        self.input_signal = input_signal

        # Business Logic 
        self.output = Output(pid_object=self.pid_controller, plant_object=self.plant_model, input_params=self.input_signal)

        #Config UI
        self.setup_ui()

        #Create and configure the matplotlib canvas
        self.setup_plot_canvas()



    def setup_ui(self):
        """Configure UI elements."""
        self.setWindowTitle(self.plant_model.name + " - Output Plotter")

        #labels
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setText(f"Output Plotter for {self.plant_model.name}")

        # Button Configuration
        self.plotButton.clicked.connect(self.plot_output)

        # Combobox configuration
        self.plotTypecomboBox.addItems(["Step Response", "Impulse Response", "Bode Plot", "Nyquist Plot", "Root Locus", "Real Time Response"])
        self.plotTypecomboBox.setCurrentIndex(0)
        self.plotTypecomboBox.currentIndexChanged.connect(self.on_plot_type_changed)

        # Inputs (Only in Real Time Response)
        regex = QRegExp(r"^-?\d+(\.\d{1,15})?$")  # Regex for float numbers with up to 15 decimal places
        validator = QRegExpValidator(regex)

        self.kpInput.setValidator(validator)
        self.kpInput.setDisabled(True)
        self.kiInput.setValidator(validator)
        self.kiInput.setDisabled(True)
        self.kdInput.setValidator(validator)
        self.kdInput.setDisabled(True)

        self.inputValueInput.setValidator(validator)
        self.inputValueInput.setDisabled(True)


    def setup_plot_canvas(self):
        """Set up the matplotlib canvas for plotting."""
        #Create canvas
        self.canvas = MplCanvas(self, width=10, height=6, dpi=80)

        """
        self.canvas.setStyleSheet("background-color: white;")

        #Replace widget layout with the canvas
        layout = self.widget.parent().layout()
        layout.replaceWidget(self.widget, self.canvas)
        self.widget.deleteLater()
        """

        plot_container = self.findChild(QtWidgets.QWidget, "widget")

        if plot_container:
            layout = QVBoxLayout(plot_container)
            layout.setContentsMargins(0,0,0,0)
            layout.setSpacing(0)
            layout.addWidget(self.canvas)

            self.canvas.setStyleSheet("background-color: white;")
            self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        else:
            print("Error: The widget that contains the graphs was not found")

    def plot_output(self):
        plot_type = self.plotTypecomboBox.currentText()
        self.display_plot_data(plot_type)


    def display_plot_data(self, plot_type):
        """Display the plot data on the canvas."""

        try:
            self.canvas.axes.clear()

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
                print("No valid data to plot.")
                return
        
            #Adjust layout after plotting
            self.canvas.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Error displaying plot data: {e}")


    def plot_step_response(self):
        """Plot Step Response using input parameters"""
        try:
            closed_loop_tf = self.output.get_closed_loop_transfer_function()
            if closed_loop_tf is None:
                print("No closed-loop transfer function available")
                return

            # Get ALL input parameters
            params = self.input_signal.get_parameters()
            step_time = params["step_time"]
            initial_value = params["initial_value"]
            final_value = params["final_value"]
            total_time = params["total_time"]
            sample_time = params["sample_time"]
            
            # Create time vector from 0 to total_time
            num_points = int(total_time / sample_time) + 1
            t = np.linspace(0, total_time, num_points)
            
            # Calculate step response (allway start at t=0)
            _, y_step = ctrl.step_response(closed_loop_tf, T=t)
            
            # Create the custom response:
            # - Before step_time: initial value
            # - After step_time: apply the scaled and shifted step response
            response = np.full_like(t, initial_value)
            
            # Find the index where step begins.
            step_index = np.argmax(t >= step_time)
            
            if step_index < len(t):
                # Apply the step response from step_time onwards
                step_duration = total_time - step_time
                step_time_points = int(step_duration / sample_time) + 1
                t_step = np.linspace(0, step_duration, step_time_points)
                
                # Recalculate step response for the duration of the step
                _, y_step_actual = ctrl.step_response(closed_loop_tf, T=t_step)
                
                # Apply amplitude
                amplitude = final_value - initial_value
                response[step_index:] = initial_value + amplitude * y_step_actual[:len(response[step_index:])]
            
            kp = self.pid_controller.get_parameters()["kp"]
            ki = self.pid_controller.get_parameters()["ki"]
            kd = self.pid_controller.get_parameters()["kd"]

            # Clear and plot
            self.canvas.figure.clear()
            self.canvas.axes = self.canvas.figure.add_subplot(111)
            self.canvas.axes.plot(t, response, 'b-', linewidth=2)
            self.canvas.axes.set_title(f'Step Response (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
            self.canvas.axes.set_xlabel('Time (s)')
            self.canvas.axes.set_ylabel('Amplitude')
            self.canvas.axes.grid(True, linestyle='--', alpha=0.7)
            self.canvas.axes.set_facecolor((0.95, 0.95, 0.95))

            # Mark step point
            self.canvas.axes.axvline(x=step_time, color='r', linestyle='--', alpha=0.7, label=f'Step at {step_time}s')
            self.canvas.axes.legend()

            # Set appropriate limits
            self.canvas.axes.set_xlim(0, total_time)

            print(f"Step response: step_time={step_time}, initial={initial_value}, final={final_value}, total_time={total_time}")

        except Exception as e:
            print(f"Error plotting step response: {e}")


    def plot_impulse_response(self):
        """Plot Impulse Response using input parameters"""
        try:
            closed_loop_tf = self.output.get_closed_loop_transfer_function()
            if closed_loop_tf is None:
                print("No closed-loop transfer function available")
                return

            # Get relevant input parameters
            params = self.input_signal.get_parameters()
            step_time = params["step_time"]  # Momento del impulso
            total_time = params["total_time"]
            sample_time = params["sample_time"]
            
            # Create time vector from 0 to total_time
            num_points = int(total_time / sample_time) + 1
            t = np.linspace(0, total_time, num_points)
            
            # Calculate impulse response (allways begins en t=0)
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
            
            kp = self.pid_controller.get_parameters()["kp"]
            ki = self.pid_controller.get_parameters()["ki"]
            kd = self.pid_controller.get_parameters()["kd"]

            # Clear and plot
            self.canvas.figure.clear()
            self.canvas.axes = self.canvas.figure.add_subplot(111)
            self.canvas.axes.plot(t, response, 'r-', linewidth=2)
            self.canvas.axes.set_title(f'Impulse Response (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
            self.canvas.axes.set_xlabel('Time (s)')
            self.canvas.axes.set_ylabel('Amplitude')
            self.canvas.axes.grid(True, linestyle='--', alpha=0.7)
            self.canvas.axes.set_facecolor((0.95, 0.95, 0.95))

            # Mark the impulse point
            self.canvas.axes.axvline(x=step_time, color='g', linestyle='--', alpha=0.7, label=f'Impulse at {step_time}s')
            self.canvas.axes.legend()

            # Set appropriate limits
            self.canvas.axes.set_xlim(0, total_time)

            print(f"Impulse response: impulse_time={step_time}, total_time={total_time}")

        except Exception as e:
            print(f"Error plotting impulse response: {e}")


    def plot_bode(self):
        """Plot Bode diagram directly using transfer functions"""
        try:
            # Get transfer function from output
            closed_loop_tf = self.output.get_closed_loop_transfer_function()
            if closed_loop_tf is None:
                print("No closed-loop transfer function available")
                return

            # Get PID parameters for title
            kp = self.pid_controller.get_parameters()["kp"]
            ki = self.pid_controller.get_parameters()["ki"]
            kd = self.pid_controller.get_parameters()["kd"]

            # Generate frequency range
            omega = np.logspace(-2, 3, 1000)
            
            # Calculate Bode data using control library
            magnitude, phase, omega = ctrl.bode(closed_loop_tf, omega=omega, plot=False, deg=False)
            
            # Clear and create subplots
            self.canvas.figure.clear()
            
            # Create subplots for Bode
            ax1 = self.canvas.figure.add_subplot(211)
            ax2 = self.canvas.figure.add_subplot(212)

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

        except Exception as e:
            print(f"Error plotting Bode diagram: {e}")


    def plot_nyquist(self):
        """Plot Nyquist diagram using control library's built-in function"""
        try:
            # Get transfer function from output
            closed_loop_tf = self.output.get_closed_loop_transfer_function()
            if closed_loop_tf is None:
                print("No closed-loop transfer function available")
                return

            # Get PID parameters for title
            kp = self.pid_controller.get_parameters()["kp"]
            ki = self.pid_controller.get_parameters()["ki"]
            kd = self.pid_controller.get_parameters()["kd"]

            # Clear and setup plot
            self.canvas.figure.clear()
            self.canvas.axes = self.canvas.figure.add_subplot(111)

            # Use control's built-in nyquist_plot
            ctrl.nyquist_plot(closed_loop_tf, 
                            omega_limits=(1e-2, 1e2),
                            omega_num=500,
                            plot=True,
                            ax=self.canvas.axes)

            # Customize the plot
            self.canvas.axes.set_title(f'Nyquist Diagram (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
            self.canvas.axes.grid(True, linestyle='--', alpha=0.7)

        except Exception as e:
            print(f"Error plotting Nyquist diagram: {e}")


    def plot_root_locus(self):
        """Plot Root Locus using control library's built-in function"""
        try:
            # Get open-loop transfer function from output
            open_loop_tf = self.output.get_open_loop_transfer_function()
            if open_loop_tf is None:
                print("No open-loop transfer function available")
                return

            # Get PID parameters for title
            kp = self.pid_controller.get_parameters()["kp"]
            ki = self.pid_controller.get_parameters()["ki"]
            kd = self.pid_controller.get_parameters()["kd"]

            # Clear and setup plot
            self.canvas.figure.clear()
            self.canvas.axes = self.canvas.figure.add_subplot(111)

            # Use control's built-in root_locus
            ctrl.root_locus(open_loop_tf, plot=True, grid=True, ax=self.canvas.axes)
            
            # Customize the plot
            self.canvas.axes.set_title(f'Root Locus (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
            self.canvas.axes.grid(True, linestyle='--', alpha=0.7)

        except Exception as e:
            print(f"Error plotting Root Locus: {e}")



    def on_plot_type_changed(self):
        selected = self.plotTypecomboBox.currentText()
        if selected == "Real Time Response":
            self.kpInput.setDisabled(False)
            self.kiInput.setDisabled(False)
            self.kdInput.setDisabled(False)
            self.inputValueInput.setDisabled(False)
        else:
            self.kpInput.setDisabled(True)
            self.kiInput.setDisabled(True)
            self.kdInput.setDisabled(True)
            self.inputValueInput.setDisabled(True)

