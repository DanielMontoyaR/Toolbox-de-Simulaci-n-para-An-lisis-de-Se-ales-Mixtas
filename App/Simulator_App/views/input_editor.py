import os
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from simulation_components.input import Input



class InputEditor(QDialog):
    def __init__(self, input_controller: Input, parent=None):
        super().__init__(parent)

        ui_path = os.path.join(os.path.dirname(__file__), "../ui/input_editor.ui")
        loadUi(ui_path, self)

        self.input_controller = input_controller

        # Input Validators
        validator = QDoubleValidator(-9999.0, 9999.0, 4)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.stepTimeInput.setValidator(validator)
        self.initialValueInput.setValidator(validator)
        self.finalValueInput.setValidator(validator)
        self.totalTimeInput.setValidator(validator)

        # Button Configuration
        self.applyButton.clicked.connect(self.apply_changes_to_model)
        self.cancelButton.clicked.connect(self.reject)

        # Set tooltips
        self.stepTimeLabelInfo.setToolTip(self.input_controller.get_descriptions()["step_time"])
        self.initialValueLabelInfo.setToolTip(self.input_controller.get_descriptions()["initial_value"])
        self.finalValueLabelInfo.setToolTip(self.input_controller.get_descriptions()["final_value"])
        self.totalTimeLabelInfo.setToolTip(self.input_controller.get_descriptions()["total_time"])

        # Load current values from the model (if any)
        self.load_from_model()

    def load_from_model(self):
        """Initialize the input fields with current input values"""
        params = self.input_controller.get_parameters()
        self.stepTimeInput.setText(str(params["step_time"]))
        self.initialValueInput.setText(str(params["initial_value"]))
        self.finalValueInput.setText(str(params["final_value"]))
        self.totalTimeInput.setText(str(params["total_time"]))

    def apply_changes_to_model(self):
        """Apply changes from input fields to the input model"""
        try:
            step_time = float(self.stepTimeInput.text())
            initial_value = float(self.initialValueInput.text())
            final_value = float(self.finalValueInput.text())
            total_time = float(self.totalTimeInput.text())
        except ValueError:
            # Handle invalid input (e.g., show an error message)
            print("Invalid input. Please enter valid numbers.")
            return
        
        self.input_controller.set_parameters(step_time, initial_value, final_value, total_time)
        print("Updated Input Parameters:", self.input_controller.get_parameters())
        self.accept()  # Close dialog and indicate success