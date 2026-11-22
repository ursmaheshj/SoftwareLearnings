from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

chat_model = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",  # Required by the OpenAI client, ignored by llama-server
    model="bartowski/microsoft_Phi-4-mini-instruct-GGUF:Q4_K_M",   # Optional: llama-server uses whichever model is loaded
    # model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M",   # Optional: llama-server uses whichever model is loaded
)

# --------------Creating json parser object
parser = JsonOutputParser()

# --------------Using parser in Prompt template
template = PromptTemplate(
    template="Give a fictional person details. \n {instructions}",
    partial_variables={'instructions':parser.get_format_instructions()}
)

# -------------Using model invokation
# prompt = template.format()
# result = chat_model.invoke(prompt)
# parsed_result = parser.parse(result.content)

# -------------Using chain invokation(few steps)
chain = template | chat_model | parser
result = chain.invoke({})
print(result)
print('---------------')
# print(parsed_result)