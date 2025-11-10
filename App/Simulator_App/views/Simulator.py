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
        """
        Main Simulator Window.
        Args:
            plant_type (str): The type of plant to initialize.
            file_path (str): The path to the project file.
            project_type (str): "New Project" or "Open Project".
        Returns:
            None
        """
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/simulator.ui")
        loadUi(ui_path, self)

        self.plant_type = plant_type

        #Create models
        self.controller_pid = ControllerPID()
        self.plant_controller = get_plant(plant_type)
        self.input_controller = Input()
        self.sensor_controller = Sensor()


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
        self.inputLabel.setToolTip(self.input_controller.get_component_description())

        self.outputLabel.clicked.connect(self.on_output_label_clicked)

        self.controlLabel.clicked.connect(self.on_control_label_clicked)
        self.controlLabel.setToolTip(self.controller_pid.get_component_description())

        self.plantLabel.clicked.connect(self.on_plant_label_clicked)
        self.plantLabel.setToolTip(self.plant_controller.get_component_description())

        self.sensorLabel.clicked.connect(self.on_sensor_label_clicked)
        self.sensorLabel.setToolTip(self.sensor_controller.get_component_description())
        
        #Indicator Labels Centering
        self.controlLabelIndicator.setAlignment(Qt.AlignCenter)
        self.plantLabelIndicator.setAlignment(Qt.AlignCenter)
        self.sensorLabelIndicator.setAlignment(Qt.AlignCenter)

        #Buttons
        self.resetButton.clicked.connect(self.on_reset_button_clicked)

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

        #Menu bar actions
        self.actionSave.triggered.connect(self.on_action_save_triggered) 
        self.actionSave_As.triggered.connect(self.on_action_save_as_triggered) 

        self.update_window_title()
    # Update window Title
    def update_window_title(self):
        """
        Update the window title to show the current project name.
        Args:
            None
        Returns:
            None
        """
        project_name = os.path.splitext(os.path.basename(self.file_path))[0]
        self.setWindowTitle(f"Simulator - {project_name} ({self.plant_controller.name})")

    #--------------- Input Label Methods ---------------
    def on_input_label_clicked(self):
        """
        Handle click on inputLabel to open InputEditor dialog.
        Args:
            None
        Returns:            
            None
        """
        #print("Input label clicked")
        dialog = InputEditor(self.input_controller, self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            #print("Input configuration accepted")
            #print("Params:", self.input_controller.get_parameters())
            pass
        else:
            #print("Input configuration canceled")
            pass

    #--------------- End Input Label Methods ---------------

    #--------------- Control Label Methods ---------------

    def on_control_label_clicked(self):
        """
        Handle click on controlLabel to open ControlEditor dialog.
        Args:
            None
        Returns:
            None
        """

        dialog = ControlEditor(self.controller_pid, self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            # Apply changes to the model
            #dialog.apply_changes_to_model()
            self.update_control_label()
        else:
            #print("Control configuration canceled")
            pass

    def update_control_label(self):
        """
        Update the controlLabel with the LaTeX representation of the PID controller from the model.
        Args:
            None
        Returns:
            None
        """
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
        """
        Handle click on plantLabel to open PlantEditor dialog.
        Args:
            None
        Returns:
            None
        """
        #print("Plant label clicked")
        dialog = PlantEditor(self.plant_controller, self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            # Apply changes to the model
            #print("Accepted")
            #dialog.apply_changes_to_model()
            self.update_plant_label()
        else:
            #print("Plant configuration canceled")
            pass


    def update_plant_label(self):
        """
        Update the plantLabel with the LaTeX representation of the plant from the model.
        Args:
            None
        Returns:
            None
        """
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
        """
        Handle click on sensorLabel to open SensorEditor dialog.
        Args:
            None
        Returns:
            None
        """
        #print("Sensor label clicked")
        dialog = SensorEditor(self.sensor_controller, self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            # Apply changes to the model
            #print("Accepted")
            #print("Sensor:", self.sensor_controller.get_parameters())
            #dialog.apply_changes_to_model()
            self.update_sensor_label()
        else:
            #print("Sensor configuration canceled")
            pass

    def update_sensor_label(self):
        """
        Update the sensorLabel with the LaTeX representation of the sensor from the model.
        Args:
            None
        Returns:
            None
        """
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
        """
        Handle click on outputLabel to open OutputPlotter dialog.
        Args:
            None
        Returns:
            None
        """
        #print("Output label clicked")
        self.inputLabel.setDisabled(True)
        self.controlLabel.setDisabled(True)
        self.plantLabel.setDisabled(True)
        self.sensorLabel.setDisabled(True)
        dialog = OutputPlotter(self.plant_controller, self.controller_pid, self.input_controller, self.sensor_controller, self)
        result = dialog.exec_()
        self.inputLabel.setDisabled(False)
        self.controlLabel.setDisabled(False)
        self.plantLabel.setDisabled(False)
        self.sensorLabel.setDisabled(False)

    
    #--------------- End Output Label Methods ---------------

    #--------------- Reset Button Methods ---------------

    def on_reset_button_clicked(self):
        """
        Handle click on reset button to reset the component values.
        Args:
            None    
        Returns:
            None
        """
        # Create confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Reset",
            "Are you sure you want to reset all simulation components?\n\n"
            "This will reset:\n"
            "• PID Controller parameters\n"
            "• Plant model parameters\n"
            "• Input signal parameters\n"
            "• Sensor parameters\n\n"
            "All current values will be lost.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # Default button
        )
        
        # If user confirms, proceed with reset
        if reply == QMessageBox.Yes:
            # Reset default models
            self.controller_pid = ControllerPID()
            self.plant_controller = get_plant(self.plant_type)
            self.input_controller = Input()
            self.sensor_controller = Sensor()

            self.update_control_label()
            self.update_plant_label()
            self.update_sensor_label()
            
            # Optional: Show success message
            QMessageBox.information(
                self,
                "Reset Complete",
                "All simulation components have been reset to default values."
            )
            #print("Reset confirmed - components reset to defaults")
        else:
            #print("Reset canceled by user")
            pass
    
    #--------------- End Reset Button Methods ---------------

    #--------------- Action Save Methods ---------------
    def on_action_save_triggered(self):
        """"
        Handle Save action using the separate file utility function.
        Args:
            None
        Returns:
            None
        """
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
        """
        Handle Save As action using the separate file utility function.
        Args:
            None
        Returns:
            None
        """
        #print("Save As triggered")
        
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
        """
        Load PID, Plant, and Input parameters from the saved project file.
        Args:
            None
        Returns:
            None
        """
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
            #print(f"Error setting parameters to models: {e}")
            return

        #print("Parameters successfully loaded into models.")
        #print("PID:", self.controller_pid.get_parameters())
        #print("Plant:", self.plant_controller.get_parameters())
        #print("Input:", self.input_controller.get_parameters())
        #print("Sensor:", self.sensor_controller.get_parameters())

        self.update_control_label()
        self.update_plant_label()
        self.update_sensor_label()

    #--------------- End Load Params Methods --------------



    def closeEvent(self, event):
        """
        Handle the window close event to prompt for saving changes.
        Args:
            event: The close event
        Returns:
            None
        """
        
        reply = QMessageBox.question(
            self,
            "Save Changes?",
            "Do you want to save your changes before closing?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Save  # Default button
        )
        
        if reply == QMessageBox.Save:
            # Save changes and close
            self.on_action_save_triggered()
            event.accept()
        elif reply == QMessageBox.Discard:
            # Close without saving
            event.accept()
        else:
            # Cancel the close operation
            event.ignore()
