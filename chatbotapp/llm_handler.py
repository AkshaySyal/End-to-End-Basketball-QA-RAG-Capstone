from database_connection import db_conn,run_query
from dotenv import load_dotenv
import os
import pandas as pd
import requests
import re

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
    url = "https://ebcd-2601-19b-e02-2da0-ce2-94ff-bb12-1a09.ngrok-free.app/api/generate"
    payload = {
        "model": "finetunedllama3.2QuantizedExp1",
        "prompt": question,
        "stream": False
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        model_response = data["response"]
        sql_query = queryExtraction(model_response)
        query_result = run_query(sql_query)
    else:
        sql_query = f"Request failed with status code: {response.status_code}"
        query_result = "NA"
    
    return sql_query,query_result

def foundational_model(question,model='Llama-3.2-3B-instruct'):
    return "Not Implemented"

def openai_llm(question,model="gpt-4-turbo"):
    return "Not Implemented"

def queryExtraction(model_response):
    matches = re.findall(r'(select.*?;)', model_response, re.IGNORECASE | re.DOTALL)
    sql_str = matches[0].strip() if matches else ''
    if sql_str:
        sql_str = sql_str.replace('\n', ' ')  # Remove newlines
        sql_str = re.sub(r'\s+', ' ', sql_str)  # Collapse whitespace
        sql_str = sql_str.rstrip(';') + ';'  # Ensure single ending semicolon
        sql_str = sql_str.lower()  # Standardize case
    
    return sql_str

# Uses llama 3.2-3B-instruct to generate response in a natural tone
def responseGeneration(query_result):
    pass

