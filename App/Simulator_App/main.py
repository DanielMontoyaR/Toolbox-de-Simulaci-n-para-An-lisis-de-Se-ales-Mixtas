import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from views.start import Start
from views.simulator import Simulator
import tests.plant_tester.plant_tester as Tester

MAX_WIDTH = 370
MAX_HEIGHT = 441

def main():

    mode = 1  # Change to 1 to launch the GUI

    if mode == 1: # GUI mode
        # Start Window
        app = QApplication(sys.argv)
        widget = QtWidgets.QStackedWidget()
        mainwindow = Start(widget)
        widget.addWidget(mainwindow)

        widget.setFixedWidth(MAX_WIDTH)
        widget.setFixedHeight(MAX_HEIGHT)
        widget.show()
        sys.exit(app.exec_())

    elif mode == 2:  # Test mode
        # Execute tests
        tester = Tester.PlantTester()
        tester.run_all_tests(verbosity=2)

    

    

    

if __name__ == "__main__":
    main()
