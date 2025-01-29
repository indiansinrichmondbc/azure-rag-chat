# Use a base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install PostgreSQL client and libpq-dev
RUN apt-get update && apt-get install -y postgresql-client libpq-dev

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8501

# Define the entry point to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
