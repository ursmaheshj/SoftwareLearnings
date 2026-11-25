from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel,RunnableLambda
from langchain_core.output_parsers import StrOutputParser

chat_model = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="NA",
    model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M"
)

# --------Lambda function to print logs inbetween chain steps
def log_parallel(x: dict):
    print("----Parallel outputs:----")
    for k, v in x.items():
        print(f"  {k}: {v}")  # (f"  {k}: {v[100]}") #truncate long outputs
    print("----Parallel outputs end:----")
    return x


# --------str Parser
parser = StrOutputParser()

# --------Templates
template_pros = PromptTemplate(
    template="Write 5 points on pros of {topic}",
    input_variables=['topic']
)

template_cons = PromptTemplate(
    template="Write 5 points on cons of {topic}",
    input_variables=['topic']
)

template_merge = PromptTemplate(
    template="Select top 3 pros and cons and combine both to give 6 top. \n cons: {cons} \n pros:{pros}",
    input_variables=['cons','pros']
)


# ----------Creating parallel runnable 
parralel_runnable = RunnableParallel({
    'pros': template_pros | chat_model | parser,
    'cons': template_cons | chat_model | parser
})

merge_chain = template_merge | chat_model |parser

# chain = parralel_runnable | merge_chain 
chain = parralel_runnable | RunnableLambda(log_parallel) | merge_chain        #using runnablelambda to print inbetween outputs of steps

result = chain.invoke({'topic','Internet'})
print(result)
print(chain.get_graph().draw_mermaid())