# views/control_editor.py
import os
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from simulation_components.controller_pid import ControllerPID
from utils.input_utils import simulator_create_pixmap_equation
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
class ControlEditor(QDialog):
    def __init__(self, controller_pid: ControllerPID, parent=None):
        super().__init__(parent)

        ui_path = os.path.join(os.path.dirname(__file__), "../ui/control_editor.ui")
        loadUi(ui_path, self)

        self.controller_pid = controller_pid

        # Input Validators
        regex = QRegExp(r"^-?\d+(\.\d{1,15})?$")# Allow negative and decimal numbers up to 15 decimal places
        validator = QRegExpValidator(regex)
        self.kpInput.setValidator(validator)
        self.kiInput.setValidator(validator)
        self.kdInput.setValidator(validator)

        # PID label configuration
        self.pidLabel.setAlignment(Qt.AlignCenter)

        # Button Configuration
        self.applyButton.clicked.connect(self.apply_changes_to_model)
        self.cancelButton.clicked.connect(self.reject)

        # Real-time connection of inputs to labels
        self.kpInput.textChanged.connect(lambda text: self.update_pid_preview())
        self.kiInput.textChanged.connect(lambda text: self.update_pid_preview())
        self.kdInput.textChanged.connect(lambda text: self.update_pid_preview())

        # Initialize PID preview
        self.update_pid_preview()

        # Set tooltips
        self.kdLabelInfo.setToolTip(self.controller_pid.get_descriptions()["kd"])
        self.kpLabelInfo.setToolTip(self.controller_pid.get_descriptions()["kp"])
        self.kiLabelInfo.setToolTip(self.controller_pid.get_descriptions()["ki"])

        # Load current values from the model (if any)
        #self.load_from_model()

    def load_from_model(self):
        """Initialize the input fields with current controller values"""
        params = self.controller_pid.get_parameters()
        self.kpInput.setText(str(params["kp"]))
        self.kiInput.setText(str(params["ki"]))
        self.kdInput.setText(str(params["kd"]))

    def update_pid_preview(self):
        """Update the preview label with the current LaTeX PID equation"""
        kp = self.kpInput.text() or "Kp"
        ki = self.kiInput.text() or "Ki"
        kd = self.kdInput.text() or "Kd"

        latex_eq = self.controller_pid.get_latex_equation(kp, ki, kd)
        pixmap = simulator_create_pixmap_equation(latex_eq, fontsize=10)

        pixmap = pixmap.scaled(self.pidLabel.width(),
                               self.pidLabel.height(),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        self.pidLabel.setPixmap(pixmap)

    def apply_changes_to_model(self):
        """Update the controller_pid object with values from inputs"""
        try:
            params = self.controller_pid.get_parameters()
            kp = float(self.kpInput.text() or params["kp"])
            ki = float(self.kiInput.text() or params["ki"])
            kd = float(self.kdInput.text() or params["kd"])
        except ValueError as e:
            kp, ki, kd = params["kp"], params["ki"], params["kd"]
            print(f"Error applying changes: {e}")

            
        self.controller_pid.set_parameters(kp, ki, kd)
        self.accept()
