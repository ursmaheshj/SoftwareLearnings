from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

chat_model = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",  # Required by the OpenAI client, ignored by llama-server
    model="bartowski/microsoft_Phi-4-mini-instruct-GGUF:Q4_K_M",   # Optional: llama-server uses whichever model is loaded
    # model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M",   # Optional: llama-server uses whichever model is loaded
)

# ---------------------PromptTemplates
template1 = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=['topic']
)
template2 = PromptTemplate(
    template="Write a 4 line summary on following text.\n {text}",
    input_variables=['text']
)

# ----------------Model invoke: Step 1 - Detailed report

prompt1 = template1.invoke({'topic':'Gold rates'})
result1 = chat_model.invoke(prompt1)

# ----------------Model invoke: Step 2 - 5 line summary

prompt2 = template2.invoke({'text':result1.content})
result2 = chat_model.invoke(prompt2)

print(result1)
print("----------------")
print(result2)