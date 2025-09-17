from PyQt5.QtWidgets import QFileDialog

def get_project_file(parent=None):
    file_path, _ = QFileDialog.getOpenFileName(
        parent, "Open Project", "", 
        "Project Archives (*.txt);;All files (*)"
    )
    if not file_path:
        return None
    if not file_path.endswith(".txt"):
        return "INVALID"
    return file_path

def create_project_file(project_name, plant_type, project_path, parent=None):
    print(f"Project Created: {project_name}")
    print(f"Plant Type: {plant_type}")
    #Create a new interface for the created project based on the entered parameters
    file_to_save = f"{project_path}/{project_name}.txt" if project_path else f"{project_name}.txt"
    with open(file_to_save, 'w') as file:
        file.write(f"Project: {project_name}\n")
        file.write(f"Plant type: {plant_type}\n")
    print(f"Project file saved as: {project_name}.txt in path {project_path if project_path else 'current directory'}")
