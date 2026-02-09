import os
from google.generativeai import types

def write_file(working_directory: str, filename: str, content: str) -> None:
    """
    Write content to a file.
    Creates the directory and file if they don't exist.
    If file exists, warns before overwriting.
    
    Args:
        working_directory: Directory where the file is located
        filename: name of file to write, assumed to be relative to working_directory
        content: Content to write to the file
    """

    file_path_abs = os.path.abspath(os.path.join(working_directory, filename))
    working_dir_abs = os.path.abspath(os.path.dirname(file_path_abs))
    # Try to read existing file content to warn before overwriting
    try:
        with open(file_path_abs, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    except (OSError, UnicodeError):
        # If the file does not exist or cannot be read/decoded, skip the warning
        existing_content = None
    else:
        print(f"Warning: File '{filename}' already exists with content:")
        print(f"--- Existing Content ---")
        print(existing_content)
        print(f"--- End of Content ---")
        print("This will overwrite the previous content.")


    # Create directory if it doesn't exist and directory path is not empty
    try:
        os.makedirs(working_dir_abs, exist_ok=True)
    except OSError as e:
        print(f"Error: Failed to create directory '{working_dir_abs}': {e}")
        raise
    os.makedirs(working_dir_abs, exist_ok=True)
    # Write to file (creates file if it doesn't exist)
    with open(file_path_abs, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"File '{filename}' has been written successfully in '{working_directory}'.")

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file within a working directory.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "working_directory": types.Schema(
                type="STRING",
                description="The root path where the operation takes place (e.g., './project_alpha'). In case not provided, defaults to current directory."
            ),
            "file_name": types.Schema(
                type="STRING",
                description="The name of the file to read, relative to the working_directory. Eg. source.py"
            ),
            "content": types.Schema(
                type="STRING",
                description="The content to write to the specified file."
            ),
        },
        required=["file_name", "working_directory", "content"] # Required parameters
    ),
)

# Example usage:
if __name__ == "__main__":
    working_directory = "calculator"
    filename = "example_output.txt"
    content = "This is an example content written to the file."
    write_file(working_directory, filename, content)

