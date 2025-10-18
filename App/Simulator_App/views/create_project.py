import os
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from utils.file_utils import create_project_file
from utils.input_utils import create_project_validate_inputs
from views.simulator import Simulator

class CreateProject(QDialog):
    def __init__(self, stacked_widget):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/project_create.ui")
        loadUi(ui_path, self)

        self.stacked_widget = stacked_widget  # Store the stacked widget reference
        self.createButton.clicked.connect(self.create_project)
        self.cancelButton.clicked.connect(self.go_back)
        self.pathButton.clicked.connect(self.browse_path)
        self.plantComboBox.clear()
        self.plantComboBox.addItems(["Ball and Beam", "DC Motor Speed Control", "DC Motor Position Control", "Personalized Plant"])
        self.stacked_widget.resize(self.size())


    def browse_path(self):
        from PyQt5.QtWidgets import QFileDialog
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.pathLineEdit.setText(directory)

    def create_project(self):
        #print("Project creation initiated")
        #print(self.nombreproyectolineEdit.text())

        validation_result = create_project_validate_inputs(
            self.pathLineEdit.text(),
            self.projectNameLineEdit.text()
        )
        if validation_result == "EMPTY_NAME":
            self.createProjectErrorLabel.setText("Error: The project name cannot be empty.")
            return
        elif validation_result == "EMPTY_PATH":
            self.createProjectErrorLabel.setText("Error: The file path cannot be empty.")
            return
        elif validation_result == "DUPLICATE":
            self.createProjectErrorLabel.setText("Error: A project with the same name already exists in the specified path.")
            return
        elif validation_result == "INVALID_PATH":
            self.createProjectErrorLabel.setText("Error: The specified file path is not a valid directory.")
            return
        else:
            self.createProjectErrorLabel.setText("")
            file_path = create_project_file(
                self.projectNameLineEdit.text(),
                self.plantComboBox.currentText(),
                self.pathLineEdit.text(),
                {},  # Empty PID parameters
                {},  # Empty Plant parameters
                {},  # Empty Input parameters
                {},  # Empty Sensor parameters
                self  # parent
            )
            """
            simulator = Simulator(self.stacked_widget)
            self.stacked_widget.addWidget(simulator)
            self.stacked_widget.setCurrentWidget(simulator)"""

            project_type = "New Project"

            self.simulator = Simulator(self.plantComboBox.currentText(), file_path, project_type)
            self.simulator.show()
            self.stacked_widget.close()



    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)