# from langchain_openai import OpenAI
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm_model = GoogleGenerativeAI(model='models/gemini-3.5-flash-lite')

result = llm_model.invoke("What is capital of india")

print(result)