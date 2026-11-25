from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel,Field

chat_model = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="NA",
    model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M"
)

# Pydantic Parser Model
class Article(BaseModel):
    title: str = Field(description="Title of article")
    topics: list[str] = Field(description="Topics covered in article")
    wordcount: int = Field(description="Count of words written in article")

# ------------------Parsers
str_parser = StrOutputParser()
pydantic_parser = PydanticOutputParser(pydantic_object=Article)

# ------------------Templates
template1 = PromptTemplate(
    template="Write an article about {topic}",
    input_variables=['topic']
)
template2 = PromptTemplate(
    template="Given the article below, respond with ONLY a valid JSON object. Do NOT write code. Do NOT explain. Do NOT use markdown code fences. Just the raw JSON object. \n Article: {article} \n {instructions}",
    input_variables=['article'],
    partial_variables={'instructions':pydantic_parser.get_format_instructions()}
)

# -----------------creating chain
chain = template1 | chat_model | str_parser | template2 | chat_model | pydantic_parser

result = chain.invoke({'topic':'cricket'})

print(result)