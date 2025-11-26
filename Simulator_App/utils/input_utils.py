# Standard library imports
import os
import io

# Third-party imports
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap

def create_project_validate_inputs(file_path, project_name):
    """
    Validate inputs for creating a new project.
    
    Args:
        file_path (str): Directory path where the project will be created
        project_name (str): Name of the new project
    Returns:
        str: 
            - "VALID":          if inputs are valid, otherwise an error code:
            - "EMPTY_NAME":     Project name is empty
            - "EMPTY_PATH":     File path is empty
            - "DUPLICATE":      A project with the same name already exists in the path
            - "INVALID_PATH":   The provided file path is not a valid directory
    """
    if not project_name:
        return "EMPTY_NAME"
    if not file_path:
        return "EMPTY_PATH"
    if os.path.exists(f"{file_path}/{project_name}.txt"):
        return "DUPLICATE"
    if not os.path.isdir(file_path):
        return "INVALID_PATH"
    return "VALID"



def simulator_create_pixmap_equation(equation: str, fontsize: int = 20, dpi: int = 200) -> QPixmap:
    """
    Generate an QPixmap from a LaTeX equation.
    
    Args:
        equation (str): The equation in LaTeX format (e.g., r"$K_p + \frac{K_i}{s} + K_d s$")
        fontsize (int): Font size for the equation
        dpi (int):      Resolution of the image

    Returns:
        QPixmap: Rendered image of the equation
    """
    # Create a matplotlib figure
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0.5, 0.5, equation, fontsize=fontsize, ha='center', va='center')
    plt.axis('off')

    # Save figure to a bytes buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=dpi, transparent=True)
    plt.close(fig)
    buf.seek(0)

    # Create QPixmap from buffer
    pixmap = QPixmap()
    pixmap.loadFromData(buf.getvalue())
    return pixmap


def must_be_positive(name, value):
    """
    Check if a value is strictly positive (> 0).
    Args:
        name (str):         Name of the variable (for error messages)
        value (float):      Value to check
    Returns:
        str: An empty string if the value is valid, otherwise an error message.
    """
    if value <= 0:
        #raise ValueError(f"{name} must be positive and strictly greater than 0 (got {value}).")
        return f"Error: {name} must be positive and strictly greater than 0 (got {value})."
    else:
        return ""

def must_be_nonnegative(name, value):
    """
    Check if a value is non-negative (>= 0).
    Args:
        name (str):         Name of the variable (for error messages)
        value (float):      Value to check
    Returns:
        str: An empty string if the value is valid, otherwise an error message.
    """
    if value < 0:
        #raise ValueError(f"{name} must be non-negative or zero (got {value}).")
        return f"Error: {name} must be non-negative or zero (got {value})."
    else:
        return ""
    
def cannot_be_zero(name, value):
    """
    Check if a value is not zero.
    Args:
        name (str):         Name of the variable (for error messages)
        value (float):      Value to check
    Returns:
        str: An empty string if the value is valid, otherwise an error message.
    """
    if value == 0:
        #raise ValueError(f"{name} cannot be zero (got {value}).")
        return f"Error: {name} cannot be zero (got {value})."
    else:
        return ""
    

def must_be_negative(name, value):
    """
    Check if a value is strictly negative (< 0).
    Args:
        name (str):         Name of the variable (for error messages)
        value (float):      Value to check
    Returns:
        str: An empty string if the value is valid, otherwise an error message.
    """
    if value >= 0:
        #raise ValueError(f"{name} must be negative (got {value}).")
        return f"Error: {name} must be negative (got {value})."
    else:
        return ""