import requests
import json

# =============================
# CONFIG
# =============================
LLAMA_API_URL = "http://localhost:8080"  # llama.cpp REST API
MAX_HISTORY = 10  # keep last N messages for context

# =============================
# Define your tools
# =============================
def getSum(num1, num2):
    return num1+num2+10

def getPrime(num):
    return num+num

# Tool registry
TOOLS = {
    "getSum": getSum,
    "getPrime": getPrime,
}

# =============================
# Helper functions
# =============================
def llama_query(prompt, history):
    """Send prompt + history to llama.cpp API"""
    context = "\n".join(history + [prompt])
    payload = {
        "prompt": context,
        "n_predict": 128
    }
    response = requests.post(LLAMA_API_URL, json=payload)
    if response.status_code != 200:
        return f"Error from LLM API: {response.text}"
    data = response.json()
    return data.get("text", "").strip()

def get_llm_decision(user_input, history):
    """Ask LLM if a tool should be used, return JSON"""
    decision_prompt = f"""
You are an assistant with access to tools.
Available tools: {list(TOOLS.keys())}
Decide if the user input needs a tool. 
If yes, return a JSON object exactly like this:
{{"use_tool": true, "tool_name": "<tool_name>", "params": "<input_for_tool>"}}
If no tool is needed, return: {{"use_tool": false}}
User input: "{user_input}"
"""
    llm_output = llama_query(decision_prompt, history)
    
    # Try to parse JSON
    try:
        return json.loads(llm_output)
    except json.JSONDecodeError:
        # fallback: assume no tool
        return {"use_tool": False}

# =============================
# Main agent loop
# =============================
def main():
    history = []
    print("Assistant is running. Type 'exit' to quit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break

        history.append(f"You: {user_input}")
        # Keep only last MAX_HISTORY messages
        history = history[-MAX_HISTORY:]

        decision = get_llm_decision(user_input, history)
        
        if decision.get("use_tool"):
            tool_name = decision.get("tool_name")
            tool_input = decision.get("params", "")
            tool_func = TOOLS.get(tool_name)
            if tool_func:
                tool_result = tool_func(tool_input)
                print(f"Assistant (tool): {tool_result}")
                history.append(f"Assistant (tool): {tool_result}")
            else:
                print(f"Assistant: Tool '{tool_name}' not found.")
                history.append(f"Assistant: Tool '{tool_name}' not found.")
        else:
            # LLM handles it
            llm_response = llama_query(user_input, history)
            print(f"Assistant: {llm_response}")
            history.append(f"Assistant: {llm_response}")

if __name__ == "__main__":
    main()