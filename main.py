import os
import sys
from dotenv import load_dotenv, find_dotenv
from google import genai

def main():
    load_dotenv(find_dotenv(),override=True)
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        print("GEMINI_API_KEY is not set in the environment.")
        sys.exit(1)

    if not sys.argv or len(sys.argv) < 2:
        print("Please provide a prompt as a command-line argument.")
        sys.exit(1)

    prompt = "".join(sys.argv[1:])
    print (f"Using prompt: {prompt}")

    client = genai.Client(api_key=gemini_api_key)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    if response is None or not response.text:
        print("No response received from the API.")
        return
    
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Total tokens: {response.usage_metadata.total_token_count}")

if __name__ == "__main__":
    main()