import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5 import QtWidgets

import control as ctrl
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from simulation_components.input import Input
from simulation_components.controller_pid import ControllerPID
from simulation_components.plant import Plant
from simulation_components.sensor import Sensor
from simulation_components.output import Output

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        fig.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.90)
        fig.tight_layout()

class OutputPlotter(QDialog):
    def __init__(self, plant_model: Plant, pid_controller: ControllerPID, input_signal: Input, sensor_model: Sensor, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/output_plotter.ui")
        loadUi(ui_path, self)

        self.plant_model = plant_model
        self.pid_controller = pid_controller
        self.input_signal = input_signal

        print("Output Initialized:", sensor_model.get_latex_equation())
        # Business Logic 
        self.output = Output(pid_object=self.pid_controller, plant_object=self.plant_model, input_params=self.input_signal, sensor_object=sensor_model)

        # Config UI
        self.setup_ui()

        # Create and configure the matplotlib canvas
        self.setup_plot_canvas()

    def setup_ui(self):
        """Configure UI elements."""
        self.setWindowTitle(self.plant_model.name + " - Output Plotter")

        # Labels
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setText(f"Output Plotter for {self.plant_model.name}")

        # Button Configuration
        self.plotButton.clicked.connect(self.plot_output)

        # Combobox configuration
        self.plotTypecomboBox.addItems(["Step Response", "Impulse Response", "Bode Plot", "Nyquist Plot", "Root Locus", "Real Time Response"])
        self.plotTypecomboBox.setCurrentIndex(0)
        self.plotTypecomboBox.currentIndexChanged.connect(self.on_plot_type_changed)

        # Inputs (Only in Real Time Response)
        regex = QRegExp(r"^-?\d+(\.\d{1,15})?$")
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
        # Create canvas
        self.canvas = MplCanvas(self, width=10, height=6, dpi=80)

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
            # Get the complete figure from OutputTest
            if plot_type == "Step Response":
                fig = self.output.plot_step_response()
            
            elif plot_type == "Impulse Response":
                fig = self.output.plot_impulse_response()
            
            elif plot_type == "Bode Plot":
                fig = self.output.plot_bode()
            
            elif plot_type == "Nyquist Plot":
                fig = self.output.plot_nyquist()
            
            elif plot_type == "Root Locus":
                fig = self.output.plot_root_locus()
            
            elif plot_type == "Real Time Response":
                fig = self.output.plot_real_time_response()
            
            else:
                print("No valid plot type selected.")
                return

            # If we got a valid figure, replace the canvas content
            if fig is not None:
                # Get plot container
                plot_container = self.findChild(QtWidgets.QWidget, "widget")
                
                if plot_container:
                    # Clean actual layout
                    layout = plot_container.layout()
                    if layout:
                        # Remove old canvas
                        for i in reversed(range(layout.count())):
                            layout.itemAt(i).widget().setParent(None)
                    
                    # Create new canvas with new figure
                    new_canvas = FigureCanvas(fig)
                    new_canvas.setStyleSheet("background-color: white;")
                    new_canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                    
                    # Add to layout
                    layout.addWidget(new_canvas)
                    
                    # Replace canvas reference
                    self.canvas = new_canvas
                    
                    # Adjust Size
                    self.canvas.draw()
                    plot_container.updateGeometry()
                    
            else:
                print(f"No figure returned for {plot_type}")

        except Exception as e:
            print(f"Error displaying plot data: {e}")

    def on_plot_type_changed(self):
        """Enable inputs if the user selects a Real Time Step Response"""
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

    def resizeEvent(self, event):
        """Handle resize events to adjust the canvas"""
        super().resizeEvent(event)
        if hasattr(self, 'canvas') and self.canvas.figure:
            # Ajustar el tamaño de la figura al canvas
            self.canvas.figure.tight_layout()
            self.canvas.draw()