import os
import sys
import json
import subprocess
import platform
from openai import OpenAI

# LLM_BASE_URL = "http://localhost:8080/v1"
# MODEL_NAME = "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M"
# API_KEY = "dummy"  # Replace with your actual API key or set as environment variable
LLM_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL_NAME = "gemini-2.5-flash"
API_KEY = os.getenv("Geminy_API_KEY")  # Replace with your actual API key or set as environment variable

# 1. Initialize OpenAI Client
# It automatically picks up the OPENAI_API_KEY environment variable,
# or you can pass it explicitly: client = OpenAI(api_key="your-key")
client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=API_KEY
)
# Global chat history array
history = []

# Tool function to execute terminal/shell commands
def execute_command(command):
    try:
        # runs the command and captures output
        result = subprocess.run(
            command, 
            shell=True, 
            text=True, 
            capture_output=True, 
            timeout=30
        )
        
        if result.stderr:
            return f"Error: {result.stderr}"
            
        return f"Success: {result.stdout} || Task executed completely"
    except Exception as e:
        return f"Error: {str(e)}"

# 2. Define the tool configuration for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Execute a single terminal/shell command. A command can be to create a folder, file, write on a file, edit the file or delete the file",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": 'It will be a single terminal command. Ex: "mkdir calculator"'
                    }
                },
                "required": ["command"]
            }
        }
    }
]

# Map string names to actual executable functions
available_tools = {
    "execute_command": execute_command
}

def run_agent(user_problem):
    global history
    
    # Add user input to history using OpenAI's format
    history.append({
        "role": "user",
        "content": user_problem
    })

    system_instruction = f"""You are an Website builder expert. You have to create the frontend of the website by analysing the user Input.
    You have access of tool, which can run or execute any shell or terminal command.
    
    Current user operation system is: {platform.system()}
    Give command to the user according to its operating system support.

    <-- What is your job -->
    1: Analyse the user query to see what type of website the want to build
    2: Give them command one by one , step by step
    3: Use available tool execute_command
    4: Always respond with proper step by step tool calls as per users platform

    // Now you can give them command in following below
    1: First create a folder, Ex: mkdir "calulator"
    2: Inside the folder, create index.html , Ex: touch "calculator/index.html"
    3: Then create style.css same as above
    4: Then create script.js
    5: Then write required code in these files

    You have to provide the terminal or shell command to user, they will directly execute it"""

    while True:
        # Merge system instructions into the execution message list
        messages = [{"role": "system", "content": system_instruction}] + history

        response = client.chat.completions.create(
            model=MODEL_NAME,  # Highly efficient tier equivalent to gemini-2.5-flash
            messages=messages,
            tools=tools
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        print("==============================")
        print(response_message)
        print("==============================")
        print(response_message.tool_calls)
        print("==============================")
        # 3. Check if LLM requested a tool execution
        if tool_calls:
            # We must append the raw message containing tool_calls back to history first
            history.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                # OpenAI returns arguments as a JSON string string; parse it to a Python dict
                function_args = json.loads(tool_call.function.arguments)

                print(f"Executing tool: {function_name} with args: {function_args}")
                
                # Fetch and run function
                tool_to_call = available_tools[function_name]
                tool_output = tool_to_call(command=function_args.get("command"))

                # Append the output message explicitly linking back via tool_call_id
                history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": tool_output
                })
        else:
            # If no tools are called, it's the final textual response
            history.append({
                "role": "assistant",
                "content": response_message.content
            })
            print(response_message.content)
            print("==============================")
            print(response_message)
            print("==============================")
            print(response_message.tool_calls)
            print("==============================")
            break

def main():
    print("I am a Python OpenAI cursor: let's create a website")
    try:
        while True:
            user_problem = input("\nAsk me anything--> ")
            if user_problem.lower() in ['exit', 'quit']:
                break
            run_agent(user_problem)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()