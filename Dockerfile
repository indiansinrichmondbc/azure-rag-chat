# Use a base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

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
