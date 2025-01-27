from langchain_community.vectorstores.chroma import Chroma
from azure_config import embeddings

def create_chat_chain(vector_store):
    # Create a conversational RAG chain using the provided vector store
    conversational_rag_chain = {
        "vector_store": vector_store,
        "embedding_function": embeddings
    }
    return conversational_rag_chain
