import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from views.start import Start
from views.simulator import Simulator
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
    

    mainwindow = Simulator(None)
    mainwindow.show()
    

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
