from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

def main():
    working_directory = "calculator"
    directory_to_scan = "."
    files_info = get_files_info(working_directory, directory_to_scan)
    for info in files_info:
        print(f"File: {info['file_path']}, Last Modified: {info['last_modified']}")


    # Example of getting file content
    print(get_file_content(working_directory, "lorem.txt"))
    print(get_file_content(working_directory, "main.py"))
    print(get_file_content(working_directory, "pkg/calculator.py"))
    print(get_file_content(working_directory, "pkg/notexists.py"))
    print(get_file_content(working_directory, "/bin/cat/"))

    #test write file content 
    write_file(working_directory, "test_output.txt", "This is a test content.")
    write_file(working_directory, "subdir/test_output2.txt", "This is another test content in a subdirectory.")
    write_file(working_directory, "test_output.txt", "This content will overwrite the previous content.")
    write_file(working_directory, "subdir/test_output2.txt", "This content will overwrite the previous content in subdirectory.")
    



if __name__ == "__main__":
    main()
