import streamlit as st
from llm_handler import process_query, chain_of_thought
from database_connection import run_query


st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: left;">
        <h1>Basketball Question Answering Chatbot</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
# Initialize chat history
if "history" not in st.session_state:
    st.session_state["history"] = []
if "model_choice" not in st.session_state:
    st.session_state["model_choice"] = "OpenAI"


# Function to handle message sending
def send_message():
    user_message = st.session_state.user_input
    if user_message and user_message.strip():
        cot_response = chain_of_thought(user_message)
        sql_response = process_query(user_message, st.session_state["model_choice"])
         # Check if SQL response is None
        if sql_response:
            sql_query = sql_response.split("Final SQL query:")[-1].strip()
            result = run_query(sql_query)
        else:
            sql_query = "No SQL query generated."
            result = "No result as the SQL query generation failed."
        response = f"The thought for solving the question was {cot_response} \nThe answer to the question is:{result}"
        st.session_state["history"].append(("You", user_message))
        st.session_state["history"].append(("BQAC", response))
        st.session_state.user_input = ""
#CSS for text bcx to be stuck to bottom 
st.markdown("""
    <style>
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        z-index: 1000;
        padding: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .stTextInput {
        flex-grow: 1;
    }
    .stButton {
        margin-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)

#chat scrolling container
chat_container = st.container()
with chat_container:
    # URLs to icons
    user_icon = "https://cdn-icons-png.flaticon.com/512/4825/4825034.png"  # Example user icon
    bot_icon = "https://cdn-icons-png.flaticon.com/512/4712/4712038.png"  # Example bot icon

# Display chat history with image icons
    for idx, (user, message) in enumerate(st.session_state["history"]):
        if user == "You":
            st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: right;">
                <div style="margin-right: 10px; text-align: right;"><b>You:</b> {message}</div>
                <img src="{user_icon}" width="30">
            </div>
            """,
            unsafe_allow_html=True,
         )
        else:
            st.markdown(
            f"""
            <div style="display: flex; align-items: center;">
                <img src="{bot_icon}" width="30">
                <div style="margin-left: 10px;"><b>CT:</b> {message}</div>
            </div>
            """,
            unsafe_allow_html=True,
            )


#bottom chat input box 
st.markdown('<div class = "fixed-bottom">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([3,1,1])
with col1:

    user_input = st.text_input(
    "Ask anything about basketball from NBA Database:",
    key="user_input",
    placeholder = "Type your basketball question here....."
    )
with col2:
    model_choice = st.selectbox("Model", ("OpenAI", "LLaMA-3.1-1B-instruct"), key="model_choice")
with col3:
  send_button = st.button("Send", on_click=send_message)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<div style = 'height: 100px;'></div>", unsafe_allow_html=True)