# End-to-End-Basketball-QA-RAG-Capstone

Streamlit app is live: https://akshaysyal-end-to-end-basketball-qa-rag-c-chatbotappapp-tgfmap.streamlit.app/

<img width="841" alt="image" src="https://github.com/user-attachments/assets/403a050e-6304-4434-b232-70e12cc043d9" />

# To run the chatbotapp locally
1. Clone the repository to your local machine:
   ```bash
   git clone <repository-url>
   cd End-to-End-Basketball-QA-RAG-Capstone
2. Switch to the Chatbot branch
   ```bash
   git checkout chatbotapp
3. Create and Set up your Environment
   ```bash
   python -m venv venv
   source venv/bin/activate
4. Install the packages using `requirements.txt`
   ```bash
   pip install -r chatbotapp/requirements.txt
5. Add your api key, hugging face token and database path(sqlite database path)
   Create a .env file in chatbotapp/ and add:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   HUGGINGFACE_API_TOKEN=your_huggingface_token_here
   DATABASE_PATH=path/to/your/database.db
6. To run the streamlit application
   ```bash
   streamlit run chatbotapp/app.py
