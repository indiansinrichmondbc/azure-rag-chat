import psycopg2
from azure_config import embeddings
import os

def process_documents(uploaded_files):
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=os.getenv("AZURE_POSTGRES_DB"),
        user=os.getenv("AZURE_POSTGRES_USER"),
        password=os.getenv("AZURE_POSTGRES_PASSWORD"),
        host=os.getenv("AZURE_POSTGRES_HOST"),
        port=os.getenv("AZURE_POSTGRES_PORT")
    )
    cur = conn.cursor()

    # Create vector_store table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vector_store (
            id SERIAL PRIMARY KEY,
            content TEXT
        )
    """)
    conn.commit()

    # Process each uploaded file
    for uploaded_file in uploaded_files:
        # Read the content of the file
        content = uploaded_file.read().decode("utf-8")
        
        # Add the content to the vector store
        cur.execute("INSERT INTO vector_store (content) VALUES (%s)", (content,))
    
    conn.commit()
    cur.close()
    conn.close()

    return "PostgreSQL Vector Store"
