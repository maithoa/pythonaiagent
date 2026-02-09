import google.genai.types as types
import os
from datetime import datetime


def get_file_content(file_name, working_directory = "."):

    file_content_string = ""
    target_file = os.path.normpath(os.path.join(working_directory, file_name))
    print(f"Scanning file: {target_file}")

    # Will be True or False
    abs_file_path = os.path.abspath(target_file)

    if not os.path.isfile(abs_file_path):
        return f"Warning: The file {abs_file_path} is not a file. Skipping scan."   
    
    if not abs_file_path.startswith(os.path.abspath(working_directory)):
        return f"Warning: The target file {abs_file_path} is outside the working directory {working_directory}. Skipping scan."

    MAX_CHARS = 1000
    try:
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS)
            if len(content) == MAX_CHARS:
                content += "\n... (truncated)"
            file_content_string = content
    except Exception as e:
        return f"Error reading file {abs_file_path}: {e}"

    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file within a working directory.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "file_name": types.Schema(
                type="STRING",
                description="The name of the file to read, relative to the working_directory. Eg. source.py"
            ),
                "working_directory": types.Schema(
                type="STRING",
                description="The root path where the operation takes place (e.g., './project_alpha'). In case not provided, defaults to current directory."
            ),
        },
        required=["file_name", "working_directory"] # Required parameter
    ),
)

# Example usage:
if __name__ == "__main__":
    working_directory = "calculator"
    file_to_read = "example.txt"
    content = get_file_content(file_to_read, working_directory)
    print(content)