import os
import sys
from dotenv import load_dotenv, find_dotenv
from google import genai
from prompts import system_prompt
from google.genai import types
from call_function import available_functions
import argparse
import functions.get_files_info as get_files_info_module
import functions.get_file_content as get_file_content_module
import functions.write_file as write_file_module
import functions.run_python_file as run_python_file_module

def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant - Thoa's version")
    parser.add_argument ("user_prompt", type=str, help = "Prompt your question to send to Gemini." )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    load_dotenv(find_dotenv(),override=True)
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        print("GEMINI_API_KEY is not set in the environment.")
        sys.exit(1)

    if not args or len(args.user_prompt) < 1:
        print("Please provide a prompt as a command-line argument.")
        sys.exit(1)

    client =genai.Client(api_key = gemini_api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose:
        print (f"Using prompt: {args.user_prompt}\n")
    
    generate_content(client, messages, args.verbose)

def handle_function_call(call: types.FunctionCall):
    #use Dispatch Table where function name maps to actual function
    function_registry = {
        "get_files_info": lambda args: get_files_info_module.get_files_info(
            args.get("working_directory"), 
            args.get("directory", ".")
        ),
        "get_file_content": lambda args: get_file_content_module.get_file_content(
            args.get("file_name"), 
            args.get("working_directory", ".")
        ),
        "write_file": lambda args: write_file_module.write_file(
            args.get("working_directory"), 
            args.get("file_name"),
            args.get("content")
        ),
        "run_python_file": lambda args: run_python_file_module.run_python_file(
            args.get("file_path")
        ),
    }

    #execution
    executor = function_registry.get(call.name)

    if not executor:
        return {"error": f"Function {call.name} not implemented."}
    
    try: 
        return executor(call.args)
    except Exception as e:
        return {"error": f"Execution failed for '{call.name}': {str(e)}"}
    

def generate_content(client, messages, verbose_flag):
    MODEL_ID = "gemini-2.0-flash"
    MAX_FUNCTION_CALLS = 5
    stacked_messages = messages.copy()
    loop_counter = 0
    for iter in range (MAX_FUNCTION_CALLS):
        loop_counter = iter + 1
        try: 
            
            # 1. Model think and decide which tool to call
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=stacked_messages,
                config= types.GenerateContentConfig(
                    system_instruction=system_prompt, 
                    temperature= 0.1,
                    tools=[available_functions]),
            )
            #print (response)

            if not response.candidates or len(response.candidates) == 0:
                print("No candidates returned")
                break
            else: 
                # 2. Loop through candidates to append the content to stacked messages
                for candidate in response.candidates:
                    if candidate.content is None: 
                        continue
                    else: 
                        stacked_messages.append(candidate.content)
            
            # 3. Loop through function calls and execute them
            tool_parts = []
            count_run = 0
            if response.function_calls:
                for requestedFunc in response.function_calls:
                    if requestedFunc.name and count_run < MAX_FUNCTION_CALLS:
                        
                        print(f"Model requested to call function: {requestedFunc.name} with args {requestedFunc.args}")
                        function_ressult = handle_function_call(requestedFunc)
                        
                        tool_parts.append(
                            types.Part.from_function_response(
                                name=requestedFunc.name,
                                response={'result': function_ressult}
                            )
                        )
                        count_run += 1
                            
                if tool_parts : 
                    tool_content = types.Content(role = "tool", parts=tool_parts)
                    stacked_messages.append(tool_content)
                
                #print ("Stacked messages after tool call:", stacked_messages)
            else: 
                #final response without function call
                print (f"Final Response: {response.text}")
                print (f"I have looped through {loop_counter} times.")
                break
    
        except Exception as e:
            print(f"[!] Error occurred: {e}")
            break
        

    
    


if __name__ == "__main__":
    main()