from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

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

# ---------------Creating Parser object

parser = StrOutputParser()

# ---------------Creating Chain using templates and parser object

chain = template1 | chat_model | parser | template2 | chat_model | parser

result = chain.invoke({'topic':'Gold rates'})

print(result)