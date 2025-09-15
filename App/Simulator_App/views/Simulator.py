import os
from PyQt5.QtWidgets import QDialog, QMainWindow, QSizePolicy, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from utils.ClickableLabel import ClickableLabel

class Simulator(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/Simulator2.ui")
        loadUi(ui_path, self)

        label_map = {
            self.inputLabel: "inputLabel",
            self.controlLabel: "controlLabel",
            self.plantLabel: "plantLabel",
            self.outputLabel: "outputLabel"
        }
        for old_label, attr_name in label_map.items():
            parent_widget = old_label.parent()
            new_label = ClickableLabel(parent_widget)
            ClickableLabel.replaceLabelInLayout(old_label, new_label)
            ClickableLabel.copyAttributes(new_label, old_label)
            old_label.deleteLater()
            #Assign the new label back to the instance variable
            setattr(self, attr_name, new_label)

        self.inputLabel.clicked.connect(self.on_input_label_clicked)
        self.outputLabel.clicked.connect(self.on_output_label_clicked)
        self.controlLabel.clicked.connect(self.on_control_label_clicked)
        self.plantLabel.clicked.connect(self.on_plant_label_clicked)


    def on_input_label_clicked(self):
        print("Input label clicked")
        self.inputLabel.setText("Input Clicked!")

    def on_control_label_clicked(self):
        print("Control label clicked")
        self.controlLabel.setText("Control Clicked!")

    def on_plant_label_clicked(self):
        print("Plant label clicked")
        self.plantLabel.setText("Plant Clicked!")

    def on_output_label_clicked(self):
        print("Output label clicked")
        self.outputLabel.setText("Output Clicked!")