from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

chat_model = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",  # Required by the OpenAI client, ignored by llama-server
    # model="bartowski/microsoft_Phi-4-mini-instruct-GGUF:Q4_K_M",   # Optional: llama-server uses whichever model is loaded
    model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M",   # Optional: llama-server uses whichever model is loaded
)

# ---------------Pydantic object as schema
class Person(BaseModel):
    name: str = Field(description='Name of the person')
    age: int = Field(description='Age of the person',gt=18)
    city: str = Field(description='Name of the city, person belongs to')

# -------------Creating parser using above pydantic model

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template='Generate basic details of a fictional {place} person (do NOT return the JSON schema itself). \n {instructions}',
    input_variables=['place'],
    partial_variables={'instructions':parser.get_format_instructions()}
)

# ---------------model invoke without chain
# prompt = template.invoke({'place':'indian'})
# result = chat_model.invoke(prompt)
# parsed_result = parser.parse(result.content)

chain = template | chat_model | parser
result = chain.invoke({'place':'japanese'})

print(result)
# print("----------")
# print(parsed_result)

