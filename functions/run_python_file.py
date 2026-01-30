#Code to run a python file
def run_python_file(file_path):
    import subprocess
    import sys
    import os

    abs_file_path = os.path.abspath(file_path)

    if not os.path.isfile(abs_file_path):
        print(f"Error: The file {abs_file_path} does not exist.")
        return
    if not file_path.endswith('.py'):
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