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

        for i in range(1, 7):  # del 1 al 6
            line_edit = getattr(self, f"param{i}Input")
            line_edit.setValidator(validator)

        

        # Button Configuration
        self.applyButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)


        #Label configurationn
        if self.plant_controller.name == "Ball and Beam":
            self.param1Label.setText("m")
            self.param2Label.setText("R")
            self.param3Label.setText("d")
            self.param4Label.setText("g")
            self.param5Label.setText("L")
            self.param6Label.setText("J")
            self.param1LabelInfo.setToolTip(self.plant_controller.get_parameter_description("m"))
            self.param2LabelInfo.setToolTip(self.plant_controller.get_parameter_description("R"))
            self.param3LabelInfo.setToolTip(self.plant_controller.get_parameter_description("d"))
            self.param4LabelInfo.setToolTip(self.plant_controller.get_parameter_description("g"))
            self.param5LabelInfo.setToolTip(self.plant_controller.get_parameter_description("L"))
            self.param6LabelInfo.setToolTip(self.plant_controller.get_parameter_description("J"))
        elif self.plant_controller.name == "DC Motor Speed Control" or self.plant_controller.name == "DC Motor Position Control":
            self.param1Label.setText("J")
            self.param2Label.setText("b")
            self.param3Label.setText("K")
            self.param4Label.setText("R")
            self.param5Label.setText("L")
            self.param6Label.hide()
            self.param1LabelInfo.setToolTip(self.plant_controller.get_parameter_description("J"))
            self.param2LabelInfo.setToolTip(self.plant_controller.get_parameter_description("b"))
            self.param3LabelInfo.setToolTip(self.plant_controller.get_parameter_description("K"))
            self.param4LabelInfo.setToolTip(self.plant_controller.get_parameter_description("R"))
            self.param5LabelInfo.setToolTip(self.plant_controller.get_parameter_description("L"))
            self.param6LabelInfo.hide()
            self.param6Input.hide()

