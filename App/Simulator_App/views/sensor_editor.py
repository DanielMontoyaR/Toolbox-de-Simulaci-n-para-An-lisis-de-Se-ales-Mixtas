import os
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, QLocale
from simulation_components.sensor import Sensor
from utils.input_utils import simulator_create_pixmap_equation


class SensorEditor(QDialog):
    def __init__(self, sensor_controller: Sensor, parent=None):
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
        self.sensorDenominatorInput.setPlaceholderText("e.g., 1, 2, 1 for s^2 + 2s + 1")

        # Real-time connection of inputs to preview
        self.sensorNumeratorInput.textChanged.connect(self.update_sensor_preview)
        self.sensorDenominatorInput.textChanged.connect(self.update_sensor_preview)
        
        # Initialize Sensor Label Preview
        self.update_sensor_preview()

        # Load current values from the model
        self.load_from_model()

    def load_from_model(self):
        """Initialize the input fields with current controller values"""
        params = self.sensor_controller.get_parameters()
        
        # Convert numerator list to comma-separated string
        if 'Numerator' in params:
            num_str = ", ".join(map(str, params['Numerator']))
            self.sensorNumeratorInput.setText(num_str)
        
        # Convert denominator list to comma-separated string
        if 'Denominator' in params:
            den_str = ", ".join(map(str, params['Denominator']))
            self.sensorDenominatorInput.setText(den_str)

    def update_sensor_preview(self):
        """Update the sensor preview label"""
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

    def apply_changes_to_model(self):
        """Update the sensor_controller object with values from inputs"""
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

        # Try to update parameters in the model
        self.sensor_controller.set_coefficients(
            num=params.get('Numerator'), 
            den=params.get('Denominator')
        )
        
        tf = self.sensor_controller.get_transfer_function()

        if isinstance(tf, str):  # An error message was returned
            # Revert to old parameters
            self.sensor_controller.set_coefficients(
                num=old_params.get('Numerator'),
                den=old_params.get('Denominator')
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