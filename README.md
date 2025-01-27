# Modern RAG Chat with Azure OpenAI

This repository contains a Streamlit application that allows users to upload text documents, process them into a vector store using Chroma, and interact with the documents through a conversational RAG (Retrieval-Augmented Generation) chain powered by Azure OpenAI.

## Prerequisites

- Docker
- Azure account (for deploying on Azure Linux)

## Building and Running the Docker Container Locally

1. Clone the repository:

   ```sh
   git clone https://github.com/githubnext/workspace-blank.git
   cd workspace-blank
   ```

2. Build the Docker image:

   ```sh
   docker build -t modern-rag-chat .
   ```

3. Run the Docker container:

   ```sh
   docker run -p 8501:8501 modern-rag-chat
   ```

4. Open your web browser and go to `http://localhost:8501` to access the application.

## Deploying the Docker Container on Azure Linux

1. Create a new Azure Container Registry (ACR) if you don't have one:

   ```sh
   az acr create --resource-group <resource-group> --name <acr-name> --sku Basic
   ```

2. Log in to the ACR:

   ```sh
   az acr login --name <acr-name>
   ```

3. Tag the Docker image with the ACR login server name:

   ```sh
   docker tag modern-rag-chat <acr-name>.azurecr.io/modern-rag-chat
   ```

4. Push the Docker image to the ACR:

   ```sh
   docker push <acr-name>.azurecr.io/modern-rag-chat
   ```

5. Create an Azure Container Instance (ACI) to run the Docker container:

   ```sh
   az container create --resource-group <resource-group> --name modern-rag-chat --image <acr-name>.azurecr.io/modern-rag-chat --dns-name-label modern-rag-chat --ports 8501
   ```

6. Open your web browser and go to `http://<dns-name-label>.<region>.azurecontainer.io:8501` to access the application.
