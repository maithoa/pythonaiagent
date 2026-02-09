## 🤖 ReAct Agent Explorer

  

This project is a functional implementation of a ReAct (Reason + Act) Agent. It demonstrates how an LLM can use a "loop of thought" to interact with local files, analyze code, and solve tasks autonomously.

  

## 📝 Learning Objectives

  

Implementing the Loop: Thought -> Action -> Observation cycle.

  

Tool Integration: Providing Python functions as tools for the LLM.

  

Reasoning: Handling multi-turn logic to achieve complex goals.

  

## 🚀 Quick Start

  

**1. Clone the repository:**

  

    git clone <repository_url>

    cd <repository_name>

  
  

** 2. Environment Setup:**

Create a .env file in the root directory and add your API Key:

  

    GOOGLE_API_KEY=your_actual_key_here

  
  

**3. Run the Agent:**

Execute the agent with a natural language prompt:

  

    python main.py "Explain how the calculator renders results to the terminal"

  
  

🔍 Execution Log (Real-world Output)

  

The following log demonstrates the agent's autonomous process:

  

    Model requested to call function: get_files_info with args {'working_directory': '.'}
    
    Scanning directory: .
    
    Model requested to call function: get_file_content with args {'file_name': 'main.py', 'working_directory': '.'}
    
    Scanning file: main.py
    
    Model requested to call function: get_file_content with args {'file_name': 'calculator/main.py', 'working_directory': '.'}
    
    Scanning file: calculator/main.py
    
    Model requested to call function: get_file_content with args {'file_name': 'calculator/pkg/render.py', 'working_directory': '.'}
    
    Scanning file: calculator/pkg/render.py
    
      
    
    Final Response: The calculator renders results to the terminal by formatting the expression and result into a JSON string and then printing that string to standard output.

  
  

## 🛠️ Integrated Tools

  

`get_files_info:` Lists the directory structure to help the agent navigate.

  

`get_file_content:` Reads the source code of specific files.

  

`write_file:` Allows the agent to create or modify code.

`run_python_file:` Allows the agent to run a .py file and test the output.

  

## ⚠️ Security Warning

  

**[!WARNING]**

This agent executes file operations directly on your local system. Use caution when providing prompts that could lead to file deletion or modification, as this version does not run in a sandboxed environment.