import os
from PyQt5.QtWidgets import QDialog, QMainWindow, QSizePolicy, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from utils.ClickableLabel import ClickableLabel
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDoubleValidator

from utils.input_utils import simulator_create_pixmap_equation

class Simulator(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/Simulator.ui")
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
        self.stopButton.clicked.connect(self.on_stop_button_clicked)
        self.simulateButton.clicked.connect(self.on_simulate_button_clicked)


    def on_input_label_clicked(self):
        print("Input label clicked")
        self.inputLabel.setText("Input Clicked!")

    def on_control_label_clicked(self):
        #print("Control label clicked")
        #self.controlLabel.setText("Control Clicked!")

        dialog = QDialog(self)
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/ControlEditor.ui")
        loadUi(ui_path, dialog)
        dialog.setWindowModality(Qt.ApplicationModal)
        
        #Input Validators
        validator = QDoubleValidator(-9999.0, 9999.0, 4)
        validator.setNotation(QDoubleValidator.StandardNotation)
        dialog.kpInput.setValidator(validator)
        dialog.kiInput.setValidator(validator)
        dialog.kdInput.setValidator(validator)

        #PID label configuration
        dialog.pidLabel.setAlignment(Qt.AlignCenter)

        #Button Configuration
        dialog.applyButton.clicked.connect(dialog.accept)
        dialog.cancelButton.clicked.connect(dialog.reject)

        # Real time connection of inputs to labels
        dialog.kpInput.textChanged.connect(lambda text: self.update_pid_preview(dialog))
        dialog.kiInput.textChanged.connect(lambda text: self.update_pid_preview(dialog))
        dialog.kdInput.textChanged.connect(lambda text: self.update_pid_preview(dialog))
        
        #Initialize PID preview
        self.update_pid_preview(dialog)

        #Set Tooltips
        dialog.kdLabelInfo.setToolTip("Derivative Gain (Kd):\n"
                                      "Influences the system's response to the rate of change of the error.\n"
                                      "Higher Kd values can help reduce overshoot and improve stability,\n"
                                      "but may also lead to increased sensitivity to noise.")
        dialog.kpLabelInfo.setToolTip("Proportional Gain (Kp):\n"
                                      "Determines the reaction to the current error.\n"
                                      "Higher Kp values result in a larger control action for a given error,\n"
                                      "which can reduce rise time but may increase overshoot and lead to instability.")
        dialog.kiLabelInfo.setToolTip("Integral Gain (Ki):\n"
                                      "Addresses accumulated past errors.\n"
                                      "Higher Ki values can eliminate steady-state error,\n"
                                      "but may also lead to increased overshoot and oscillations.")

        result = dialog.exec_()

        if result == QDialog.Accepted:
            #Read Inputs from QDialog
            kp = dialog.kpInput.text()
            ki = dialog.kiInput.text()
            kd = dialog.kdInput.text()
            #Put values on controlLabel
            self.controlLabel.setText(f"Kp: {kp}, Ki: {ki}, Kd: {kd}")

            self.update_control_label(kp, ki, kd)

        else:
            print("Control configuration canceled")

    def update_control_label(self, Kp, Ki, Kd):
        """
        Update the controlLabel with the LaTeX representation of the PID controller.
        """

        # Create LaTeX equation
        latex_eq = r"C(s) = $%s + \frac{%s}{s} + %s\,s$" % (Kp, Ki, Kd)

        # Generate pixmap from LaTeX equation
        pixmap = simulator_create_pixmap_equation(latex_eq, fontsize=20, dpi=200)
        pixmap = pixmap.scaled(self.controlLabel.width(), self.controlLabel.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.controlLabel.setPixmap(pixmap)

    def update_pid_preview(self, dialog):
        kp = dialog.kpInput.text() or "Kp"
        ki = dialog.kiInput.text() or "Ki"
        kd = dialog.kdInput.text() or "Kd"

        latex_eq = r"$%s + \frac{%s}{s} + %s\,s$" % (kp, ki, kd)

        pixmap = simulator_create_pixmap_equation(latex_eq, fontsize=10)

        # Scale pixmap to fit label
        pixmap = pixmap.scaled(dialog.pidLabel.width(),
                            dialog.pidLabel.height(),
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation)

        dialog.pidLabel.setPixmap(pixmap)


    def on_plant_label_clicked(self):
        print("Plant label clicked")
        self.plantLabel.setText("Plant Clicked!")

    def on_output_label_clicked(self):
        print("Output label clicked")
        self.outputLabel.setText("Output Clicked!")

    def on_stop_button_clicked(self):
        print("Stop button clicked")
        self.stopButton.setText("Stopped")
    
    def on_simulate_button_clicked(self):
        print("Simulate button clicked")
        self.simulateButton.setText("Simulating...")