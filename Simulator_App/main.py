# Standard library imports
import sys

# Third-party imports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

# Local application imports
from views.start import Start
from views.simulator import Simulator
from views.create_project import CreateProject
import tests.plant_tester.plant_tester as Tester

MAX_WIDTH_START = 370
MAX_HEIGHT_START = 441

MIN_WIDTH_SIMULATOR = 1115
MIN_HEIGHT_SIMULATOR = 601

class ApplicationManager:
    def __init__(self):
        """
        Initialize the ApplicationManager.
        Args:
            None
        Returns:
            None
        """
        self.app = QApplication(sys.argv)
        self.main_window = QtWidgets.QStackedWidget()
        self.current_simulator = None  # Reference to current simulator
        self.setup_application()
        
    def setup_application(self):
        """
        Perform initial application setup.
        Args:
            None
        Returns:
            None
        """
        self.main_window.setWindowTitle("TSASM - Start Menu")
        self.show_start()
        
    def show_start(self):
        """
        Display the start window.
        Args:
            None
        Returns:
            None
        """
        self.cleanup_stack()
        self.current_simulator = None  # Clear simulator reference
        start_window = Start(self)
        self.main_window.addWidget(start_window)
        self.main_window.setCurrentWidget(start_window)
        
        # Set size for the start window
        self.main_window.setFixedSize(MAX_WIDTH_START, MAX_HEIGHT_START)
        self.main_window.show()
        
    def show_simulator(self, plant_type, file_path, project_type):
        """
        Display the simulator window.
        Args:
            plant_type (str): Type of plant to simulate
            file_path (str): Path to the project file
            project_type (str): "New Project" or "Open Project"
        Returns:
            None
        """
        self.cleanup_stack()
        simulator = Simulator(plant_type, file_path, project_type, self)
        self.current_simulator = simulator  # Save reference
        self.main_window.addWidget(simulator)
        self.main_window.setCurrentWidget(simulator)
        
        # Change to variable size for simulator
        self.main_window.setMinimumSize(MIN_WIDTH_SIMULATOR, MIN_HEIGHT_SIMULATOR)
        self.main_window.setMaximumSize(16777215, 16777215)
        self.main_window.resize(MIN_WIDTH_SIMULATOR, MIN_HEIGHT_SIMULATOR)
        self.main_window.setWindowTitle(f"Simulator - {plant_type}")
        
    def show_create_project(self):
        """
        Display the create project window.
        Args:
            None
        Returns:
            None
        """
        self.cleanup_stack()
        self.current_simulator = None  # Clear simulator reference
        create_project = CreateProject(self)
        self.main_window.addWidget(create_project)
        self.main_window.setCurrentWidget(create_project)
        
        # Set size for create project window
        self.main_window.setFixedSize(MAX_WIDTH_START, MAX_HEIGHT_START)
        
    def cleanup_stack(self):
        """
        Clean up the stacked widget safely.
        Args:
            None
        Returns:
            None
        """
        while self.main_window.count() > 0:
            widget = self.main_window.widget(0)
            self.main_window.removeWidget(widget)
            if widget and not widget.parent():
                widget.deleteLater()
    
    def handle_main_window_close(self):
        """
        Handle main window close event.
        Args:
            None
        Returns:
            None
        """
        if self.current_simulator:
            # If there's an active simulator, delegate closing to it
            self.current_simulator.handle_close_request()
        else:
            # Close the application if there's no simulator
            self.app.quit()
    
    def run(self):
        """
        Execute the application.
        Args:
            None
        Returns:
            int: Application exit code
        """
        # Connect the main window close event
        self.main_window.closeEvent = self.main_window_close_event
        return self.app.exec_()
    
    def main_window_close_event(self, event):
        """
        Handle main window close event.
        Args:
            event: The close event
        Returns:
            None
        """
        self.handle_main_window_close()
        event.ignore()  # Let handle_main_window_close decide

def main():
    mode = 1  # GUI mode, 2 for test mode

    if mode == 1:
        app_manager = ApplicationManager()
        sys.exit(app_manager.run())
    elif mode == 2:
        tester = Tester.PlantTester()
        tester.run_all_tests(verbosity=2)

if __name__ == "__main__":
    main()