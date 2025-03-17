from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
import os
import sqlite3
import pandas as pd

#loading environement variables 
load_dotenv()

#establishing database connection
def db_conn():
    sqlite_path = os.getenv('SQLITE_DB_PATH', 'nba_roster_lower_case.db') #default path
    DB_URL = f"sqlite:///{sqlite_path}"
    return SQLDatabase.from_uri(DB_URL)


#Execute SQL query
def run_query(sql_query):
    engine = sqlite3.connect(os.getenv('SQLITE_DB_PATH', 'nba_roster_lower_case.db'))
    return pd.read_sql(sql_query, con=engine).to_string(index=False)
    # db = db_conn()
    # with db._engine.connect() as connection:
    #     return connection.execute("select name from nba_roster where team='Golden State Warriors' and POS='PG';").fetchall()
