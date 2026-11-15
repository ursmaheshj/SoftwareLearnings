from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

chat_model = ChatGoogleGenerativeAI(model='models/gemini-3.5-flash-lite')

result = chat_model.invoke("What is capital of india")

print(result)