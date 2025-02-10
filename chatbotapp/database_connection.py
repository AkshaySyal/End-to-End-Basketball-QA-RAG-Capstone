import sqlite3

def run_query(sql_query):
    conn = sqlite3.connect("nba.sqlite")  
    cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    conn.commit()
    conn.close()
    return result, columns