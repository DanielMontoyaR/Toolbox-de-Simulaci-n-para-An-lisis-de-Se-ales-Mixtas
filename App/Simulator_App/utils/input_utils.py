import os
def create_project_validate_inputs(file_path, project_name):
    if not project_name:
        return "EMPTY_NAME"
    if not file_path:
        return "EMPTY_PATH"
    if os.path.exists(f"{file_path}/{project_name}.txt"):
        return "DUPLICATE"
    if not os.path.isdir(file_path):
        return "INVALID_PATH"
    return "VALID"
