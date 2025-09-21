import os
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from simulation_components.plant import Plant
from utils.input_utils import simulator_create_pixmap_equation


class PlantEditor(QDialog):
    def __init__(self, plant_controller: Plant, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/predefined_plant_editor.ui")
        loadUi(ui_path, self)

        self.plant_controller = plant_controller

        # Input Validators
        validator = QDoubleValidator(-9999.0, 9999.0, 4)
        validator.setNotation(QDoubleValidator.StandardNotation)

        for i in range(1, 7):  # From input 1 to 6 
            line_edit = getattr(self, f"param{i}Input")
            line_edit.setValidator(validator)

        # Button Configuration
        self.applyButton.clicked.connect(self.accept)
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
            line_edit.setText(str(value))


    def update_plant_preview(self):
        # Tomar valores de inputs
        params = {}
        for i, key in enumerate(self.plant_controller.get_parameters().keys(), start=1):
            text = getattr(self, f"param{i}Input").text()
            if text:
                try:
                    params[key] = float(text)
                except ValueError:
                    params[key] = None  # si no es convertible, mostramos símbolo

        # Pedir la ecuación usando los valores ingresados o None para los vacíos
        latex_eq = self.plant_controller.get_latex_equation(**params)

        pixmap = simulator_create_pixmap_equation(latex_eq, fontsize=10)
        pixmap = pixmap.scaled(
            self.plantLabel.width(),
            self.plantLabel.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.plantLabel.setPixmap(pixmap)

    def apply_changes_to_model(self):
        """Update the plant_controller object with values from inputs"""

        params = {}

        for i, key in enumerate(self.plant_controller.get_parameters().keys(), start=1):
            input_widget = getattr(self, f"param{i}Input")
            text = input_widget.text()

            if text:
                try:
                    params[key] = float(text)
                except ValueError:
                    print(f"Error: Invalid value for {key}")
                    return

        #Update plant Parameters 
        self.plant_controller.set_parameters(**params)

        print("Parameteres updated")
        print(self.plant_controller.get_parameters())
        print("Transfer Function")
        print(self.plant_controller.get_transfer_function())