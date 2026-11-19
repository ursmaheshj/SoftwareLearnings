from openai import OpenAI
import subprocess
import json
import os
from pathlib import Path
import dotenv

PLATFORM = os.name
dotenv.load_dotenv()

# LLM_BASE_URL = "http://localhost:8080/v1"
# MODEL_NAME = "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M"
# API_KEY = "dummy"

# LLM_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
# MODEL_NAME = "gemini-2.5-flash"
# API_KEY = os.getenv("Geminy_API_KEY")  # Replace with your actual API key or set as environment variable

# LLM_BASE_URL = "https://api.groq.com/openai/v1"
# MODEL_NAME = "llama-3.3-70b-versatile"
# API_KEY = os.getenv("Groq_API_KEY")  

# LLM_BASE_URL = "https://api.openai.com/v1"
# MODEL_NAME = "gpt-4o-mini"
# API_KEY = os.getenv("Openai_API_KEY")  

LLM_BASE_URL = "https://api.mistral.ai/v1"
MODEL_NAME = "mistral-small-latest"
API_KEY = os.getenv("Mistral_API_KEY")  

client = OpenAI(
    base_url = LLM_BASE_URL,
    api_key = API_KEY
)

history = []

WORKSPACE = Path("./workspace").resolve()
def safe_path(relative_path: str) -> Path:
    p = (WORKSPACE / relative_path).resolve()

    if not str(p).startswith(str(WORKSPACE)):
        raise Exception("Access denied outside workspace")

    return p

def executeCommand(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return f"Success: {result.stdout}"
    except Exception as e:
        return f"Error: {e}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "executeCommand",
            "description": "execute a single terminal/shell command and return the output, command can be to create a file/directory, read a file/directory, list files/directories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "single terminal/shell command to execute eg. 'ls -la' or 'mkdir testfolder'"}
                },
                "required": ["command"]
            }
        }
    }
]

TOOLS_MAP = {"executeCommand": executeCommand}

SYSTEM_PROMPT = f"""You are a coding assistant helping create software projects in a local development environment. You can execute terminal/shell commands to create files, directories, and manage projects.

WORKSPACE: {WORKSPACE}
PLATFORM: {PLATFORM}

CRITICAL RULES FOR COMMANDS:
1. ALL commands must work within the workspace: {WORKSPACE}
2. DO NOT use 'cd' commands - they don't persist across executions
3. Instead, construct full file paths or use relative paths from the workspace
4. For file operations: use full path like "{WORKSPACE}\\project_name\\file.txt" on Windows or "{WORKSPACE}/project_name/file.txt" on Linux/Mac
5. When creating multi-line files, use appropriate syntax for {PLATFORM}:
   - Windows: Use `(echo line1 & echo line2) > file.txt` or heredoc syntax
   - Linux/Mac: Use heredoc with `cat > file.txt << 'EOF'`

EXECUTION WORKFLOW:
1. Break down user request into small steps
2. For each step, provide ONE complete, self-contained command
3. Each command must include the full workspace path - don't rely on directory context
4. Example: `mkdir "{WORKSPACE}\\tic_tac_toe"` (Windows) or `mkdir "{WORKSPACE}/tic_tac_toe"` (Linux)
5. When done with tool calls, provide a clear final message to the user

RESPONSE FORMAT:
- When calling tools: Respond ONLY with valid JSON tool calls, no markdown or explanations
- When summarizing: Use plain text, no markdown formatting
- Always use absolute paths or paths relative to workspace with full context

Examples:
CORRECT: mkdir "{WORKSPACE}\\my_project"
WRONG: cd workspace && mkdir my_project
CORRECT: echo content > "{WORKSPACE}\\my_project\\file.txt"
WRONG: cd my_project && echo content > file.txt
"""

def runAgent(user_input):
    print("running agent with user input:", user_input)
    global history
    history.append({
        "role": "user",
        "content": user_input
    })
    while True:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools
        )
        responseMessage = response.choices[0].message
        tool_calls = responseMessage.tool_calls

        if tool_calls:
            history.append(responseMessage)

            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                print(f"executing tool:{tool_name}, with args:{tool_args}")
                tool_to_call = TOOLS_MAP.get(tool_name)
                tool_output = tool_to_call(command=tool_args.get("command"))

                history.append({
                    "role":"tool",
                    "tool_call_id": tool_call.id,
                    "name":tool_name,
                    "content":tool_output
                })
        else:
            history.append({
                "role":"assistant",
                "content":responseMessage.content
            })
            print("=====================")
            print(history)
            print("=====================")

            break
                

def main():

    print("====================================")
    print(" Local LLM Cursor")
    print(" Folder used:", WORKSPACE)
    print("====================================")

    try:
        while True:
            user_input = input('\nYou >')

            if user_input.lower() in ["quit","exit"]:
                break

            runAgent(user_input)
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()


if __name__ == "__main__":
    main()







# messages = []
# user_input = None
# c = 1
# while True:
#     print(f"Loop {c}")
#     c += 1
    
#     if not user_input:
#         user_input = input("Enter your message: ")
#         if user_input.lower().strip() == "quit":
#             break
#         print(user_input)
#         # Append the new user message to the history
#         messages.append({"role": "user", "content": user_input})
        
#     # Get response from the local model
#     response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=messages,
#         tools=tools,
#         tool_choice="auto"
#     )
    
#     response_message = response.choices[0].message
#     tool_calls = response_message.tool_calls
    
#     # Check if the model wants to call a function
#     if tool_calls:
#         # Append the model's request to call a tool to history
#         messages.append(response_message)
        
#         # Process the tool calls requested by the model
#         for tool_call in tool_calls:
#             function_name = tool_call.function.name
#             # OpenAI returns arguments as a JSON string; we must parse it
#             function_args = json.loads(tool_call.function.arguments)
            
#             if function_name in tools_map:
#                 # Execute your local Python function
#                 function_result = tools_map[function_name](**function_args)
                
#                 # Append the function's result back into the chat history
#                 messages.append({
#                     "tool_call_id": tool_call.id,
#                     "role": "tool",
#                     "name": function_name,
#                     "content": str(function_result),
#                 })
        
#         final_response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=messages
#         )
#         ai_response = final_response.choices[0].message.content
#         messages.append({"role": "assistant", "content": ai_response})
#         print(f"AI: {ai_response}")
#         user_input = None
#     else:
#         # No function call, the model just spoke to the user
#         user_input = None
#         ai_response = response_message.content
#         messages.append({"role": "assistant", "content": ai_response})
#         print(f"AI: {ai_response}")