from PyQt5.QtWidgets import QFileDialog

def get_project_file(parent=None):
    file_path, _ = QFileDialog.getOpenFileName(
        parent, "Abrir Proyecto", "", 
        "Archivos de Proyecto (*.txt);;Todos los archivos (*)"
    )
    if not file_path:
        return None
    if not file_path.endswith(".txt"):
        return "INVALID"
    return file_path

def create_project_file(project_name, plant_type, project_path, parent=None):
    print(f"Proyecto creado: {project_name}")
    print(f"Tipo de planta: {plant_type}")
    #Acá creamos una nueva interfaz para el proyecto creado basado en los parámetros ingresados
    file_to_save = f"{project_path}/{project_name}.txt" if project_path else f"{project_name}.txt"
    with open(file_to_save, 'w') as file:
        file.write(f"Proyecto: {project_name}\n")
        file.write(f"Tipo de planta: {plant_type}\n")
    print(f"Archivo de proyecto guardado como: {project_name}.txt en ruta {project_path if project_path else 'directorio actual'}")
