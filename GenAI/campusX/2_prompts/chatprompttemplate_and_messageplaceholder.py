# example of how can we use dynamic ChatPromptTemplate and MessagePlaceholder
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

chat_template = ChatPromptTemplate([
    ('system','You are a helpful customer support agent'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human','{query}')
])

chat_history = []
with open('chathistory.txt') as f:
    chat_history.extend(f.readlines())

chat_template.invoke()