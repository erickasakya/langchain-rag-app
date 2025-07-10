# Retrieval-Augmented Generation (RAG) APP
## Overview
This application allows users to upload a document and ask questions against the document. The application uses Langchain, GroQ LLM, Azure OpenAI embeddings  and Retrieval-Augmented Generation (RAG).

## APP Features
- Load: Document ingestion
- Split: Document chunking using semantic chuncker, and embedding function from Azure openai.
- Store: This is done using a vector store (chromadb) and Embeddings model
- Retrieve: Given a user input, relevant splits are retrieved from storage using a retriever. 
- Generate: A chatmodel LLM(GroQ) produces an answer using a prompt that includes both the question with the retrieved data.
- Chat: Streamlit web interface for seamless user interaction

## Tools Used
- Python -> Backend development
- Langchain -> LLM framework
- ChromaDB -> vector store
- Streamlit -> Frontend/Chat Builder
- Docker -> Application packaging tool
- Docker Compose -> Application deployment

## Steps to Run this Application
1. Have the following installed on your machine.
- [Docker](https://docs.docker.com/desktop/?_gl=1*ldm9ra*_gcl_au*MTU3NjU5NDE3MC4xNzUyMTI5Njc0*_ga*MjU0Mzc5MzUwLjE3MTg2MzM0NDQ.*_ga_XJWPQMJYHQ*czE3NTIxMjk2NzQkbzY2JGcxJHQxNzUyMTI5Njc1JGo1OSRsMCRoMA..)
- [Docker-compose](https://docs.docker.com/compose/install/)

2. Clone the Repository

```
git clone https://github.com/erickasakya/langchain-rag-app.git

cd langchain-rag-app
```
3. Build Docker Containers

`docker compose up -d --build`

## Access
Open the browser and enter the url below.

`http://localhost:8502`
