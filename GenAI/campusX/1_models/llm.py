from langchain_openai import OpenAI
# from langchain_google_genai import GoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

# Point OpenAI to your local llama-server
llm_model = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",  # Required by the OpenAI client, ignored by llama-server
    model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M",   # Optional: llama-server uses whichever model is loaded
    temperature=0.7,
)

# llm_model = GoogleGenerativeAI(model='models/gemini-3.5-flash-lite')

result = llm_model.invoke("What is capital of india")

print(result)