import os
import sys
from dotenv import load_dotenv, find_dotenv
from google import genai
from prompts import system_prompt
from google.genai import types
from call_function import available_functions
import argparse
import functions.get_files_info as get_files_info_module
#Change to use Hugging Face API due to Google Gemini API Key rate limit issues
from huggingface_hub import InferenceClient as hfInferenceClient


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant - Thoa's version")
    parser.add_argument ("user_prompt", type=str, help = "Prompt your question to send to Gemini." )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    load_dotenv(find_dotenv(),override=True)
    #gemini_api_key = os.getenv("GEMINI_API_KEY")
    hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")

    #debug using HF API
    hf_client = hfInferenceClient(token=hugging_face_api_key)


    
    #messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    messages = [
            {
                "role": "user",
                "content": args.user_prompt
            }
        ]

    if args.verbose:
        print (f"Using prompt: {args.user_prompt}\n")
    
    generate_content(hf_client, messages, args.verbose)


   



def generate_content(client, messages, verbose_flag):
    try: 
        stacked_messages = list(messages) 
        # 1. Model think and decide which tool to call

     
        response = client.text_generation(
            model="Qwen/Qwen3-Coder-30B-A3B-Instruct",
            messages=stacked_messages,
            

            config= types.GenerateContentConfig(
                system_instruction=system_prompt, 
                temperature= 0.1,
                tools=[available_functions]),
                
        )

        #stacked with response message
        stacked_messages.append(response.candidates[0].content)
        
    
        # Check if there's a function call in the response
        tool_parts = []
        for part in response.candidates[0].content.parts:
            if part.function_call:
                call = part.function_call
                print(f"Model yêu cầu gọi hàm: {call.name} với tham số {call.args}")
    
                # Execute the function call
                if call.name == "get_files_info":
                    function_result = get_files_info_module.get_files_info(call.args.get("working_directory"), call.args.get("directory", "."))
                else: 
                    function_result = {"error": f"Function {call.name} not implemented."}
                
                # tool_parts.append(
                #    types.Part.from_function_response(
                #        name=part.function_call.name,
                #       response={"result": function_result}
                #    )
                # )
                    
        if tool_parts : 
            tool_content = types.Content(role = "tool", parts=tool_parts)
            stacked_messages.append(tool_content)
        
        print (tool_parts)
        print (tool_content)
        return

        # 5. GỬI KẾT QUẢ NGƯỢC LẠI CHO MODEL (Lần 2)
        response_final = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=stacked_messages, # Lịch sử câu hỏi
            config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions]
                ),
            )
        response = response_final
        # Cuối cùng, khi không còn function_call nào, Model sẽ trả về text
        print("\n[Kết quả cuối cùng]:")
        print(response.text)

        if response is None or not response.function_calls:
            print("No function call response received from the API.")
            return

        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    

        if response is None or not response.text:
            print("No response received from the API.")
            return
            
        print("Response:\n" + response.text)

        if verbose_flag:
            print(f"User prompt: {messages[0].parts[0].text}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"Total tokens: {response.usage_metadata.total_token_count}")
    
    except Exception as e:
        print(f"[!] Error occurred: {e}")


if __name__ == "__main__":
    main()