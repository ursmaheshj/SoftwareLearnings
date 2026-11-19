from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage

chat_model = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",  # Required by the OpenAI client, ignored by llama-server
    model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M",   # Optional: llama-server uses whichever model is loaded
    temperature=0.7,
)

# # ----------------Simple ChatBot without langchain messages
# chat_history=[]
# while True:
#     user_input = input("you:")
#     chat_history.append(user_input)

#     if user_input.lower() == 'exit':
#         break

#     result = chat_model.invoke(chat_history)
#     chat_history.append(result)
#     print("AI: ",result.content)
# print(chat_history)


# -----------------Chatbot with langchain messages
chat_history=[
    SystemMessage(content="You are an ai agent, expert in animals and their food!")
]
while True:
    user_input = input("you:")
    chat_history.append(HumanMessage(content=user_input))

    if user_input.lower() == 'exit':
        break

    result = chat_model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print("AI: ",result.content)
print(chat_history)
