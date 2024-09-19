import os
from langchain_openai import ChatOpenAI



# Configurer LLM
llm = ChatOpenAI(
    openai_api_key= os.getenv('OPENAI_API_KEY'),
    model="gpt-4o",
)