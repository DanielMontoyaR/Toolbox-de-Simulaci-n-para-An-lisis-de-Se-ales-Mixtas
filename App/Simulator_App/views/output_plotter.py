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

class OutputPlotter(QDialog):
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
        plot_data = self.output.get_plot_data(plot_type)
        if plot_data:
            self.display_plot_data(plot_data, plot_type)        


    def display_plot_data(self, plot_data, plot_type):
        """Display the plot data on the canvas."""

        try:
            self.canvas.axes.clear()

            if plot_type == "Step Response" and plot_data["time"] is not None:
                self.plot_step_response(plot_data)

            elif plot_type == "Impulse Response" and plot_data["time"] is not None:
                self.plot_impulse_response(plot_data)
            
            elif plot_type == "Bode Plot" and plot_data["magnitude"] is not None:
                self.plot_bode(plot_data)
            
            elif plot_type == "Nyquist Plot":
                self.plot_nyquist(plot_data)
            
            elif plot_type == "Root Locus":
                self.plot_root_locus(plot_data)
            
            elif plot_type == "Real Time Response" and plot_data["time"] is not None:
                self.plot_real_time_response(plot_data)
            
            else:
                print("No valid data to plot.")
                return
        
            #Adjust layout after plotting
            self.canvas.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Error displaying plot data: {e}")


    def plot_step_response(self, plot_data):
        """Plot step response data."""

        # Clear plots
        self.canvas.figure.clear()
        self.canvas.axes = self.canvas.figure.add_subplot(111)


        time = plot_data["time"]
        response = plot_data["response"]
        kp = self.pid_controller.get_parameters()["kp"]
        ki = self.pid_controller.get_parameters()["ki"]
        kd = self.pid_controller.get_parameters()["kd"]

        self.canvas.axes.plot(time, response, 'b-', linewidth=2)
        self.canvas.axes.set_title(f'Step Response (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
        self.canvas.axes.set_xlabel('Time (s)')
        self.canvas.axes.set_ylabel('Amplitude')
        self.canvas.axes.grid(True, linestyle='--', alpha=0.7)
        self.canvas.axes.set_facecolor((0.95, 0.95, 0.95))


        # Adjust limits to improve visualization
        if len(time) > 0 and len(response) > 0:
            self.canvas.axes.set_xlim(left=0)
            # Adjust limits automatically
            y_min, y_max = min(response), max(response)
            y_range = y_max - y_min
            if y_range == 0:  # Prevent zero division
                y_range = 1
            self.canvas.axes.set_ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)


    def plot_impulse_response(self, plot_data):
        """Plot impulse response data"""

        # Clear plots
        self.canvas.figure.clear()
        self.canvas.axes = self.canvas.figure.add_subplot(111)

        time = plot_data["time"]
        response = plot_data["response"]
        kp = self.pid_controller.get_parameters()["kp"]
        ki = self.pid_controller.get_parameters()["ki"]
        kd = self.pid_controller.get_parameters()["kd"]

        self.canvas.axes.plot(time, response, 'r-', linewidth=2)
        self.canvas.axes.set_title(f'Impulse Response (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
        self.canvas.axes.set_xlabel('Time (s)')
        self.canvas.axes.set_ylabel('Amplitude')
        self.canvas.axes.grid(True, linestyle='--', alpha=0.7)
        self.canvas.axes.set_facecolor((0.95, 0.95, 0.95))
        
        # Adjust limits to improve visualization
        if len(time) > 0 and len(response) > 0:
            self.canvas.axes.set_xlim(left=0)
            y_min, y_max = min(response), max(response)
            y_range = y_max - y_min
            if y_range == 0:
                y_range = 1
            self.canvas.axes.set_ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)


    def plot_bode(self, plot_data):
        """Plot Bode diagram."""

        # Clear plots
        self.canvas.figure.clear()
        self.canvas.axes = self.canvas.figure.add_subplot(111)

        magnitude = plot_data["magnitude"]
        phase = plot_data["phase"]
        omega = plot_data["frequency"]
        
        kp = self.pid_controller.get_parameters()["kp"]
        ki = self.pid_controller.get_parameters()["ki"]
        kd = self.pid_controller.get_parameters()["kd"]
        
        #Create subplots for Bode
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
        
        self.canvas.figure.tight_layout()




    def plot_nyquist(self, plot_data):
        """Plot Nyquist diagram with all the features from control.nyquist_plot()"""
        # Clear plots
        self.canvas.figure.clear()
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        try:
            real = plot_data["real"]
            imag = plot_data["imag"]
            omega = plot_data.get("omega", None)
            
            if real is None or imag is None:
                print("No Nyquist data available")
                return

            kp = self.pid_controller.get_parameters()["kp"]
            ki = self.pid_controller.get_parameters()["ki"]
            kd = self.pid_controller.get_parameters()["kd"]

            

            # Plot main Nyquist curve (parte positiva de frecuencia)
            self.canvas.axes.plot(real, imag, 'b-', linewidth=2, label='Nyquist')
            
            # Plot reflected curve (parte negativa de frecuencia - simetría)
            self.canvas.axes.plot(real, -np.array(imag), 'b--', linewidth=1.5, alpha=0.7, label='Reflected')
            
            # Add direction arrows (every ~10% of the data points)
            if len(real) > 10 and omega is not None:
                # Select points for arrows (skip first and last few points)
                arrow_indices = np.linspace(2, len(real)-3, 6, dtype=int)
                
                for i in arrow_indices:
                    if i < len(real) - 1:
                        # Calculate direction vector
                        dx = real[i+1] - real[i]
                        dy = imag[i+1] - imag[i]
                        
                        # Normalize arrow length
                        length = np.sqrt(dx**2 + dy**2)
                        if length > 0:
                            dx = dx / length * 0.1 * max(np.abs(real))
                            dy = dy / length * 0.1 * max(np.abs(imag))
                        
                        # Add arrow
                        self.canvas.axes.arrow(real[i], imag[i], dx, dy, 
                                            head_width=0.05, head_length=0.1, 
                                            fc='red', ec='red', alpha=0.8)

            # Mark critical point (-1, 0j)
            self.canvas.axes.plot(-1, 0, 'ro', markersize=8, markerfacecolor='red', 
                                markeredgecolor='darkred', label='Critical Point (-1, 0j)')
            
            # Add a circle around critical point for better visibility
            critical_circle = matplotlib.patches.Circle((-1, 0), 0.1, color='red', fill=False, linestyle='--', alpha=0.5)
            self.canvas.axes.add_patch(critical_circle)

            # Set labels and title
            self.canvas.axes.set_title(f'Nyquist Diagram (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
            self.canvas.axes.set_xlabel('Real Axis')
            self.canvas.axes.set_ylabel('Imaginary Axis')
            self.canvas.axes.grid(True, linestyle='--', alpha=0.7)
            
            # Set aspect ratio to equal for proper scaling
            self.canvas.axes.set_aspect('equal', adjustable='datalim')
            
            # Add legend
            self.canvas.axes.legend(loc='upper right')
            
            # Auto-scale with some margin
            all_real = np.concatenate([real, -real])
            all_imag = np.concatenate([imag, -imag])
            
            x_margin = 0.1 * (np.max(all_real) - np.min(all_real))
            y_margin = 0.1 * (np.max(all_imag) - np.min(all_imag))
            
            self.canvas.axes.set_xlim(np.min(all_real) - x_margin, np.max(all_real) + x_margin)
            self.canvas.axes.set_ylim(np.min(all_imag) - y_margin, np.max(all_imag) + y_margin)

            # Draw the plot
            self.canvas.draw()

            print("Enhanced Nyquist plot displayed successfully")

        except Exception as e:
            print(f"Error displaying enhanced Nyquist data: {e}")






    def plot_root_locus(self, plot_data):
        """Plot Root Locus diagram using control's built-in function
        
        Args:
            plot_data (dict): Plot data from Output class (not used in this approach)
        """
        try:
            kp = self.pid_controller.get_parameters()["kp"]
            ki = self.pid_controller.get_parameters()["ki"]
            kd = self.pid_controller.get_parameters()["kd"]
            
            open_loop_tf = self.output.get_open_loop_transfer_function()
            
            # Clear the canvas and create fresh axes
            self.canvas.figure.clear()
            self.canvas.axes = self.canvas.figure.add_subplot(111)
            
            # Use control.root_locus to plot directly with all its features
            ctrl.root_locus(open_loop_tf, plot=True, grid=True, ax=self.canvas.axes)
            
            # Customize title and ensure consistent styling
            self.canvas.axes.set_title(f'Root Locus (Kp={kp}, Ki={ki}, Kd={kd})', pad=20)
            
            # Force consistent grid style
            self.canvas.axes.grid(True, linestyle='--', alpha=0.7)
            
            # Set consistent background color
            self.canvas.axes.set_facecolor((0.95, 0.95, 0.95))
            
            # Reset layout to maintain consistent appearance
            self.reset_canvas_layout()
            
            self.canvas.draw()
            print("Root Locus plotted successfully using control library")
            
        except Exception as e:
            print(f"Error displaying Root Locus: {e}")


    def reset_canvas_layout(self):
        """Reset canvas layout to maintain consistent appearance across all plots"""
        # Apply consistent margins for all plot types
        self.canvas.figure.subplots_adjust(
            left=0.15, 
            bottom=0.15, 
            right=0.95, 
            top=0.90
        )
        
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

