import streamlit as st
from langchain_openai import ChatOpenAI

chat_model = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",  # Required by the OpenAI client, ignored by llama-server
    model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M",   # Optional: llama-server uses whichever model is loaded
    temperature=0.7,
)

chat_history=[]

while True:
    user_input = input("you:")
    chat_history.append(user_input)

    if user_input.lower() == 'exit':
        break

    result = chat_model.invoke(chat_history)
    chat_history.append(result)
    print("AI: ",result.content)