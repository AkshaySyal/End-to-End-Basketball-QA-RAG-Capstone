from database_connection import db_conn
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

#processing query with the user's input and model_choice
def process_query(question, model_choice):
    response = ""
    if model_choice == 'Finetuned-Llama-3.2-3B':
        response = finetuned_model(question)
    elif model_choice == 'Llama-3.2-3B-instruct':
        response = foundational_model(question)
    else:
        response = openai_llm(question)
    return response 

def finetuned_model(question,model='Finetuned-Llama-3.2-3B'):
    return "Not Implemented"

def foundational_model(question,model='Llama-3.2-3B-instruct'):
    return "Not Implemented"

def openai_llm(question,model="gpt-4-turbo"):
    return "Not Implemented"

