import psycopg2
from azure_config import embeddings
import os

def create_chat_chain(vector_store):
    # Create a conversational RAG chain using the provided vector store
    conversational_rag_chain = {
        "vector_store": vector_store,
        "embedding_function": embeddings
    }
    return conversational_rag_chain

def get_vector_store():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )
    cur = conn.cursor()
    cur.execute("SELECT content FROM vector_store")
    rows = cur.fetchall()
    vector_store = [row[0] for row in rows]
    cur.close()
    conn.close()
    return vector_store
