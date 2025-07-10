import os
# from langchain_community.document_loaders import PyPDFLoader, TextLoader # Comment out or delete this line
from langchain_community.document_loaders import UnstructuredPDFLoader, TextLoader # Add this line
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# --- Configuration ---
DOCUMENTS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "LLM-Test") # Your current path
CHROMA_PERSIST_DIR = "./chroma_db"
OLLAMA_EMBEDDING_MODEL = "mxbai-embed-large"

def ingest_documents():
    print(f"Starting document ingestion from: {DOCUMENTS_DIR}")
    documents = []
    found_files_count = 0

    for root, _, files in os.walk(DOCUMENTS_DIR):
        for file in files:
            file_path = os.path.join(root, file)

            if file.startswith('.'):
                continue

            found_files_count += 1
            if file.lower().endswith(".pdf"):
                try:
                    print(f"  Loading PDF with UnstructuredPDFLoader: {file_path}")
                    # Use UnstructuredPDFLoader here
                    loader = UnstructuredPDFLoader(file_path)
                    documents.extend(loader.load())
                except Exception as e:
                    print(f"  Error loading PDF {file_path} with UnstructuredPDFLoader: {e}")
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
    # RecursiveCharacterTextSplitter is generally still good, but you might
    # experiment with chunk_size and chunk_overlap if answers are still poor.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
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

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_PERSIST_DIR
        )
        vectorstore.persist()
        print("Documents ingested and ChromaDB updated.")
    except Exception as e:
        print(f"An error occurred during embedding or ChromaDB storage: {e}")
        print("Please ensure your Ollama server is running and the embedding model is pulled.")

if __name__ == "__main__":
    ingest_documents()