from langchain.llms import OpenAI, HuggingFaceHub
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
from database_connection import db_conn
from dotenv import load_dotenv
import os

#loading environment variables 
load_dotenv()

#Using OPEN AI for chain of Thought
cot_llm = OpenAI(api_key = os.getenv('openai.api_key'))

#Prompt for chain of thought to openai

cot_prompt = PromptTemplate(input_variables = ["input"], template="""
                        You are an  AI assistant specalizing in SQL queries. Think step by step to solve thw following:
                        Question:{input}
                        Stepwise Reasoning:
                        """)
# chain of thought function that uses openAI LLM
def chain_of_thought(question):
    return cot_llm(cot_prompt.format(input=question))
#processing query with the user's input and model_choice
def process_query(question, model_choice):
    if model_choice == "OpenAI":
        sql_llm = cot_llm
    else:
        sql_llm = HuggingFaceHub(repo_id = "meta-llama/Llama-3.2-1B", model_kwargs={"temperature":0, "max_length":512})
        db = db_conn()
        sql_chain=SQLDatabaseChain(llm=sql_llm, database=db, verbose=True)
        return sql_chain.run(question)

