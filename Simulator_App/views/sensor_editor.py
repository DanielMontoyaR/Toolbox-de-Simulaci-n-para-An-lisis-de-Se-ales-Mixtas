# Standard library imports
import os

# Third-party imports
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, QLocale

# Local application imports
from simulation_components.sensor import Sensor
from utils.input_utils import simulator_create_pixmap_equation


class SensorEditor(QDialog):
    def __init__(self, sensor_controller: Sensor, parent=None):
        """
        Dialog for editing Sensor parameters.
        Args:
            sensor_controller (Sensor): The Sensor controller object to edit.
        Returns:
            None
        """
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/sensor_editor.ui")
        loadUi(ui_path, self)

        self.sensor_controller = sensor_controller

        self.setWindowTitle(sensor_controller.name + " Editor")
        self.errorLabel.hide()
        self.errorLabelInfo.hide()

        # Button Configuration
        self.applyButton.clicked.connect(self.apply_changes_to_model)
        self.cancelButton.clicked.connect(self.reject)
        self.clearButton.clicked.connect(self.clear_inputs)

        # Sensor label configuration
        self.sensorLabel.setAlignment(Qt.AlignCenter)

        # Set tooltips
        self.sensorNumeratorLabelInfo.setToolTip(self.sensor_controller.get_parameter_descriptions()["Numerator"])
        self.sensorDenominatorLabelInfo.setToolTip(self.sensor_controller.get_parameter_descriptions()["Denominator"])

        # Configure validators for polynomial inputs
        regex = QRegExp(r"^-?\d{1,6}(\.\d{1,15})?(,-?\d{1,6}(\.\d{1,15})?)*$")
        validator = QRegExpValidator(regex)
        
        self.sensorNumeratorInput.setValidator(validator)
        self.sensorDenominatorInput.setValidator(validator)
        
        self.sensorNumeratorInput.setPlaceholderText("e.g., 1, 0, 5 for s^2 + 5")
        self.sensorDenominatorInput.setPlaceholderText("e.g., 1, 0, 5 for s^2 + 5")

        # Real-time connection of inputs to preview
        self.sensorNumeratorInput.textChanged.connect(self.update_sensor_preview)
        self.sensorDenominatorInput.textChanged.connect(self.update_sensor_preview)
        
        # Initialize Sensor Label Preview
        self.update_sensor_preview()

        # Load current values from the model
        self.load_from_model()

    def load_from_model(self):
        """
        Initialize the input fields with current controller values
        Args:
            None
        Returns:
            None
        """
        params = self.sensor_controller.get_parameters()
        #print("Loading sensor parameters:", params)
        
        # Convert numerator list to comma-separated string
        if 'Numerator' in params:
            num_list = params['Numerator']
            # If it's a list, convert to string
            if isinstance(num_list, list):
                num_str = ", ".join(map(str, num_list))
            else:
                num_str = str(num_list)
            self.sensorNumeratorInput.setText(num_str)
        
        # Convert denominator list to comma-separated string
        if 'Denominator' in params:
            den_list = params['Denominator']
            # If it's a list, convert to string
            if isinstance(den_list, list):
                den_str = ", ".join(map(str, den_list))
            else:
                den_str = str(den_list)
            self.sensorDenominatorInput.setText(den_str)
            
    def update_sensor_preview(self):
        """
        Update the sensor preview label
        Args:
            None
        Returns:
            None
        """
        try:
            # Take values from inputs
            params = {}
            
            num_text = self.sensorNumeratorInput.text()
            den_text = self.sensorDenominatorInput.text()
            
            if num_text:
                params['Numerator'] = num_text
            if den_text:
                params['Denominator'] = den_text
            
            # Ask sensor controller for LaTeX equation
            latex_eq = self.sensor_controller.get_latex_equation(**params)
            
            pixmap = simulator_create_pixmap_equation(latex_eq, fontsize=10)
            pixmap = pixmap.scaled(
                self.sensorLabel.width(),
                self.sensorLabel.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.sensorLabel.setPixmap(pixmap)
        
        except Exception as e:
            # If there's an error, show a message or leave the preview empty
            #print(f"Error updating preview: {e}")
            # Optional: show an error message in the preview
            self.sensorLabel.setText("Error: Invalid input")

    def apply_changes_to_model(self):
        """
        Apply changes from input fields to the sensor controller
        Args:
            None
        Returns:
            None
        """
        params = {}
        
        # Collect values from input fields
        num_text = self.sensorNumeratorInput.text()
        den_text = self.sensorDenominatorInput.text()
        
        if num_text:
            params['Numerator'] = num_text
        if den_text:
            params['Denominator'] = den_text

        # Save old parameters for comparison
        old_params = self.sensor_controller.get_parameters().copy()

        # Use the names expected by Sensor (that extends PersonalizedPlant)
        self.sensor_controller.set_parameters(
            Numerator=params.get('Numerator'), 
            Denominator=params.get('Denominator')
        )
        
        tf = self.sensor_controller.get_transfer_function()

        if isinstance(tf, str):  # An error message was returned
            # Revert to old parameters
            self.sensor_controller.set_parameters(
                Numerator=old_params.get('Numerator'),
                Denominator=old_params.get('Denominator')
            )
            self.errorLabel.show()
            self.errorLabelInfo.show()
            self.errorLabelInfo.setToolTip(tf)  # Show error message as tooltip
            return
        else:
            self.errorLabel.hide()
            self.errorLabelInfo.hide()
            #print("Sensor parameters updated")
            #print(self.sensor_controller.get_parameters())
            #print("Sensor Transfer Function:")
            #print(self.sensor_controller.get_transfer_function())
            self.accept()  # Close dialog with Accepted status

    def clear_inputs(self):
        """
        Clear all input fields
        Args:
            None
        Returns:
            None
        """
        self.sensorNumeratorInput.clear()
        self.sensorDenominatorInput.clear()
        self.update_sensor_preview()