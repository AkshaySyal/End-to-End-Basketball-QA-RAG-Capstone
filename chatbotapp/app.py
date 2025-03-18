import streamlit as st
from llm_handler import process_query
from database_connection import run_query

st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: left;">
        <h1>Basketball QA Chatbot</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize chat history and model choice
if "history" not in st.session_state:
    st.session_state["history"] = []
if "model_choice" not in st.session_state:
    st.session_state["model_choice"] = "Finetuned-Llama-3.2-3B"

# Prewritten example queries
prewritten_queries = [
    "What team is LaMelo Ball on?",
    "What is the number of players on the Chicago Bulls who are 25 years old or younger?",
    "Who is the pointguard for the Golden State Warriors?",
    "What team has the smallest roster?",
    "What's the average age of the Trail Blazers?"
]

# Display example queries at the top
st.markdown("#### Try These Example Queries:")
for query in prewritten_queries:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"📌 `{query}`") 
    with col2:
        if st.button("📋", key=query, help="Copy to input box"):
            st.session_state["user_input"] = query  # Set in session state

# Chat container with scrolling
chat_container = st.container()
with chat_container:
    user_icon = "https://cdn-icons-png.flaticon.com/512/4825/4825034.png"
    bot_icon = "https://cdn-icons-png.flaticon.com/512/4712/4712038.png"

    # Display chat history
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
                    <div style="margin-left: 10px;"><b>BQAC:</b> {message}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# Function to handle message sending
def send_message():
    question = st.session_state.user_input
    choice = st.session_state["model_choice"]
    print(f"QUESTION: {question}")
    print(f"CHOICE: {choice}")
    
    # Process query and get response
    # st.write(process_query(question, choice))
    model_response,generated_query,query_result = process_query(question, choice)
    
    response = f"""
    
    Generated Query: 
    {generated_query}

    Model Response:
    {model_response}
    
    The answer to the question is: 
    {query_result}
    """
    
    # Update chat history
    st.session_state["history"].append(("You", question))
    st.session_state["history"].append(("BQAC", response))
    
    # Clear input by deleting the session state key
    del st.session_state.user_input  # More reliable than setting to empty string

# Fixed-bottom input area
st.markdown(
    """
    <style>
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        z-index: 1000;
        padding: 10px;
    }
    .stTextInput {
        flex-grow: 1;
    }
    .stButton {
        margin-left: 10px;
    }
    /* Increase the width of the selectbox */
    div[data-testid="stSelectbox"] {
        width: 250px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Input widgets inside fixed-bottom container
with st.container():
    st.markdown('<div class="fixed-bottom">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask anything about basketball from NBA Database:",
            key="user_input",  # Let Streamlit manage this key
            placeholder="Type your basketball question here...",
        )
    
    with col2:
        model_choice = st.selectbox(
            "Model", 
            ("Finetuned-Llama-3.2-3B","OpenAI", "Llama-3.2-3B-instruct"), 
            key="model_choice"
        )
        st.button("Send", on_click=send_message)
    
    st.markdown('</div>', unsafe_allow_html=True)
