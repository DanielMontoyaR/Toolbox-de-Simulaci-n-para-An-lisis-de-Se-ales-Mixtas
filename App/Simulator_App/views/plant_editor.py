import os
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, QLocale
from simulation_components.plant import Plant
from utils.input_utils import simulator_create_pixmap_equation


class PlantEditor(QDialog):
    def __init__(self, plant_controller: Plant, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/plant_editor.ui")
        loadUi(ui_path, self)

        self.plant_controller = plant_controller

        self.setWindowTitle(plant_controller.name + " Editor")
        self.errorLabel.hide()
        self.errorLabelInfo.hide()

        # Button Configuration
        self.applyButton.clicked.connect(self.apply_changes_to_model)
        self.cancelButton.clicked.connect(self.reject)

        #Plant label configuration
        self.plantLabel.setAlignment(Qt.AlignCenter)

        #Parameter descriptions 
        descriptions = self.plant_controller.get_parameter_descriptions()

        #Label and Tooltip configuration
        for i, (key, desc) in enumerate(descriptions.items(), start=1):
            label = getattr(self, f"param{i}Label")
            label.setText(key)

            info_label = getattr(self, f"param{i}LabelInfo")
            info_label.setToolTip(desc)

            line_edit = getattr(self, f"param{i}Input")

            if key in ("Numerator", "Denominator"):
                #print("Setting regex validator for polynomial input")

                # Only allow numbers, commas, and periods
                regex = QRegExp(r"^(-?\d+(\.\d+)?)(,-?\d+(\.\d+)?)*$")
                validator = QRegExpValidator(regex)

                
                line_edit.setPlaceholderText("e.g., 1, 0, 5 for s^2 + 5")
            else:
                # Only allow numbers (including negative and decimal)
                regex = QRegExp(r"^-?\d+(\.\d*)?$") # Allow negative and decimal numbers
                validator = QRegExpValidator(regex)

            line_edit.setValidator(validator)
        # Hide unused Labels and Inputs
        for j in range(len(descriptions) + 1, 7):  
            getattr(self, f"param{j}Label").hide()
            getattr(self, f"param{j}LabelInfo").hide()
            getattr(self, f"param{j}Input").hide()

        
        # Initialize Plant Label Preview
        self.update_plant_preview()

        # Real-time connection of inputs to labels
        self.param1Input.textChanged.connect(lambda text: self.update_plant_preview())
        self.param2Input.textChanged.connect(lambda text: self.update_plant_preview())
        self.param3Input.textChanged.connect(lambda text: self.update_plant_preview())
        self.param4Input.textChanged.connect(lambda text: self.update_plant_preview())
        self.param5Input.textChanged.connect(lambda text: self.update_plant_preview())
        self.param6Input.textChanged.connect(lambda text: self.update_plant_preview())

        # Load current values from the model (if any)
        #self.load_from_model()

    def load_from_model(self):
        """Initialize the input fields with current controller values"""
        params = self.plant_controller.get_parameters()
        for i, (key, value) in enumerate(params.items(), start=1):
            line_edit = getattr(self, f"param{i}Input")

            # If the value is a list (for polynomials), convert to comma-separated string
            if isinstance(value, list):
                line_edit.setText(", ".join(map(str, value)))
            else:
                line_edit.setText(str(value))


    def update_plant_preview(self):
        """Update the plant preview label"""
        try:
            # Take values from inputs
            params = {}
            for i, key in enumerate(self.plant_controller.get_parameters().keys(), start=1):
                text = getattr(self, f"param{i}Input").text()
                if text:
                    if key in ("Numerator", "Denominator"):
                        params[key] = text  # keep as string for polynomial parsing
                    else:
                        try:
                            params[key] = float(text)
                        except ValueError:
                            params[key] = None  # if not convertible, set to None

            # Ask plant controller for LaTeX equation
            latex_eq = self.plant_controller.get_latex_equation(**params)

            pixmap = simulator_create_pixmap_equation(latex_eq, fontsize=10)
            pixmap = pixmap.scaled(
                self.plantLabel.width(),
                self.plantLabel.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.plantLabel.setPixmap(pixmap)
        
        except Exception as e:
            # If there's an error, show a message or leave the preview empty
            print(f"Error updating preview: {e}")
            self.plantLabel.setText("Error: Invalid input")

    def apply_changes_to_model(self):
        """Update the plant_controller object with values from inputs"""

        params = {}
        # Collect values from input fields
        for i, key in enumerate(self.plant_controller.get_parameters().keys(), start=1):
            input_widget = getattr(self, f"param{i}Input")
            text = input_widget.text()
            # Only update if text is not empty
            if text:
                # Check if the key is for a polynomial (personalized plant model)
                if key in ("Numerator", "Denominator"):
                    params[key] = text  # keep as string for polynomial parsing
                else:
                    try:
                        params[key] = float(text)
                    except ValueError:
                        print(f"Error: Invalid value for {key}")
                        return

        # Save old parameters for comparison
        old_params = self.plant_controller.get_parameters().copy()

        #Try to update parameters in the model
        self.plant_controller.set_parameters(**params)
        tf = self.plant_controller.get_transfer_function()

        if isinstance(tf, str):  # An error message was returned

            self.plant_controller.set_parameters(**old_params) #Revert to old parameters
            self.errorLabel.show()
            self.errorLabelInfo.show()
            self.errorLabelInfo.setToolTip(tf) # Show error message as tooltip
            return
        else:
            self.errorLabel.hide()
            self.errorLabelInfo.hide()
            print("Parameters updated")
            print(self.plant_controller.get_parameters())
            print("Transfer Function")
            print(self.plant_controller.get_transfer_function())
            self.accept()  # Close dialog with Accepted status