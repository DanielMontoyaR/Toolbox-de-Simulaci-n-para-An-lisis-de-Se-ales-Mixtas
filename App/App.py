import sys
from PyQt5.QtWidgets import (QFileDialog,QApplication, QMainWindow, QWidget, QVBoxLayout,QPushButton, QDialog, QLabel, QLineEdit, QComboBox, QHBoxLayout, QDesktopWidget, QStyle)
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PID Toolbox")
        self.setGeometry(0, 0, 400, 200)
                
        # Icono de la aplicación
        self.setWindowIcon(self.style().standardIcon(getattr(QStyle, 'SP_ComputerIcon')))

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Botones principales
        self.btn_new_project = QPushButton("Crear Proyecto")
        self.btn_open_project = QPushButton("Abrir Proyecto")
        
        # Conectar señales
        self.btn_new_project.clicked.connect(self.show_new_project_dialog)
        self.btn_open_project.clicked.connect(self.open_project)
        
        # Añadir botones al layout
        layout.addWidget(self.btn_new_project)
        layout.addWidget(self.btn_open_project)

        #Label de Error si no se selecciona un archivo válido
        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet("color: red")
        layout.addWidget(self.lbl_error)
        
        # Centrar botones
        layout.addStretch()

        #Centrar ventana
        self.center_on_screen()

    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        window_rect = self.frameGeometry()  # Geometria de la ventana

        # Mover el centro de la ventana al centro de la pantalla
        window_rect.moveCenter(screen.center())
        
        # Mover la ventana a la nueva posición
        self.move(window_rect.topLeft())

    def show_new_project_dialog(self):
        dialog = NewProjectDialog(self)
        if dialog.exec_():
            project_name = dialog.project_name()
            plant_type = dialog.plant_type()
            project_path = dialog.project_path()
            self.create_project(project_name, plant_type, project_path)
            
        
    def create_project(self, project_name, plant_type, project_path=None):
        print(f"Proyecto creado: {project_name}")
        print(f"Tipo de planta: {plant_type}")
        #Acá creamos una nueva interfaz para el proyecto creado basado en los parámetros ingresados
        file_to_save = f"{project_path}/{project_name}.txt" if project_path else f"{project_name}.txt"
        with open(file_to_save, 'w') as file:
            file.write(f"Proyecto: {project_name}\n")
            file.write(f"Tipo de planta: {plant_type}\n")
        print(f"Archivo de proyecto guardado como: {project_name}.txt en ruta {project_path if project_path else 'directorio actual'}")


    

    def open_project(self):

        QfileDialog = QFileDialog()
        file_path, _ = QfileDialog.getOpenFileName(self, "Abrir Proyecto", "", "Archivos de Proyecto (*.txt);;Todos los archivos (*)")
        
        if file_path:
            print(f"Proyecto abierto: {file_path}")

            if not file_path.endswith('.txt'):
                self.lbl_error.setText("Error: El archivo seleccionado no es un archivo de proyecto válido (.txt).")
                return
            else:
                self.lbl_error.setText("")
                #Leer el contenido del archivo seleccionado
                with open(file_path, 'r') as file:
                    content = file.read()
                    print(f"Contenido del archivo:\n{content}")
                #Acá creamos una nueva interfaz para el proyecto abierto basado en el archivo seleccionado
                pass
                
        else:
            print("No se seleccionó ningún archivo")

class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Proyecto")
        self.setModal(True)
        
        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Nombre del proyecto
        lbl_name = QLabel("Nombre del proyecto:")
        self.txt_name = QLineEdit()
        layout.addWidget(lbl_name)
        layout.addWidget(self.txt_name)
        
        #Ruta del proyecto
        lbl_path = QLabel("Ruta del proyecto:")
        self.txt_path = QLineEdit()
        self.btn_browse = QPushButton("Seleccionar Ruta")
        self.btn_browse.clicked.connect(self.create_file_dialog)
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.txt_path)
        path_layout.addWidget(self.btn_browse)
        layout.addWidget(lbl_path)
        layout.addLayout(path_layout)
        
        #Error label for path
        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet("color: red")
        layout.addWidget(self.lbl_error)

        # Tipo de planta
        lbl_plant = QLabel("Tipo de planta:")
        self.cmb_plant = QComboBox()
        self.cmb_plant.addItems(["Ball and Beam", "Telescopio", "Ascensor", "Péndulo Invertido", "Personalizado"])
        layout.addWidget(lbl_plant)
        layout.addWidget(self.cmb_plant)
        
        # Botones
        btn_layout = QHBoxLayout()
        self.btn_create = QPushButton("Crear")
        self.btn_cancel = QPushButton("Cancelar")
        
        btn_layout.addWidget(self.btn_create)
        btn_layout.addWidget(self.btn_cancel)
        
        layout.addLayout(btn_layout)
        
        # Conectar señales
        self.btn_create.clicked.connect(self.validate_inputs)
        self.btn_cancel.clicked.connect(self.reject)
    

    def validate_inputs(self):
        if self.txt_name.text().strip() == "":
            self.lbl_error.setText("El nombre del proyecto no puede estar vacío.")
            return False
        if self.txt_path.text().strip() == "":
            self.lbl_error.setText("La ruta del proyecto no puede estar vacía.")
            return False
        
        if not os.path.isdir(self.txt_path.text()):
            self.lbl_error.setText("La ruta del proyecto no es válida.")
            return False

        self.accept()

    def create_file_dialog(self):
        #Crear explorador de archivos para seleccionar la ruta del proyecto
        file_dialog = QFileDialog()
        selected_path = file_dialog.getExistingDirectory(self, "Seleccionar Directorio")
        print(f"Directorio seleccionado: {selected_path}")
        if selected_path != "":
            self.txt_path.setText(selected_path)
        else:
            print("No se seleccionó ninguna ruta.")
            self.lbl_error.setText("No se seleccionó ninguna ruta.")
        print(f"Ruta seleccionada: {selected_path}")

    def project_name(self):
        return self.txt_name.text()
    
    def plant_type(self):
        return self.cmb_plant.currentText()
    
    def project_path(self):
        return self.txt_path.text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())