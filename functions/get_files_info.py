def get_files_info(working_directory, directory="."):
    import os
    from datetime import datetime

    files_info = []
    target_directory = os.path.normpath(os.path.join(working_directory, directory))
    print(f"Scanning directory: {target_directory}")

    # Will be True or False
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.abspath(target_directory)
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        print(f"Warning: The target directory {target_directory} is outside the working directory {working_directory}. Skipping scan.")
        return files_info
    
    if not os.path.isdir(directory):
        print (f"Warning: The directory {directory} is not a directory. Skipping scan.")
        return files_info

    for root, _, files in os.walk(target_directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, working_directory)
            last_modified_time = os.path.getmtime(file_path)
            last_modified_datetime = datetime.fromtimestamp(last_modified_time)
            files_info.append({
                "file_path": relative_path,
                "last_modified": last_modified_datetime.strftime("%Y-%m-%d %H:%M:%S")
            })

    return files_info

# Example usage:
if __name__ == "__main__":
    working_directory = "calculator"
    directory_to_scan = "."
    files_info = get_files_info(working_directory, directory_to_scan)
    for info in files_info:
        print(f"File: {info['file_path']}, Last Modified: {info['last_modified']}")