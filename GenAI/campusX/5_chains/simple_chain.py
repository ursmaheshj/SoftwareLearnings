from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

chat_model = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="NA",
    model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M"
)

template = PromptTemplate(
    template="Generate 5 interesting facts about {topic}",
    input_variables=['topic']
)

parser = StrOutputParser()

chain = template | chat_model | parser

result = chain.invoke({'topic':'cricket'})

print(result)

# print(chain.get_graph().print_ascii()) #Needs grandalf library installation
# print(chain.get_graph().draw_mermaid())
# print(chain.get_graph().draw_mermaid_png()) #gives png in bytes

