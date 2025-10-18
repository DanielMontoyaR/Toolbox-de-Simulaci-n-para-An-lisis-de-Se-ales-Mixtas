from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QStandardPaths
from simulation_components.plant import get_plant
import os
import re
import ast


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

def create_project_file(project_name, plant_type, project_path, pid_params, plant_params, input_params, sensor_params, parent=None):
    
    #print(f"Project Created: {project_name}")
    #print(f"Plant Type: {plant_type}")

    #Create a new interface for the created project based on the entered parameters
    file_to_save = f"{project_path}/{project_name}.txt" if project_path else f"{project_name}.txt"
    with open(file_to_save, 'w') as file:
        file.write(f"Project: {project_name}\n")
        file.write(f"Plant type: {plant_type}\n")
        file.write(f"PID: {pid_params}\n")
        file.write(f"Plant: {plant_params}\n")
        file.write(f"Input: {input_params}\n")
        file.write(f"Sensor: {sensor_params}\n")
    
    #print(f"Project file saved as: {project_name}.txt in path {project_path if project_path else 'current directory'}")
    
    return file_to_save

def save_simulation_config(file_path, pid_params, plant_params, input_params, sensor_params, plant_type_fallback=None, project_name=None):
    """
    Saves the current simulator configuration to a text file.
    If the file already contains 'Project:' and 'Plant type:' lines, they are reused.
    If not, the function automatically extracts or generates them.

    Args:
        file_path (str): Full path of the .txt file where the configuration will be saved.
        pid_params (dict): PID controller parameters.
        plant_params (dict): Plant model parameters.
        input_params (dict): Input parameters.
        sensor_params (dict): Sensor parameters.
        plant_type_fallback (str, optional): Fallback plant type if it cannot be read from the file.
        project_name (str, optional): Project name to use (for Save As). If None, extracted from file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Use provided project_name or extract from file path as fallback
    if project_name is None:
        project_name = os.path.splitext(os.path.basename(file_path))[0]
    
    plant_type = "Unknown"

    # Try to read existing headers if the file already exists
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                match_project = re.search(r'^Project:\s*(.+)', content, re.MULTILINE)
                match_plant = re.search(r'^Plant type:\s*(.+)', content, re.MULTILINE)

                # Only use existing project name if no project_name was provided
                if match_project and project_name == os.path.splitext(os.path.basename(file_path))[0]:
                    project_name = match_project.group(1).strip()
                if match_plant:
                    plant_type = match_plant.group(1).strip()
        except Exception as e:
            print(f"Warning: Could not read existing file headers: {e}")

    # If the plant type was not found, use the provided fallback if available
    if plant_type == "Unknown" and plant_type_fallback:
        plant_type = plant_type_fallback

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Project: {project_name}\n")
            f.write(f"Plant type: {plant_type}\n\n")
            f.write(f"PID: {pid_params}\n")
            f.write(f"Plant: {plant_params}\n")
            f.write(f"Input: {input_params}\n")
            f.write(f"Sensor: {sensor_params}\n")

        print(f"Configuration saved successfully at: {file_path}")

    except Exception as e:
        print(f"Error saving configuration: {e}")


def save_simulation_config_as(parent_window, current_file_path, pid_params, plant_params, input_params, sensor_params, plant_type_fallback=None):
    """
    Handle Save As functionality with file dialog and save to new location.
    
    Args:
        parent_window: The parent window for the file dialog
        current_file_path (str): Current file path (for suggesting name)
        pid_params (dict): PID controller parameters
        plant_params (dict): Plant model parameters  
        input_params (dict): Input parameters
        sensor_params (dict): Sensor parameters.
        plant_type_fallback (str, optional): Fallback plant type
        
    Returns:
        str or None: New file path if saved successfully, None if canceled
    """
    # Get the documents directory or the current directory 
    default_dir = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
    if not default_dir:
        default_dir = os.path.dirname(current_file_path) if current_file_path else os.getcwd()
    
    # Suggest name based on current file or "new_project"
    suggested_name = os.path.basename(current_file_path) if current_file_path else "new_project.txt"
    
    # Open dialog to select location and name
    file_path, selected_filter = QFileDialog.getSaveFileName(
        parent_window,
        "Save Simulation As",
        os.path.join(default_dir, suggested_name),
        "Text Files (*.txt);;All Files (*)"
    )
    
    # If the user cancels dialog
    if not file_path:
        print("Save As canceled by user")
        return None
    
    # Ensure the file has a .txt extension
    if not file_path.lower().endswith('.txt'):
        file_path += '.txt'
    
    try:
        # Use the existing save function
        save_simulation_config(
            file_path=file_path,
            pid_params=pid_params,
            plant_params=plant_params,
            input_params=input_params,
            sensor_params=sensor_params,
            plant_type_fallback=plant_type_fallback
        )
        
        print(f"Project saved as: {file_path}")
        return file_path
        
    except Exception as e:
        print(f"Error saving file as {file_path}: {e}")
        QMessageBox.critical(parent_window, "Error", f"Could not save file:\n{str(e)}")
        return None





def validate_project_file(file_path):
    """
    Validates the structure of a project configuration file and checks
    the consistency of the plant model and its parameters.

    Returns:
        (bool, str): (True, "") if valid, or (False, error_message) if invalid.
    """

    if not os.path.exists(file_path):
        return False, "File does not exist."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read file: {e}"

    # Required structure
    required_fields = ["Project:", "Plant type:", "PID:", "Plant:", "Input:"]
    for field in required_fields:
        if field not in content:
            return False, f"Missing required field: '{field}'"

    # Extract Plant type
    match_type = re.search(r"Plant type:\s*(.+)", content)
    if not match_type:
        return False, "Could not determine plant type."
    plant_type = match_type.group(1).strip()

    # Extract Plant parameters
    match_params = re.search(r"Plant:\s*(\{.*?\})", content, re.DOTALL)
    if not match_params:
        return False, "Could not extract plant parameters."
    plant_params_str = match_params.group(1)

    try:
        plant_params = ast.literal_eval(plant_params_str)
        if not isinstance(plant_params, dict):
            return False, "Invalid plant parameter format (not a dictionary)."
    except Exception as e:
        return False, f"Error parsing plant parameters: {e}"

    # Create plant instance
    try:
        plant_instance = get_plant(plant_type)
    except ValueError as e:
        return False, str(e)

    # Set parameters to the model before validation
    try:
        plant_instance.set_parameters(**plant_params)
    except Exception as e:
        return False, f"Error setting plant parameters: {e}"

    # Evaluate transfer function to confirm parameter consistency
    tf_result = plant_instance.get_transfer_function()
    if isinstance(tf_result, str):  # If returned error message
        return False, f"Plant parameter error:\n{tf_result}"

    return True, ""



def extract_params_from_file(file_path):
    """
    Extract PID, Plant, and Input parameters from a project file.
    
    Args:
        file_path (str): Path to the project file
        
    Returns:
        tuple: (pid_params, plant_params, input_params) dictionaries
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found -> {file_path}")
        return {}, {}, {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return {}, {}, {}

    # Helper function to extract a dictionary by key label (e.g., "PID:")
    def extract_dict(label):
        match = re.search(rf"{label}\s*(\{{.*?\}})", content, re.DOTALL)
        if not match:
            print(f"Warning: Section '{label}' not found.")
            return {}
        try:
            return ast.literal_eval(match.group(1))
        except Exception as e:
            print(f"Error parsing {label} section: {e}")
            return {}

    # Extract sections
    pid_params = extract_dict("PID:")
    plant_params = extract_dict("Plant:")
    input_params = extract_dict("Input:")
    sensor_params = extract_dict("Sensor:")

    return pid_params, plant_params, input_params, sensor_params