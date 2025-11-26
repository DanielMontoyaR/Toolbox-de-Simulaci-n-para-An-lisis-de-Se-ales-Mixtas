import os
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from simulation_components.input import Input
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp



class InputEditor(QDialog):
    def __init__(self, input_controller: Input, parent=None):
        """
        Dialog for editing Input parameters.
        Args:
            input_controller (Input): The Input controller object to edit.
        Returns:
            None
        """
        super().__init__(parent)

        ui_path = os.path.join(os.path.dirname(__file__), "../ui/input_editor.ui")
        loadUi(ui_path, self)

        self.input_controller = input_controller

        # Input Validators
        regex = QRegExp(r"^\d+(\.\d{1,4})?$")  # Allow only non-negative decimal numbers 
        validator = QRegExpValidator(regex)

        regex_initial_final = QRegExp(r"^-?\d+(\.\d{1,4})?$")  # Allow negative and decimal numbers for initial and final values
        validator_initial_final = QRegExpValidator(regex_initial_final)
        self.stepTimeInput.setValidator(validator)
        self.initialValueInput.setValidator(validator_initial_final)
        self.finalValueInput.setValidator(validator_initial_final)
        self.totalTimeInput.setValidator(validator)
        self.sampleTimeInput.setValidator(validator)

        # Button Configuration
        self.applyButton.clicked.connect(self.apply_changes_to_model)
        self.cancelButton.clicked.connect(self.reject)
        self.clearButton.clicked.connect(self.clear_inputs)

        # Set tooltips
        self.stepTimeLabelInfo.setToolTip(self.input_controller.get_descriptions()["step_time"])
        self.initialValueLabelInfo.setToolTip(self.input_controller.get_descriptions()["initial_value"])
        self.finalValueLabelInfo.setToolTip(self.input_controller.get_descriptions()["final_value"])
        self.totalTimeLabelInfo.setToolTip(self.input_controller.get_descriptions()["total_time"])
        self.sampleTimeLabelInfo.setToolTip(self.input_controller.get_descriptions()["sample_time"])

        # Load current values from the model (if any)
        self.load_from_model()

        # Hide error labels initially
        self.errorLabel.hide()
        self.errorLabelInfo.hide()

    def load_from_model(self):
        """
        Initialize the input fields with current input values
        Args:
            None
        Returns:
            None
        """
        params = self.input_controller.get_parameters()
        self.stepTimeInput.setText(str(params["step_time"]))
        self.initialValueInput.setText(str(params["initial_value"]))
        self.finalValueInput.setText(str(params["final_value"]))
        self.totalTimeInput.setText(str(params["total_time"]))
        self.sampleTimeInput.setText(str(params["sample_time"]))

    def apply_changes_to_model(self):
        """
        Apply changes from input fields to the input model
        Args:
            None
        Returns:
            None
        """
        try:
            params = self.input_controller.get_parameters()
            step_time = float(self.stepTimeInput.text() or params["step_time"])
            initial_value = float(self.initialValueInput.text() or params["initial_value"])
            final_value = float(self.finalValueInput.text() or params["final_value"])
            total_time = float(self.totalTimeInput.text() or params["total_time"])
            sample_time = float(self.sampleTimeInput.text() or params["sample_time"])
        except ValueError:
            # Handle invalid input (e.g., show an error message)
            #print("Invalid input. Please enter valid numbers.")
            self.errorLabel.show()
            self.errorLabelInfo.show()
            self.errorLabelInfo.setToolTip("Please enter valid numeric values for all fields.")
            return
        
        old_params = self.input_controller.get_parameters()
        response = self.input_controller.set_parameters(step_time, initial_value, final_value, total_time, sample_time)
        if isinstance(response, str):
            # There were errors; show them
            self.errorLabel.show()
            self.errorLabelInfo.show()
            self.errorLabelInfo.setToolTip(response) # Show error message as tooltip
            self.input_controller.set_parameters(**old_params)  # Revert to old parameters
            return
        else:
            self.errorLabel.hide()
            self.errorLabelInfo.hide()
            print("Updated Input Parameters:", self.input_controller.get_parameters())
            self.accept()  # Close dialog and indicate success

    def clear_inputs(self):
        """
        Clear all input fields
        Args:
            None
        Returns:
            None
        """
        self.stepTimeInput.clear()
        self.initialValueInput.clear()
        self.finalValueInput.clear()
        self.totalTimeInput.clear()
        self.sampleTimeInput.clear()