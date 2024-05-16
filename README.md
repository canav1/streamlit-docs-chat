# Streamlit Assistant 🤖
Streamlit Assistant is an intelligent chatbot application designed to help users interact with Streamlit documentation. This assistant leverages the power of machine learning models and a MongoDB Atlas vector store to provide accurate and relevant information, reducing the risk of hallucinations in responses.

## Project Overview
### Purpose
The purpose of this project is to create a responsive and interactive chatbot that can assist developers in finding information related to Streamlit. By using embeddings and vector search technology, the assistant can deliver precise answers to user queries, making it easier to navigate through extensive documentation.

## Architecture
### The architecture of this project involves several key components:
1. Embeddings Creation: Initially, embeddings of the Streamlit documentation data are created using a model from the Together platform. These embeddings are then stored in a MongoDB Atlas database.
2. Vector Store: MongoDB Atlas is used to store these embeddings, enabling efficient vector searches.
3. Query Handling: When a user inputs a query, the query is converted into an embedding using the same model. This embedding is then used to search for similar embeddings in the MongoDB vector store.
4. Response Generation: The similar embeddings retrieved from MongoDB are passed to a language model (LLM) from the Together platform, which generates a relevant and accurate response for the user.

#### This approach minimizes the hallucination of the language model by grounding its responses in the actual documentation data.

## User Interaction Guide
User can either enter his custom prompt or choose one from the predefined prompts.

## Local Installation Guide
1. Install dependencies: `pip install -r requirements.txt`
2. Make a .env file and store ATLAS connection url and Together API Key
3. Run the application using `streamlit run streamlit_app.py`
