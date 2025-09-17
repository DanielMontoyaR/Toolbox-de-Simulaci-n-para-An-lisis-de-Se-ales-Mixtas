import os
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from utils.file_utils import get_project_file
from views.createProject import CreateProject

class Start(QDialog):
    def __init__(self, stacked_widget):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/Start.ui")
        loadUi(ui_path, self)

        self.stacked_widget = stacked_widget

        self.projectopenButton.clicked.connect(self.open_project)
        self.projectcreateButton.clicked.connect(self.create_project)

        self.stacked_widget.resize(self.size())

    def open_project(self):
        file_path = get_project_file(self)

        if file_path is None:
            print("No file selected")
            return

        if file_path == "INVALID":
            self.openerrorLabel.setText("Error: Invalid project file selected (txt).")
            return
        else:
            self.openerrorLabel.setText("")

        with open(file_path, "r") as file:
            content = file.read()
            print(f"Content:\n{content}")
            # Change window to Simulator
        pass

    def create_project(self):
        createProject = CreateProject(self.stacked_widget)
        self.stacked_widget.addWidget(createProject)
        self.stacked_widget.setCurrentWidget(createProject)
