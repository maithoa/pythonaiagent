import os

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