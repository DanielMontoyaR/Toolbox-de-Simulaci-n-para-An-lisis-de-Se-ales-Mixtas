from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QStandardPaths
from simulation_components.plant import get_plant
from simulation_components.sensor import Sensor
import os
import re
import ast

MIN_SAMPLES = 10
MAX_SAMPLES = 10000


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
    the consistency of all simulation components.

    Returns:
        (bool, str, str): (True, "", "") if valid, or (False, error_message, error_log) if validation errors found.
    """

    if not os.path.exists(file_path):
        return False, "File error", "File does not exist."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return False, "Error: could not read file", f"{e}"

    # Required structure
    required_fields = ["Project:", "Plant type:", "PID:", "Plant:", "Input:", "Sensor:"]
    for field in required_fields:
        if field not in content:
            return False, "File missing required field", f"'{field}' not found in project file."

    # Extract basic sections
    try:
        project_name = re.search(r"Project:\s*(.+)", content)
        project_name = project_name.group(1).strip() if project_name else "Unknown"
        
        plant_type = re.search(r"Plant type:\s*(.+)", content)
        plant_type = plant_type.group(1).strip() if plant_type else "Unknown"
        
        pid_section = re.search(r"PID:\s*(\{.*?\})", content, re.DOTALL)
        plant_section = re.search(r"Plant:\s*(\{.*?\})", content, re.DOTALL)
        input_section = re.search(r"Input:\s*(\{.*?\})", content, re.DOTALL)
        sensor_section = re.search(r"Sensor:\s*(\{.*?\})", content, re.DOTALL)
        
        if not all([pid_section, plant_section, input_section, sensor_section]):
            return False, "Missing sections", "One or more required sections (PID, Plant, Input, Sensor) are missing or malformed."
            
    except Exception as e:
        return False, "Error parsing file structure", f"{e}"

    # Helper function to safely parse dictionary sections
    def parse_section_dict(section_match, section_name):
        if not section_match:
            return None, f"Could not extract {section_name} parameters"
        
        try:
            params_str = section_match.group(1)
            params = ast.literal_eval(params_str)
            if not isinstance(params, dict):
                return None, f"Invalid {section_name} parameter format. Not a dictionary."
            return params, ""
        except Exception as e:
            # Clean up the error message to remove Python internal details
            error_msg = str(e)
            if "malformed node or string" in error_msg or "ast." in error_msg:
                return None, f"Invalid {section_name} parameters: syntax error in dictionary format"
            else:
                return None, f"Error parsing {section_name} parameters."

    # Helper function to validate numeric parameters
    def validate_numeric_params(params, required_keys, section_name):
        errors = []
        for key in required_keys:
            if key not in params:
                errors.append(f"Missing key: {key}")
            elif not isinstance(params[key], (int, float)):
                # Try to convert string to number if possible
                try:
                    if isinstance(params[key], str):
                        params[key] = float(params[key])
                    else:
                        errors.append(f"Key '{key}' must be a number, got {type(params[key])}")
                except (ValueError, TypeError):
                    errors.append(f"Key '{key}' must be a number, got {type(params[key])} with value '{params[key]}'")
        return errors

    # Parse all sections
    pid_params, pid_error = parse_section_dict(pid_section, "PID")
    plant_params, plant_error = parse_section_dict(plant_section, "Plant")
    input_params, input_error = parse_section_dict(input_section, "Input")
    sensor_params, sensor_error = parse_section_dict(sensor_section, "Sensor")

    if any(error for error in [pid_error, plant_error, input_error, sensor_error]):
        error_msg = "; ".join([err for err in [pid_error, plant_error, input_error, sensor_error] if err])
        return False, "Parameter parsing error", error_msg

    # Validate PID parameters
    pid_errors = validate_numeric_params(pid_params, ["kp", "ki", "kd"], "PID")
    if pid_errors:
        return False, "PID parameter error", "; ".join(pid_errors)

    # Validate Input parameters
    input_required_keys = ["step_time", "initial_value", "final_value", "total_time", "sample_time"]
    input_errors = validate_numeric_params(input_params, input_required_keys, "Input")
    
    # Additional input validations
    if "step_time" in input_params and "total_time" in input_params:
        if input_params["step_time"] >= input_params["total_time"]:
            input_errors.append("Step time cannot be greater or equal than total time.")
    
    if "initial_value" in input_params:
        if input_params["initial_value"] < -100 or input_params["initial_value"] > 100:
            input_errors.append("Initial value must be between -100 and 100.")
    
    if "final_value" in input_params:
        if input_params["final_value"] < -100 or input_params["final_value"] > 100:
            input_errors.append("Final value must be between -100 and 100.")
    
    if "total_time" in input_params:
        if input_params["total_time"] > 1000:
            input_errors.append("Total time must be less than or equal to 1000 seconds.")
    
    if "sample_time" in input_params and "total_time" in input_params:
        try:
            num_samples = input_params["total_time"] / input_params["sample_time"]
            if num_samples < MIN_SAMPLES:
                input_errors.append(f"Sample time is too large; there should be at least {MIN_SAMPLES} samples.")
            if num_samples > MAX_SAMPLES:
                input_errors.append(f"Sample time is too small; maximum {MAX_SAMPLES} samples allowed.")
        except (ZeroDivisionError, TypeError):
            input_errors.append("Invalid sample_time or total_time for sample calculation.")
    
    if input_errors:
        return False, "Input parameter error", "; ".join(input_errors)

    # Validate Plant
    try:
        plant_instance = get_plant(plant_type)
    except ValueError as e:
        return False, f"Plant error", f"{str(e)}"

    # Set parameters to the plant model before validation
    try:
        plant_instance.set_parameters(**plant_params)
    except Exception as e:
        return False, f"Error setting plant parameters", f"{e}"

    # Evaluate transfer function to confirm parameter consistency
    tf_result = plant_instance.get_transfer_function()
    if isinstance(tf_result, str):  # If returned error message
        return False, f"Plant parameter error", f"{tf_result}"

    # Validate Sensor
    sensor_required_keys = ["Numerator", "Denominator"]
    sensor_errors = []
    
    for key in sensor_required_keys:
        if key not in sensor_params:
            sensor_errors.append(f"Missing key: {key}")
        elif not isinstance(sensor_params[key], (str, list, int, float)):
            sensor_errors.append(f"Key '{key}' must be a string, list, or number.")
    
    if sensor_errors:
        return False, "Sensor parameter error", "; ".join(sensor_errors)

    # Additional sensor validation for string format
    if isinstance(sensor_params.get("Numerator"), str):
        if not re.match(r"^[0-9+\-*/().,\s]+$", sensor_params["Numerator"]):
            sensor_errors.append("Numerator contains invalid characters.")
    
    if isinstance(sensor_params.get("Denominator"), str):
        if not re.match(r"^[0-9+\-*/().,\s]+$", sensor_params["Denominator"]):
            sensor_errors.append("Denominator contains invalid characters.")
    
    if sensor_errors:
        return False, "Sensor parameter error", "; ".join(sensor_errors)

    # Create sensor instance and validate transfer function
    try:
        sensor_instance = Sensor(**sensor_params)
        sensor_instance.set_parameters(**sensor_params)
        sensor_tf_result = sensor_instance.get_transfer_function()
        
        if isinstance(sensor_tf_result, str):  # If returned error message
            return False, f"Sensor parameter error", f"{sensor_tf_result}"
            
    except Exception as e:
        return False, f"Sensor error", f"{str(e)}"

    # If all checks passed, return validation success
    return True, "", ""


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