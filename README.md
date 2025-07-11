Local Document Chatbot with Ollama (RAG)


This project provides a local, privacy-focused chatbot that answers questions based on your own documents. It's perfect for engineers needing quick, offline access to information from large technical manuals or reports.

What it Does
Answers Questions from Your Documents: Get direct answers from your PDFs and text files.

Local & Private: Everything runs on your machine, no data leaves your laptop.

Contextual & Accurate: Uses your document content to provide factual responses.

Handles Complex Documents: Designed to extract information from technical documents with complex layouts.

How to Install and Use
Prerequisites
Ollama: Download and install from ollama.com.

Python 3.9+: Ensure you have a recent Python version.

git: For cloning the repository.

Installation Steps
Pull Ollama Models:
Open your terminal and run:

ollama pull llama3         # Main LLM for generating answers
ollama pull mxbai-embed-large # Embedding model for document search

Ensure your Ollama server is running (ollama serve) in the background.

Clone the Project:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

(Remember to replace your-username/your-repo-name.git with your actual repository URL.)

Set Up Python Environment:
Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install Python Libraries:
With the virtual environment active, install dependencies:

pip install langchain-community langchain-ollama pypdf chromadb "unstructured[pdf]"

Usage
Place Your Documents:
Put your PDF and .txt files directly into the your-repo-name folder (e.g., ~/Documents/your-repo-name/).

Ingest Documents:
This builds the searchable database from your documents.
Important: If you've run this before, delete the chroma_db folder first (rm -rf ./chroma_db).

python ingest.py

This step can take a while for large documents.

Start the Chatbot:

python chatbot.py

Once running, you can ask questions. To query a specific document, use [filename.pdf] your question.
