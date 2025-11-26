import os
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from utils.file_utils import create_project_file
from utils.input_utils import create_project_validate_inputs

class CreateProject(QDialog):
    def __init__(self, app_manager):
        """
        Dialog for creating a new project.
        Args:
            app_manager: The ApplicationManager instance.
        Returns:
            None"""
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/project_create.ui")
        loadUi(ui_path, self)

        self.app_manager = app_manager  # Store the app_manager reference
        self.createButton.clicked.connect(self.create_project)
        self.cancelButton.clicked.connect(self.go_back)
        self.pathButton.clicked.connect(self.browse_path)
        self.plantComboBox.clear()
        self.plantComboBox.addItems(["Ball and Beam", "DC Motor Speed Control", "DC Motor Position Control", "Personalized Plant"])

    def keyPressEvent(self, event):
        """
        System Ignore ESC key press event (this caused system to display a white screen and stopped working)
        Args:
            event: Esc key press event
        Returns:
            None
        """
        if event.key() == Qt.Key_Escape:
            # Ignore ESC
            event.ignore()
        else:
            super().keyPressEvent(event)

    def browse_path(self):
        """
        Open a file dialog to select a directory.
        Args:
            None
        Returns:
            None
        """
        from PyQt5.QtWidgets import QFileDialog
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.pathLineEdit.setText(directory)

    def create_project(self):
        """
        Validate inputs and create a new project.
        Args:
            None
        Returns:
            None
        """
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

            
            project_type = "New Project"
            self.app_manager.show_simulator(self.plantComboBox.currentText(), file_path, project_type)

    def go_back(self):
        """
        Navigate back to the previous screen.
        Args:
            None
        Returns:
            None
        """
        self.app_manager.show_start()