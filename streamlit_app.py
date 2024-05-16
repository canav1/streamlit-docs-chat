import os
import pymongo
import streamlit as st
from dotenv import load_dotenv
from llama_index.llms.together import TogetherLLM
from llama_index.core import (
    ServiceContext, 
    StorageContext, 
    VectorStoreIndex
)
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch

# Load environment variables from a .env file
load_dotenv()

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Streamlit Assistant 🤖", 
    page_icon="streamlit-docs-chat-logo.webp", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Retrieve MongoDB Atlas URI and Together API key from environment variables
ATLAS_URI = st.secrets['ATLAS_URI']
TOGETHER_API_KEY = st.secrets['TOGETHER_API_KEY']

# MongoDB database and collection configuration
DB_NAME = "KB"
COLLECTION_NAME = "docs"

# Initialize MongoDB client and specify the collection
client = pymongo.MongoClient(ATLAS_URI)
collection = client[DB_NAME][COLLECTION_NAME]

# Field name for storing vector embeddings in MongoDB
VECTOR_DATABASE_FIELD_NAME = 'embedding'

# Set up embedding model from Together platform
embed_model = TogetherEmbedding(
    model_name = "togethercomputer/m2-bert-80M-8k-retrieval", 
    api_key = TOGETHER_API_KEY
)

# Set up LLM model from Together platform
llm = TogetherLLM(
    model = "mistralai/Mixtral-8x7B-Instruct-v0.1", 
    api_key = TOGETHER_API_KEY
)

# Create service context with embedding model and LLM
service_context = ServiceContext.from_defaults(embed_model = embed_model, llm = llm)

# Set up vector store for MongoDB Atlas
vector_store = MongoDBAtlasVectorSearch(
    mongodb_client = client,
    db_name = DB_NAME, 
    collection_name = COLLECTION_NAME,
    index_name = 'idx_embedding',
)

# Create storage context with the vector store
storage_context = StorageContext.from_defaults(vector_store = vector_store)

# Create a VectorStoreIndex with the vector store and service context
index = VectorStoreIndex.from_vector_store(
    vector_store = vector_store, 
    service_context = service_context
)

# Add a title and description
st.title("Streamlit Assistant 🤖")
st.subheader("Chat with Streamlit Docs, Powered by Mixtral and MongoDB Atlas")

# Define test prompts
test_prompts = [
    "How to use columns in Streamlit?",
    "What are Streamlit input widgets?",
    "How to add a file uploader?",
    "Explain how to use st.write?",
    "Create an interactive data table.",
    "What is the use of sidebar?",
    "How to deploy a Streamlit app?",
    "Supported data formats for upload?",
    "Create a multi-page app in Streamlit.",
    "How to use session state in app?",
    "Purpose of caching in Streamlit?",
    "Add custom CSS styles in Streamlit.",
    "Using form and form submit button?",
    "Display images and videos in Streamlit."
]

# Display prompt buttons in a grid layout
cols = st.columns(4)
for i, prompt in enumerate(test_prompts):
    if cols[i % 4].button(prompt):
        button_pressed = prompt

# Text input for user queries
prompt = st.text_input("Or enter your own query:")

final_prompt = button_pressed if 'button_pressed' in locals() else prompt

# Display the response if a prompt is submitted
if final_prompt:
    response = index.as_query_engine().query(final_prompt)
    st.write(response.response)
