import streamlit as st
from llm_handler import generate_sql_query
from database_connection import run_query
import pandas as pd

def main():
    st.set_page_config(page_title="AI Conversational Assistant", layout="centered")
    st.title("Basketball QA Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Ask a question from the basketball database...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        if any(keyword in user_input.lower() for keyword in ["hi", "hello", "how are you", "what's up"]):
            response = "Hello! How can I assist you with your basketball database today?"
        elif "csv" in user_input.lower() or "file" in user_input.lower():
            response = "I can only handle SQL queries related to the basketball database. Please provide a database-related question."
        else:
            sql_query = generate_sql_query(user_input)

            if not sql_query.strip() or "SELECT" not in sql_query.upper():
                response = "The generated query is invalid. Please refine your question."

            else:
                response = f"Generated SQL Query:\n{sql_query}"
                result, columns = run_query(sql_query)
                if columns:
                    df = pd.DataFrame(result, columns=columns)
                    st.dataframe(df)
                elif isinstance(result, str):  
                    st.write(result)
                else:
                    st.write("No results found or invalid query.")


        with st.chat_message("assistant"):
            st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

if __name__== "__main__":
    main()