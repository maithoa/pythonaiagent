import google.genai.types as types
import functions.get_files_info as get_files_info_module


available_functions = types.Tool(
    function_declarations=[get_files_info_module.schema_get_files_info,]
)