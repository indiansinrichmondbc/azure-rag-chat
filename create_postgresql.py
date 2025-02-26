import psycopg2
import os

def create_postgresql_db():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=os.getenv("AZURE_POSTGRES_DB"),
            user=os.getenv("AZURE_POSTGRES_USER"),
            password=os.getenv("AZURE_POSTGRES_PASSWORD"),
            host=os.getenv("AZURE_POSTGRES_HOST"),
            port=os.getenv("AZURE_POSTGRES_PORT")
        )
        cur = conn.cursor()

        # Create a simple table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100)
            )
        """)
        conn.commit()

        print("Table created successfully!")

        cur.close()
        conn.close()
    except psycopg2.OperationalError as e:
        print(f"Error: {e}")
        print("Is the server running on that host and accepting TCP/IP connections?")

if __name__ == "__main__":
    create_postgresql_db()
