# Standard library imports
import os

# Third party imports
from PyQt5.QtWidgets import QDialog, QMainWindow, QSizePolicy, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMessageBox

# Local imports
from simulation_components.controller_pid import ControllerPID
from simulation_components.plant import get_plant
from simulation_components.input import Input
from simulation_components.sensor import Sensor
from utils.clickable_label import ClickableLabel
from utils.input_utils import simulator_create_pixmap_equation
from utils.file_utils import save_simulation_config, extract_params_from_file, save_simulation_config_as

from views.control_editor import ControlEditor
from views.input_editor import InputEditor
from views.plant_editor import PlantEditor
from views.output_plotter import OutputPlotter
from views.sensor_editor import SensorEditor


class Simulator(QMainWindow):
    def __init__(self, plant_type, file_path, project_type):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/simulator.ui")
        loadUi(ui_path, self)

        # Make labels clickable
        label_map = {
            self.inputLabel: "inputLabel",
            self.controlLabel: "controlLabel",
            self.plantLabel: "plantLabel",
            self.outputLabel: "outputLabel",
            self.sensorLabel: "sensorLabel"
        }
        for old_label, attr_name in label_map.items():
            parent_widget = old_label.parent()
            new_label = ClickableLabel(parent_widget)
            ClickableLabel.replaceLabelInLayout(old_label, new_label)
            ClickableLabel.copyAttributes(new_label, old_label)
            old_label.deleteLater()
            #Assign the new label back to the instance variable
            setattr(self, attr_name, new_label)
        
        # Connect signals to slots
        self.inputLabel.clicked.connect(self.on_input_label_clicked)
        self.outputLabel.clicked.connect(self.on_output_label_clicked)
        self.controlLabel.clicked.connect(self.on_control_label_clicked)
        self.plantLabel.clicked.connect(self.on_plant_label_clicked)
        self.sensorLabel.clicked.connect(self.on_sensor_label_clicked)

        #Buttons
        self.stopButton.clicked.connect(self.on_stop_button_clicked)
        self.simulateButton.clicked.connect(self.on_simulate_button_clicked)

        #Create models
        self.controller_pid = ControllerPID()
        self.plant_controller = get_plant(plant_type)
        self.input_controller = Input()
        self.sensor_controller = Sensor()

        #File path
        self.file_path = file_path
        
        #Project type
        self.project_type = project_type

        if self.project_type == "New Project":
            #Quick save on new project file (to save default params of components)
            self.on_action_save_triggered()
        elif self.project_type == "Open Project":
            #Load params from save file to system models.
            self.load_params_to_models()
            

        #print("plant Type:", self.plant_controller.name)

        #Disabled elements at start
        self.outputLabel.setDisabled(True)
        self.stopButton.setDisabled(True)
        self.simulateButton.setDisabled(False)

        #Menu bar actions
        self.actionSave.triggered.connect(self.on_action_save_triggered) 
        self.actionSave_As.triggered.connect(self.on_action_save_as_triggered) 

        self.update_window_title()
    # Update window Title
    def update_window_title(self):
        """Update the window title to show the current project name."""
        project_name = os.path.splitext(os.path.basename(self.file_path))[0]
        self.setWindowTitle(f"Simulator - {project_name}")

    #--------------- Input Label Methods ---------------
    def on_input_label_clicked(self):
        #print("Input label clicked")
        #self.inputLabel.setText("Input Clicked!")
        dialog = InputEditor(self.input_controller, self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            print("Input configuration accepted")
            print("Params:", self.input_controller.get_parameters())
        else:
            print("Input configuration canceled")

    #--------------- End Input Label Methods ---------------

    #--------------- Control Label Methods ---------------

    def on_control_label_clicked(self):
        dialog = ControlEditor(self.controller_pid, self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            # Apply changes to the model
            #dialog.apply_changes_to_model()
            self.update_control_label()
        else:
            print("Control configuration canceled")

    def update_control_label(self):
        """Update the controlLabel with the LaTeX representation of the PID controller from the model."""
        params = self.controller_pid.get_parameters()
        Kp = params["kp"]
        Ki = params["ki"]
        Kd = params["kd"]

        #Get LaTex equation from model
        latex_eq = self.controller_pid.get_latex_equation(Kp, Ki, Kd)

        # Generate pixmap from LaTeX equation
        pixmap = simulator_create_pixmap_equation(latex_eq, fontsize=20, dpi=200)
        pixmap = pixmap.scaled(
            self.controlLabel.width(), 
            self.controlLabel.height(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )

        self.controlLabel.setPixmap(pixmap)

    #--------------- End Control Label Methods ---------------
    
    #--------------- Plant Label Methods ---------------

    def on_plant_label_clicked(self):
        print("Plant label clicked")
        #self.plantLabel.setText("Plant Clicked!")
        dialog = PlantEditor(self.plant_controller, self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            # Apply changes to the model
            print("Accepted")
            #dialog.apply_changes_to_model()
            self.update_plant_label()
        else:
            print("Plant configuration canceled")


    def update_plant_label(self):
        """Update the plantLabel with the LaTeX representation of the plant from the model."""
        params = self.plant_controller.get_parameters()
        latex_eq = self.plant_controller.get_latex_equation(**params)

        # Generate pixmap from LaTeX equation
        pixmap = simulator_create_pixmap_equation(latex_eq, fontsize=50, dpi=200)
        pixmap = pixmap.scaled(
            self.plantLabel.width(), 
            self.plantLabel.height(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )

        self.plantLabel.setPixmap(pixmap)
    #--------------- End Plant Label Methods ---------------

    #--------------- Sensor Label Methods ---------------

    def on_sensor_label_clicked(self):
        print("Sensor label clicked")
        dialog = SensorEditor(self.sensor_controller, self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            # Apply changes to the model
            print("Accepted")
            print("Sensor:", self.sensor_controller.get_parameters())
            #dialog.apply_changes_to_model()
            self.update_sensor_label()
        else:
            print("Sensor configuration canceled")

    def update_sensor_label(self):
        """Update the sensorLabel with the LaTeX representation of the sensor from the model."""
        params = self.sensor_controller.get_parameters()
        latex_eq = self.sensor_controller.get_latex_equation(**params)

        # Generate pixmap from LaTeX equation
        pixmap = simulator_create_pixmap_equation(latex_eq, fontsize=50, dpi=200)
        pixmap = pixmap.scaled(
            self.plantLabel.width(),
            self.sensorLabel.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.sensorLabel.setPixmap(pixmap)

    #--------------- End Sensor Label Methods ---------------




    #--------------- Output Label Methods ---------------

    def on_output_label_clicked(self):
        print("Output label clicked")
        dialog = OutputPlotter(self.plant_controller, self.controller_pid, self.input_controller, self.sensor_controller, self)
        result = dialog.exec_() 

        #self.outputLabel.setText("Output Clicked!")
    
    #--------------- End Output Label Methods ---------------


    #--------------- Stop Button Methods ---------------

    def on_stop_button_clicked(self):
        self.stopButton.setDisabled(True)
        self.simulateButton.setDisabled(False)
        self.outputLabel.setDisabled(True)
        self.inputLabel.setDisabled(False)
        self.controlLabel.setDisabled(False)
        self.plantLabel.setDisabled(False)
        self.sensorLabel.setDisabled(False)
        print("Stop button clicked")
        #self.stopButton.setText("Stopped")
    
    #--------------- End Stop Button Methods ---------------


    #--------------- Simulate Button Methods ---------------

    def on_simulate_button_clicked(self):
        self.stopButton.setDisabled(False)
        self.simulateButton.setDisabled(True)
        self.outputLabel.setDisabled(False)
        self.inputLabel.setDisabled(True)
        self.controlLabel.setDisabled(True)
        self.plantLabel.setDisabled(True)
        self.sensorLabel.setDisabled(True)
        print("Simulate button clicked")
        #self.simulateButton.setText("Simulating...")

    #--------------- End Simulate Button Methods ---------------


    #--------------- Action Save Methods ---------------
    def on_action_save_triggered(self):
        pid_params = self.controller_pid.get_parameters()
        plant_params = self.plant_controller.get_parameters()
        input_params = self.input_controller.get_parameters()
        sensor_params = self.sensor_controller.get_parameters()
        file_path = self.file_path

        save_simulation_config(
            file_path=file_path,
            pid_params=pid_params,
            plant_params=plant_params,
            input_params=input_params,
            sensor_params=sensor_params,
            plant_type_fallback=self.plant_controller.name
        )


    #--------------- End Action Save Methods ---------------


    #--------------- Action Save As Methods --------------

    def on_action_save_as_triggered(self):
        """Handle Save As action using the separate file utility function."""
        print("Save As triggered")
        
        # Get current params
        pid_params = self.controller_pid.get_parameters()
        plant_params = self.plant_controller.get_parameters()
        input_params = self.input_controller.get_parameters()
        sensor_params = self.sensor_controller.get_parameters()
        
        # Call function Save As
        new_file_path = save_simulation_config_as(
            parent_window=self,
            current_file_path=self.file_path,
            pid_params=pid_params,
            plant_params=plant_params,
            input_params=input_params,
            sensor_params=sensor_params,
            plant_type_fallback=self.plant_controller.name
        )
        
        # If saved successfully, update the path and title
        if new_file_path:
            self.file_path = new_file_path
            self.update_window_title()
            
            # Display success message
            QMessageBox.information(self, "Success", 
                                f"Project saved as:\n{os.path.basename(new_file_path)}")

    #--------------- End Action Save As Methods --------------



    #--------------- Load Params Methods --------------

    def load_params_to_models(self):
        """Load PID, Plant, and Input parameters from the saved project file."""
        # Extract parameters from file using the separate function
        pid_params, plant_params, input_params, sensor_params = extract_params_from_file(self.file_path)

        # Apply parameters to model controllers
        try:
            if pid_params:
                self.controller_pid.set_parameters(Kp=pid_params["kp"], Ki=pid_params["ki"], Kd=pid_params["kd"])
            if plant_params:
                self.plant_controller.set_parameters(**plant_params)
            if input_params:
                self.input_controller.set_parameters(**input_params)
            if sensor_params:
                self.sensor_controller.set_parameters(Numerator=sensor_params["Numerator"], Denominator=sensor_params["Denominator"])
        except Exception as e:
            print(f"Error setting parameters to models: {e}")
            return

        print("Parameters successfully loaded into models.")
        print("PID:", self.controller_pid.get_parameters())
        print("Plant:", self.plant_controller.get_parameters())
        print("Input:", self.input_controller.get_parameters())
        print("Sensor:", self.sensor_controller.get_parameters())

        self.update_control_label()
        self.update_plant_label()
        self.update_sensor_label()

    #--------------- End Load Params Methods --------------


