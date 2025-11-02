import os
import re
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from utils.file_utils import get_project_file, validate_project_file
from views.create_project import CreateProject
from views.simulator import Simulator

class Start(QDialog):
    def __init__(self, stacked_widget):
        """
        Start dialog for opening or creating projects.
        Args:
            stacked_widget (QStackedWidget): The main stacked widget to switch views.
        Returns:
            None
        """
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/start.ui")
        loadUi(ui_path, self)

        self.stacked_widget = stacked_widget

        self.projectopenButton.clicked.connect(self.open_project)
        self.projectcreateButton.clicked.connect(self.create_project)

        self.errorLabel.hide()
        self.errorLabelInfo.hide()

        self.stacked_widget.resize(self.size())


    def keyPressEvent(self, event):
        """
        System Ignore ESC key press event (this caused system to display a white screen and stopped working)
        Args:
            event: Esc key press event
        Returns:
            None
        """
        if event.key() == Qt.Key_Escape:
            event.ignore()  # Ignore ESC
        else:
            super().keyPressEvent(event)


    def open_project(self):
        """
        Open an existing project.
        Validate the project file structure before loading.

        Args:
            None
        Returns:
            None
        """
        file_path = get_project_file(self)

        if file_path is None:
            print("No file selected")
            return

        if file_path == "INVALID":
            self.errorLabel.setText("Error: Invalid project file selected (txt).")
            return
        else:
            self.errorLabel.setText("")

        # validate the structure before proceeding

        valid, error_message, error_log = validate_project_file(file_path)

        if not valid:
            self.errorLabel.setText(f"Error: {error_message}")
            self.errorLabel.show()
            self.errorLabelInfo.setText(f"<u>Details:</u>")
            self.errorLabelInfo.setToolTip(error_log)
            self.errorLabelInfo.show()
            return
        
        #Continue loading if the structure is valid.
        with open(file_path, "r") as file:
            self.errorLabel.hide()
            self.errorLabelInfo.hide()
            content = file.read()
            print(f"Content:\n{content}")

            match = re.search(r"Plant type:\s*(.+)", content)
            plant_type = match.group(1).strip() if match else "Unknown"

            # Change window to Simulator
            project_type = "Open Project"
            self.simulator = Simulator(plant_type, file_path, project_type)
            self.simulator.show()
            self.stacked_widget.close()

    def create_project(self):
        """
        Create a new project.
        Args:
            None
        Returns:
            None
        """
        createProject = CreateProject(self.stacked_widget)
        self.stacked_widget.addWidget(createProject)
        self.stacked_widget.setCurrentWidget(createProject)
