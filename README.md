# Docuery – PDF RAG Application

Docuery is a PDF-based Retrieval Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions to get accurate, context-aware answers directly from the content.

## 🚀 Features

Upload and process PDF files \
Generate embeddings for semantic search \
Retrieve relevant chunks using a vector database \
Answer queries using LLM + retrieved context \
REST API built with FastAPI

## 🛠 Tech Stack

Backend: FastAPI, Python \
Embeddings: TfIdf \
Vector DB: Pinecone \
PDF Processing: PyMuPDF \
LLM: Groq Llama 3

## Use Case

Document Q&A \
Study material analysis \
Legal / research document querying

## 📂 Project Flow

Upload PDF \
Extract text \
Create embeddings and store in vector DB \
Query → retrieve relevant chunks \
Generate final answer using LLM

## .env setup
```
PINECONE_API_KEY=
PINECONE_ENVIRONMENT=
PINECONE_INDEX=
GROQ_API_KEY=
```

## ▶️ Run Locally
```
install -r requirements.txt
uvicorn main:app --reload
```
