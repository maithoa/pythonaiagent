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
#Change to use Hugging Face API due to Google Gemini API Key rate limit issues
#from huggingface_hub import InferenceClient as hfInferenceClient


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
    try: 
        stacked_messages = messages
        # 1. Model think and decide which tool to call
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=stacked_messages,
            config= types.GenerateContentConfig(
                system_instruction=system_prompt, 
                temperature= 0.1,
                tools=[available_functions]),
        )

        if not response.candidates or not response.candidates[0].content:
            print("No candidates returned")
            return
        #stacked with response message
        stacked_messages.append(response.candidates[0].content)

        # Check if there's a function call in the response
        tool_parts = []
        count_run = 0
        print (response.candidates[0].content)
        for part in response.candidates[0].content.parts:
            if part.function_call and count_run < MAX_FUNCTION_CALLS:
                
                print(f"Model requested to call fun ction: {part.function_call.name} with args {part.function_call.args}")
                function_ressult = handle_function_call(part.function_call)
                
                tool_parts.append(
                    types.Part.from_function_response(
                        name=part.function_call.name,
                        response={'result': function_ressult}
                    )
                )
                count_run += 1
                    
        if tool_parts : 
            tool_content = types.Content(role = "tool", parts=tool_parts)
            stacked_messages.append(tool_content)
        
        print ("Stacked messages after tool call:", stacked_messages)

        # 5. SEND CALL RESULT TO MODEL (2nd time)
        response_final = client.models.generate_content(
            model=MODEL_ID,
            contents=stacked_messages, # History of messages
            config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions],
                    temperature=0.1,
                ),
            )
        if not response_final or not response_final.candidates or not response_final.candidates[0].content:
            print("No final candidates returned")
            return
        
        # Cuối cùng, khi không còn function_call nào, Model sẽ trả về text
        print("\n=====================Final Result================:")
        print(response_final.text)
        #print(response_final)

        if verbose_flag:
            print(f"User prompt: {messages[0].parts[0].text}")
            print(f"Prompt tokens: {response_final.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response_final.usage_metadata.candidates_token_count}")
            print(f"Total tokens: {response_final.usage_metadata.total_token_count}")
    
    except Exception as e:
        print(f"[!] Error occurred: {e}")


if __name__ == "__main__":
    main()