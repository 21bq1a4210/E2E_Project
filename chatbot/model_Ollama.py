from datetime import datetime
import time
import httpx
from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import pickle
import os
from dotenv import load_dotenv

load_dotenv()

# Function to save data using pickle
from datetime import datetime
import time
import httpx
from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import pickle
import os
from dotenv import load_dotenv

load_dotenv()


# Function to save data using pickle
def save_data(obj, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)


# Function to load data using pickle
def load_data(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


# File paths for serialized data
documents_file = 'chatbot/serialize/documents.pkl'
vector_index_file = 'chatbot/serialize/vector_index.pkl'

# Check if parsed documents already exist
if os.path.exists(documents_file):
    print("Loading pre-parsed documents...")
    documents = load_data(documents_file)
else:
    print("Parsing documents from txt files...")
    parser = LlamaParse(result_type='markdown')
    file_extractor = {'.txt': parser}
    documents = SimpleDirectoryReader('chatbot/data', file_extractor=file_extractor).load_data()
    save_data(documents, documents_file)

# Check if vector index already exists
if os.path.exists(vector_index_file):
    print("Loading pre-built vector index...")
    vector_index = load_data(vector_index_file)
else:
    print("Building vector index...")
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    vector_index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    save_data(vector_index, vector_index_file)

llm = Ollama(model="llama3", request_timeout=60.0)

# Create query engine
query_engine = vector_index.as_query_engine(llm=llm)


# Function to handle retries on queries
def query_with_retry(query, max_retries=3, wait_time=5):
    for attempt in range(max_retries):
        try:
            start_time = datetime.now()
            response = query_engine.query(query)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"Query completed in {duration:.2f} seconds.")

            # Ensure the response is JSON-serializable by returning a string
            return str(response)  # Convert response to a string for serialization
        except httpx.ReadTimeout:
            if attempt < max_retries - 1:
                print(f"Timeout occurred. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    # Main loop for user interaction
    while True:
        q = input("Jai Sri Ram :> ")
        if q.lower() in ['q', 'quit', 'exit']:
            print(":< Bye...")
            break
        response = query_with_retry(q)
        if response:
            print(response)
