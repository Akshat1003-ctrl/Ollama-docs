import os
from langchain_ollama import OllamaLLM as Ollama # Updated import for LLM
from langchain_ollama import OllamaEmbeddings # Updated import for Embeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# --- Configuration ---
CHROMA_PERSIST_DIR = "./chroma_db" # Must match the directory used in ingest.py
OLLAMA_LLM_MODEL = "llama3" # The LLM you pulled (e.g., llama3, mistral)
OLLAMA_EMBEDDING_MODEL = "mxbai-embed-large" # Must match the one used in ingest.py

# IMPORTANT: Ensure your Ollama server is running on this address.
# This is the default. If you configured Ollama differently, change this.
OLLAMA_BASE_URL = "http://localhost:11434" 

def initialize_chatbot():
    print("Initializing chatbot...")
    
    # Check if ChromaDB exists and has content
    if not os.path.exists(CHROMA_PERSIST_DIR) or not os.listdir(CHROMA_PERSIST_DIR):
        print(f"Error: ChromaDB not found or empty at {CHROMA_PERSIST_DIR}.")
        print("Please ensure you have run 'python ingest.py' successfully first.")
        return None

    try:
        # Load the embedding model
        embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)

        # Load the Chroma vector store
        vectorstore = Chroma(
            persist_directory=CHROMA_PERSIST_DIR,
            embedding_function=embeddings
        )
        print("ChromaDB loaded successfully.")

        # Initialize the Ollama LLM
        llm = Ollama(model=OLLAMA_LLM_MODEL, base_url=OLLAMA_BASE_URL)
        print(f"Ollama LLM '{OLLAMA_LLM_MODEL}' connected.")

        # Define a custom prompt template for RAG
        prompt_template = """
        You are a helpful assistant for engineers, providing information based on the provided documents.
        Use only the context provided to answer the question.
        If you don't know the answer or can't find it in the provided context, state that you don't know
        and politely suggest rephrasing the question or checking the documents.
        
        Context: {context}

        Question: {question}

        Answer:
        """
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # Create a RetrievalQA chain
        # 'stuff' combines all retrieved documents into one large context string
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True # This allows us to see which documents were used
        )
        print("Chatbot initialized. Ready to answer questions.")
        return qa_chain
    
    except Exception as e:
        print(f"An error occurred during chatbot initialization: {e}")
        print("Please ensure your Ollama server is running and the models are pulled correctly.")
        return None

def chat_loop(qa_chain):
    if qa_chain is None:
        print("Chatbot could not be initialized. Exiting.")
        return

    print("\n--- Document Chatbot ---")
    print("Type your questions about the documents. Type 'exit' to quit.")

    while True:
        user_input = input("\nEngineer (You): ")
        if user_input.lower() == 'exit':
            print("Exiting chatbot. Goodbye!")
            break
        
        if not user_input.strip(): # Handle empty input
            print("Please enter a question.")
            continue

        try:
            response = qa_chain.invoke({"query": user_input})
            print(f"Chatbot: {response['result']}")

            # Optional: Print sources for transparency
            if response.get('source_documents'):
                print("\nSources (chunks used for answer):")
                for i, doc in enumerate(response['source_documents']):
                    source_info = doc.metadata.get('source', 'Unknown Source')
                    page_info = doc.metadata.get('page', 'N/A')
                    print(f"- Source {i+1}: {os.path.basename(source_info)} (Page: {page_info})")
                    # Optionally print a snippet of the content
                    # print(f"  Snippet: \"{doc.page_content[:200]}...\"") 
            else:
                print("\n(No specific document sources found for this answer - check prompt or document content.)")

        except Exception as e:
            print(f"An error occurred while processing your query: {e}")
            print("Please check your Ollama server connection or the model's status.")


if __name__ == "__main__":
    qa_bot = initialize_chatbot()
    chat_loop(qa_bot)