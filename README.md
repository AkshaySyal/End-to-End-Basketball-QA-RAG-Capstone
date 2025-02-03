# End-to-End-Basketball-QA-RAG-Capstone

## Purpose
This project aims to democratize basketball analytics by addressing the challenges non-technical users face when working with complex datasets due to limited SQL expertise. By developing a fine-tuned LLM-powered system, the project simplifies SQL query generation, ensuring accurate and consistent data-driven insights. The ultimate goal is to make analytics accessible, enabling better coaching strategies, player evaluations, and fan engagement while tackling key issues like LLM hallucinations and inconsistencies.
## Goal 
These are our technical goals for this project:
- Fine-tune an open source LLM for generating semantically correct SQL queries to answer Analytics Queries
- Deploy the LLM on cloud
- Deploy Chatbot application created using LangChain
- Apply Object-Oriented Design Principles to enhance code quality and maintainability for critical scripts (eg: Benchmarking Script)
- Create an orchestration workflow to augment data and build a custom dataset for fine-tuning
## Setup Instruction
## To run the chatbotapp
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
