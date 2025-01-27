from langchain_community.vectorstores.chroma import Chroma
from azure_config import embeddings
import os

def process_documents(uploaded_files):
    # Create a new Chroma vector store
    vector_store = Chroma(
        persist_directory="/app/chroma_db",
        embedding_function=embeddings
    )

    # Process each uploaded file
    for uploaded_file in uploaded_files:
        # Read the content of the file
        content = uploaded_file.read().decode("utf-8")
        
        # Add the content to the vector store
        vector_store.add_texts([content])

    # Save the vector store to the specified directory
    vector_store.persist()

    return vector_store
