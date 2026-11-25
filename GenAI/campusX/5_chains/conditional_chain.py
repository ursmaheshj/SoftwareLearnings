from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser  
from langchain_core.runnables import RunnableBranch, RunnableLambda
from pydantic import BaseModel,Field
from typing import Literal

chat_model = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="NA",
    model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M"
)

# ----------pydantic model for sentiment
class Feedback(BaseModel):
    sentiment: Literal["positive","negative"] = Field(description="Gives sentiment of the feedback")

strparser = StrOutputParser()
pydanticparser = PydanticOutputParser(pydantic_object=Feedback)

# ----------Template prompts
conditional_prompt = PromptTemplate(
    template="Classify the sentiment of following user feedback text into positive or negative. Do not return any text except asked format. \n {user_feedback} \n {instructions}",
    input_variables=['user_feedback'],
    partial_variables={'instructions':pydanticparser.get_format_instructions()}
)

positive_prompt = PromptTemplate(
    template="write a proper mail based on positive sentiment provided by user for feedback: {user_feedback}",
    input_variables=['user_feedback']
)
negative_prompt = PromptTemplate(
    template="write a proper mail based on negative sentiment provided by user for feedback: {user_feedback}",
    input_variables=['user_feedback']
)

# ------------Creating chains
sentiment_classifier_chain = conditional_prompt | chat_model | pydanticparser

conditional_chain = RunnableBranch(
    (lambda x: x.sentiment == 'positive',positive_prompt | chat_model | strparser),
    (lambda x: x.sentiment == 'negative',negative_prompt | chat_model | strparser),
    RunnableLambda(lambda x: f'Count not find sentiment: {x}')
)

chain = sentiment_classifier_chain | conditional_chain 

while True:
    user_input = input("feedback:")
    result = chain.invoke({'user_feedback':user_input})
    print(result)
