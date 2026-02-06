import os
import sys
from dotenv import load_dotenv, find_dotenv
from huggingface_hub import InferenceClient as hfInferenceClient


def main():


    load_dotenv(find_dotenv(),override=True)

    hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")

    #debug using HF API
    hf_client = hfInferenceClient(token=hugging_face_api_key)

    completion = hf_client.chat.completions.create(
        model="Qwen/Qwen3-Coder-30B-A3B-Instruct",
        messages=[
            {
                "role": "user",
                "content": "How to be professional as FOMOer?"
            }
        ],
        max_tokens=256
     
    )

    print(completion.choices[0].message.content)

    return
if __name__ == "__main__":
    main()
