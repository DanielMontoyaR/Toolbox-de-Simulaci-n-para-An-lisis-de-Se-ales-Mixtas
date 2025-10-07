import os
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker

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
        self.output = Output(pid_function=self.pid_controller, plant_function=self.plant_model, input_params=self.input_signal)

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
        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        self.canvas.setStyleSheet("background-color: white;")

        #Replace widget layout with the canvas
        layout = self.widget.parent().layout()
        layout.replaceWidget(self.widget, self.canvas)
        self.widget.deleteLater()

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
            elif plot_type == "Nyquist Plot" and plot_data["real"] is not None:
                self.plot_nyquist(plot_data)
            elif plot_type == "Root Locus" and plot_data["real"] is not None:
                self.plot_root_locus(plot_data)
            elif plot_type == "Real Time Response" and plot_data["time"] is not None:
                self.plot_real_time_response(plot_data)
            else:
                print("No valid data to plot.")
                return
        
            self.canvas.draw()
        except Exception as e:
            print(f"Error displaying plot data: {e}")


    def plot_step_response(self, plot_data):
        """Plot step response data."""
        time = plot_data["time"]
        response = plot_data["response"]
        kp = self.pid_controller.get_parameters()["kp"]
        ki = self.pid_controller.get_parameters()["ki"]
        kd = self.pid_controller.get_parameters()["kd"]

        self.canvas.axes.plot(time, response, 'b-', linewidth=2)
        self.canvas.axes.set_title(f'Step Response (kp={kp}, ki={ki}, kd={kd})')
        self.canvas.axes.set_xlabel('Time (s)')
        self.canvas.axes.set_ylabel('Amplitude')
        self.canvas.axes.grid(True, linestyle='--', alpha=0.7)
        self.canvas.axes.set_facecolor((0.95, 0.95, 0.95))

    def on_plot_type_changed(self, index):
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

