Local Document Chatbot with Ollama and RAG
This project implements a local chatbot powered by Ollama and Retrieval-Augmented Generation (RAG). It allows users to query their own documents (e.g., extensive engineering manuals, technical specifications) and receive answers grounded in the content of those documents. The entire system runs locally on your machine, ensuring data privacy and offline accessibility.

Table of Contents
Project Overview

Features

Prerequisites

Installation

1. Install Ollama

2. Pull Required Models

3. Clone the Repository

4. Set Up Python Virtual Environment

5. Install Python Dependencies

Usage

1. Place Your Documents

2. Ingest Documents

3. Start the Chatbot

Common Problems & Troubleshooting

PowerShell cd Path Error

Python SyntaxError: unicodeescape

ModuleNotFoundError

ChromaDB Not Found / Empty Embeddings

Slow Ingestion/Querying on MacBook Air M2 8GB

Model Unable to Find Answers in PDF (e.g., ASME BPVC)

Future Enhancements

Contributing

License

Project Overview
Engineers often need quick access to specific information within large technical documents, even in offline environments. This project provides a solution by creating a local AI chatbot that can answer questions directly from these documents. It utilizes the Retrieval-Augmented Generation (RAG) framework:

Ingestion: Your documents are processed, split into manageable chunks, and converted into numerical representations (embeddings) that capture their semantic meaning. These embeddings are stored in a local vector database (ChromaDB).

Retrieval: When a user asks a question, the question is also converted into an embedding. The system then quickly searches the vector database to find the most semantically relevant document chunks.

Generation: These relevant chunks are provided as context to a powerful Large Language Model (LLM) running locally via Ollama. The LLM then generates an answer based only on the provided context, reducing hallucinations and ensuring relevance to your specific documents.

Features
Local Execution: Runs entirely on your laptop (macOS recommended), ensuring data privacy and offline access.

Document Querying: Ask questions about your PDF and text documents.

Contextual Answers: Answers are derived directly from your ingested documents.

Specific Document Querying: Ability to specify a particular document for the chatbot to focus on using a special syntax.

Open-Source Stack: Built with Ollama, LangChain, and ChromaDB.

Handles Complex PDFs: Utilizes UnstructuredPDFLoader for better text extraction from technical documents with complex layouts (e.g., tables, figures, multi-column text).

Prerequisites
Before you begin, ensure you have the following installed:

Ollama: The local LLM runtime. Download from ollama.com.

Python 3.9+: Recommended version.

git: For cloning the repository.

Installation
1. Install Ollama
If you haven't already, download and install Ollama for your operating system from their official website: https://ollama.com/

Once installed, ensure the Ollama server is running. You can start it manually in a terminal if needed:

ollama serve

Keep this terminal open, or ensure Ollama runs as a background service.

2. Pull Required Models
Open a new terminal window and pull the necessary models for your chatbot:

LLM (for generation): llama3 (recommended for its balance of performance and quality)

ollama pull llama3

Alternatively, for better performance on systems with 8GB RAM, consider phi3:mini by running ollama pull phi3:mini and updating OLLAMA_LLM_MODEL in chatbot.py.

Embedding Model (for retrieval): mxbai-embed-large

ollama pull mxbai-embed-large

Verify that the models are installed by running:

ollama list

3. Clone the Repository
Clone this GitHub repository to your local machine:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

(Replace your-username/your-repo-name.git with the actual path to your repository)

4. Set Up Python Virtual Environment
It is highly recommended to use a Python virtual environment to manage dependencies for your project. This avoids conflicts with other Python projects.

python3 -m venv venv
source venv/bin/activate

Your terminal prompt should now show (venv) at the beginning, indicating the virtual environment is active.

5. Install Python Dependencies
With your virtual environment activated, install the required Python libraries:

pip install langchain-community langchain-ollama pypdf chromadb "unstructured[pdf]"

The "unstructured[pdf]" package is crucial for robust PDF text extraction from complex documents, including those with tables and varying layouts.

Usage
1. Place Your Documents
Place your PDF and/or .txt documents that you want the chatbot to learn from into the LLM-Test directory (the same directory where ingest.py and chatbot.py are located).

Important: For this project's configuration, your documents should be in:
~/Documents/LLM-Test/

(If your documents are in a subfolder, adjust DOCUMENTS_DIR in ingest.py accordingly. E.g., DOCUMENTS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "LLM-Test", "my_docs_folder"))

2. Ingest Documents
This step processes your documents and builds the searchable knowledge base (ChromaDB). This is a one-time process or whenever your documents change.

Before running, ensure:

Your Ollama server is running (ollama serve).

You are in your project directory (LLM-Test).

Your virtual environment is active ((venv) in your prompt).

Crucially, if you've run ingest.py before and are making changes to documents or loaders (like switching to UnstructuredPDFLoader), DELETE the old chroma_db folder first:

rm -rf ./chroma_db

Now, run the ingestion script:

python ingest.py

This process can take a while, especially for large documents (like the ASME BPVC PDF) or a large number of documents. It involves reading, parsing, splitting, and generating embeddings for thousands of text chunks. Be patient!

3. Start the Chatbot
Once ingestion is complete, you can start the chatbot.

Ensure:

Your Ollama server is still running.

You are in your project directory (LLM-Test).

Your virtual environment is active.

python chatbot.py

The chatbot will initialize and then prompt you for questions.

Interacting with the Chatbot:

General Query: Ask any question about your documents.

Engineer (You): What is the purpose of the ASME Boiler and Pressure Vessel Code?

Specific Document Query: To ask a question about a particular document, use the format [filename.pdf] your question.

Engineer (You): [ASME BPVC 2025 Section II part D (metric).pdf] What are the temperature limits for carbon steel?

List Available Documents:

Engineer (You): list docs

Exit Chatbot: Type exit and press Enter.

Common Problems & Troubleshooting
Here are solutions to issues you might encounter, many of which were faced during this project's development:

PowerShell cd Path Error
Problem: Set-Location : A positional parameter cannot be found... when using cd with paths containing spaces.

Solution: Always enclose paths with spaces in double quotes: cd "C:\Users\Your Name\Documents\LLM-Test".

Python SyntaxError: unicodeescape
Problem: SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes... due to backslashes in Windows file paths.

Solution: Use forward slashes (/) in your Python path strings ("C:/Users/Your Name/...") or raw strings (r"C:\Users\Your Name\...").

ModuleNotFoundError
Problem: ModuleNotFoundError: No module named 'langchain_community' or similar.

Cause: Python packages are not installed or are installed in a different Python environment than the one running the script.

Solution:

Ensure your virtual environment is active (source venv/bin/activate).

Run pip install langchain-community langchain-ollama pypdf chromadb "unstructured[pdf]".

Confirm which python and which pip point to locations within your venv directory.

ChromaDB Not Found / Empty Embeddings
Problem: Error: ChromaDB not found... or Loaded 0 raw documents... Created 0 text chunks... ValueError: Expected Embeddings to be non-empty....

Cause:

ingest.py was not run successfully before chatbot.py.

ingest.py could not find your documents in DOCUMENTS_DIR.

ingest.py failed to extract text from your documents (e.g., due to complex PDF formats).

Solution:

Verify DOCUMENTS_DIR in ingest.py is correct and contains accessible documents.

Delete any existing chroma_db folder.

Run python ingest.py and monitor its output for successful document loading and chunk creation.

Slow Ingestion/Querying on MacBook Air M2 8GB
Problem: Ingestion and chatbot response times are very slow.

Cause: 8GB of unified memory is quickly consumed by macOS, other applications, and especially the large Llama3 model, leading to heavy use of slower SSD swap space.

Solution:

Switch to a smaller LLM for primary generation: ollama pull phi3:mini and update OLLAMA_LLM_MODEL = "phi3:mini" in chatbot.py. Phi-3 Mini is much smaller (~1.8GB) and performs surprisingly well.

Minimize other applications running in the background.

This is a fundamental hardware limitation; significant performance gains often require more RAM (e.g., 16GB or 24GB).

Model Unable to Find Answers in PDF (e.g., ASME BPVC)
Problem: Chatbot says the answer isn't in the document, even when you know it is.

Cause: This is almost certainly a PDF parsing quality issue. PyPDFLoader (the default pypdf backend) struggles with complex layouts, tables, and scanned text common in technical documents like ASME BPVC. This results in jumbled text chunks and poor embeddings, so the retrieval system can't find relevant information.

Solution: You are already using UnstructuredPDFLoader, which is the correct solution for this. Ensure:

You have correctly installed unstructured and its PDF dependencies (pip install "unstructured[pdf]").

You have modified ingest.py to use UnstructuredPDFLoader instead of PyPDFLoader.

You deleted the old chroma_db folder (rm -rf ./chroma_db) and re-ran python ingest.py completely after making these changes. The text must be re-extracted and re-embedded with the new loader.

If the problem persists, you may need to examine the page_content of the source_documents retrieved by the chatbot (by temporarily adding print statements in chatbot.py) to verify the text quality.

Future Enhancements
Web Interface: Implement a simple web interface (e.g., with Flask or FastAPI) for a more user-friendly experience.

Document Update/Delete: Add functionality to update or delete specific documents from the ChromaDB without re-ingesting everything.

Advanced Chunking: Experiment with more sophisticated chunking strategies (e.g., semantic chunking, table-aware chunking) using LlamaIndex or custom logic.

Reranking: Integrate a reranker model (e.g., with CohereRerank) to improve the relevance of retrieved chunks before passing them to the LLM.

Multi-document Query: Enhance the specific document query to allow querying across multiple named documents simultaneously.

Streamlined Model Management: Automate checking for Ollama and model availability directly within the Python scripts.

Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to:

Fork the repository.

Create a new branch (git checkout -b feature/your-feature-name).

Make your changes and commit them.

Push to your fork (git push origin feature/your-feature-name).

Open a Pull Request.

License
This project is open-source and available under the MIT License.
