from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
import os

def main():
    working_directory = "calculator"
    directory_to_scan = "."
    files_info = get_files_info(working_directory, directory_to_scan)
    for info in files_info:
        print(f"File: {info['file_path']}, Last Modified: {info['last_modified']}")


    # Example of getting file content
    #print(get_file_content("lorem.txt", working_directory))
    #print(get_file_content("main.py", working_directory))
    #print(get_file_content("pkg/calculator.py", working_directory))
    #print(get_file_content("pkg/notexists.py", working_directory))
    #print(get_file_content("/bin/cat/", working_directory))
    print(get_file_content("prompts.py", "."))


    #test write file content 
    write_file(working_directory, "test_output.txt", "This is a test content.")
    write_file(working_directory, "subdir/test_output2.txt", "This is another test content in a subdirectory.")
    write_file(working_directory, "test_output.txt", "This content will overwrite the previous content.")
    write_file(working_directory, "subdir/test_output2.txt", "This content will overwrite the previous content in subdirectory.")

    #test run python file
    run_python_file("test_output.txt", working_directory)
    run_python_file("main.py", working_directory)

    


if __name__ == "__main__":
    main()
