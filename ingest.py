import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings # Updated import
from langchain_community.vectorstores import Chroma

# --- Configuration ---
# IMPORTANT: Adjust this path to the directory where your documents are located on your Mac.
# This example assumes your documents are in the same directory as ingest.py
# If your documents are in a subfolder, e.g., 'data', then change this:
# DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "data")
DOCUMENTS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Test-doc")

CHROMA_PERSIST_DIR = "./chroma_db" # Where your vector database will be stored (relative to script location)
OLLAMA_EMBEDDING_MODEL = "mxbai-embed-large" # The embedding model you pulled

def ingest_documents():
    print(f"Starting document ingestion from: {DOCUMENTS_DIR}")
    documents = []
    found_files_count = 0

    # Walk through the specified directory to find documents
    for root, _, files in os.walk(DOCUMENTS_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip hidden files or system files that might start with '.'
            if file.startswith('.'):
                continue

            found_files_count += 1
            if file.lower().endswith(".pdf"):
                try:
                    print(f"  Loading PDF: {file_path}")
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())
                except Exception as e:
                    print(f"  Error loading PDF {file_path}: {e}")
            elif file.lower().endswith(".txt"):
                try:
                    print(f"  Loading TXT: {file_path}")
                    loader = TextLoader(file_path)
                    documents.extend(loader.load())
                except Exception as e:
                    print(f"  Error loading TXT {file_path}: {e}")
            else:
                print(f"  Skipping unsupported file type: {file_path}")
                
    if found_files_count == 0:
        print(f"WARNING: No files found in '{DOCUMENTS_DIR}' or its subdirectories. Please ensure documents are present.")
        print("Ingestion halted. No documents to process.")
        return

    print(f"Successfully loaded {len(documents)} raw documents (from {found_files_count} files found).")

    if not documents:
        print("No content extracted from loaded documents. Perhaps they were empty or unreadable.")
        return

    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # Max characters per chunk
        chunk_overlap=200,    # Overlap between chunks to maintain context
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks.")

    if not chunks:
        print("No text chunks were created after splitting. This might mean the documents were too small or empty.")
        return

    print("Creating embeddings and storing in ChromaDB...")
    try:
        embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL)

        # Create/load the Chroma vector store
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_PERSIST_DIR
        )
        vectorstore.persist() # Save the database to disk
        print("Documents ingested and ChromaDB updated.")
    except Exception as e:
        print(f"An error occurred during embedding or ChromaDB storage: {e}")
        print("Please ensure your Ollama server is running and the embedding model is pulled.")

if __name__ == "__main__":
    ingest_documents()