# QA Bot with Retrieval-Augmented Generation (RAG)

## Overview

This project implements a Retrieval-Augmented Generation (RAG) model for a Question Answering (QA) bot. The bot retrieves relevant information from a dataset using Pinecone DB and generates coherent answers using Cohere API or an alternative generative model. The project also includes an interactive frontend interface for real-time user interactions.

## Project Structure

```
qa-bot/
│
├── backend/
│   ├── cohere_client.py
│   ├── dataset.py
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   └── Dockerfile
│
├── data/
│   └── sample_data.json
│
├── Dockerfile
└── README.md
```

## Setup and Installation

1. **Clone the Repository**

   ```bash
   git clone <GitHub repository URL>
   cd qa-bot
   ```

2. **Build Docker Images**

   Navigate to the project root directory and build the Docker images for the backend and frontend:

   ```bash
   docker build -t qa-bot-backend:latest -f backend/Dockerfile .
   docker build -t qa-bot-frontend:latest -f frontend/Dockerfile .
   ```

3. **Run the Docker Containers**

   You can use Docker Compose to run the containers. Ensure `docker-compose.yml` is correctly set up.

   ```bash
   docker-compose up
   ```

4. **Access the Frontend**

   Open a browser and navigate to `http://localhost:8501` (or the port specified in your `Dockerfile` for the frontend).

## Usage

1. **Upload Documents**

   Use the frontend interface to upload PDF documents.

2. **Ask Questions**

   After uploading a document, enter your questions in the provided input field.

3. **View Answers**

   The bot will retrieve relevant information from the document and generate answers based on the content.

## Example Queries

- "What is the main topic of the document?"
- "Can you summarize the key points of the document?
