from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
import os

#loading environement variables 
load_dotenv()

#establishing database connection
def db_conn():
    sqlite_path = os.getenv('SQLITE_DB_PATH', 'nba_database.sqlite') #default path
    DB_URL = f"sqlite:///{sqlite_path}"
    return SQLDatabase.from_uri(DB_URL)


#Execute SQL query
def run_query(sql_query):
    db = db_conn()
    with db._engine.connect() as connection:
        return connection.execute(sql_query).fetchall()