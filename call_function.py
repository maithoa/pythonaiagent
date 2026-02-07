import google.genai.types as types
import functions.get_files_info as get_files_info_module
import functions.get_file_content as get_file_content_module


available_functions = types.Tool(
    function_declarations=[get_files_info_module.schema_get_files_info, 
                           get_file_content_module.schema_get_file_content]
)