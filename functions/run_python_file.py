#Code to run a python file
def run_python_file(file_path, working_directory):
    import subprocess
    import sys
    import os

    # Construct the target file path relative to working directory
    target_file = os.path.normpath(os.path.join(working_directory, file_path))
    abs_file_path = os.path.abspath(target_file)
    working_dir_abs = os.path.abspath(working_directory)

    # Validate that the target file is within the working directory
    try:
        valid_target_file = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
    except ValueError:
        # Different drives on Windows
        valid_target_file = False
    
    if not valid_target_file:
        print(f"Error: The target file {abs_file_path} is outside the working directory {working_dir_abs}. Access denied.")
        return

    if not os.path.isfile(abs_file_path):
        print(f"Error: The file {abs_file_path} does not exist.")
        return
    if not abs_file_path.endswith('.py'):
        print(f"Error: The file {abs_file_path} is not a Python file.")
        return

    try:
        result = subprocess.run([sys.executable, abs_file_path], capture_output=True, text=True, check=True, timeout=30)
        print("Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        if result.returncode !=0:
            print(f"The script exited with return code {result.returncode}")
        else:
            print("The script executed successfully. No output or errors.")
    except subprocess.TimeoutExpired:
        print(f"Error: The file {abs_file_path} exceeded the 30 second timeout.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the file {abs_file_path}:")
        print(e.stderr)

schema_run_python_file = {
    "name": "run_python_file",
    "description": "Executes a specified Python file within a working directory and returns its output or errors.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the Python file to execute, relative to the working_directory."
            },
            "working_directory": {
                "type": "string",
                "description": "The root path where the operation takes place (e.g., './project_alpha')."
            },
        },
        "required": ["file_path", "working_directory"]
    },
}

# Example usage:
if __name__ == "__main__":
    working_directory = "calculator"
    test_file_path = "main.py"
    run_python_file(test_file_path, working_directory)