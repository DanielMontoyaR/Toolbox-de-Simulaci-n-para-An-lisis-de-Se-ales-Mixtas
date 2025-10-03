import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from views.start import Start
from views.simulator import Simulator
import tests.plant_tester  as Tester
def main():
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    # Ventana de start
    """
    mainwindow = Start(widget)
    widget.addWidget(mainwindow)

    #widget.setFixedWidth(370)
    #widget.setFixedHeight(441)
    widget.show()
    """


    #Tester.run_all_tests()
    plant_types = ["Ball and Beam", "DC Motor Speed Control", "DC Motor Position Control", "Personalized Plant"]
    mainwindow = Simulator(plant_types[0])
    mainwindow.show()
    

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
