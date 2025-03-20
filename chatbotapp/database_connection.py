from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
import os
import sqlite3
import pandas as pd

#loading environement variables 
load_dotenv()

#establishing database connection
def db_conn():
    sqlite_path = os.getenv('SQLITE_DB_PATH', 'nba_roster_lower_case (1).db') #default path
    DB_URL = f"sqlite:///{sqlite_path}"
    return SQLDatabase.from_uri(DB_URL)


#Execute SQL query
def run_query(sql_query):
    engine = sqlite3.connect("chatbotapp/nba_roster_lower_case (1).db")
    try:
        df = pd.read_sql(sql_query, con=engine)
        return df.to_string(index=False)
    except Exception as e:
        return f"""Generated Query did not execute."""
