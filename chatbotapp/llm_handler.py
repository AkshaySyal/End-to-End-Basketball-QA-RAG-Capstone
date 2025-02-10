import openai
import os
import re
from dotenv import load_dotenv
load_dotenv()

# Fetch API Key
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def clean_sql_query(sql_query):
    """
    Cleans the SQL query to remove unwanted formatting.
    """
    sql_query = re.sub(r"sql", "", sql_query, flags=re.IGNORECASE).strip()
    sql_query = re.sub(r"", "", sql_query, flags=re.IGNORECASE).strip()
    return sql_query.strip()

def generate_sql_query(user_input):
    database_schema = """ 
    Table common_player_info:
    - person_id (INTEGER, PRIMARY KEY)
    - first_name (TEXT)
    - last_name (TEXT)
    - display_first_last (TEXT)
    - team_name (TEXT)
    - team_abbreviation (TEXT)
    - position (TEXT)
    - height (TEXT)
    - weight (INTEGER)
    - from_year (INTEGER)
    - to_year (INTEGER)
    - draft_year (INTEGER)
    - draft_round (INTEGER)
    - draft_number (INTEGER)
    
    The table contains player information, including their names, teams, positions, height, weight, draft details, and career span.
    """

    prompt = f"""You are an AI that generates SQLite queries based on user input.
    {database_schema}
    
    User Request:
    {user_input}
    
    Generate an SQLite SELECT query that retrieves relevant data. Output ONLY the query, nothing else.
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You generate SQLite queries based on a predefined schema. Return only valid SQL queries without explanation, markdown, or formatting."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=150
    )

    raw_query = response.choices[0].message.content.strip()
    sql_query = clean_sql_query(raw_query)  
    return sql_query