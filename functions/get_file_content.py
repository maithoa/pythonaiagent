def get_file_content(working_directory, file_path):
    import os
    from datetime import datetime

    file_content_string = ""
    target_file = os.path.normpath(os.path.join(working_directory, file_path))
    print(f"Scanning file: {target_file}")

    # Will be True or False§
    abs_file_path = os.path.abspath(target_file)

    
    if not os.path.isfile(target_file):
        print (f"Warning: The file {target_file} is not a file. Skipping scan.")
        return file_content_string
    
    if not abs_file_path.startswith(os.path.abspath(working_directory)):
        print(f"Warning: The target file {target_file} is outside the working directory {working_directory}. Skipping scan.")
        return file_content_string
    
    MAX_CHARS = 1000
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS)
            if len(content) == MAX_CHARS:
                content += "\n... (truncated)"
            file_content_string = content
    except Exception as e:
        print(f"Error reading file {target_file}: {e}")
    

    
    return file_content_string

# Example usage:
if __name__ == "__main__":
    working_directory = "calculator"
    directory_to_scan = "."
    files_info = get_files_info(working_directory, directory_to_scan)
    for info in files_info:
        print(f"File: {info['file_path']}, Last Modified: {info['last_modified']}")