# capstone/scripts/build_index.py
from dotenv import load_dotenv
import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()  # load .env file

# Define paths
BASE_DIR = Path(__file__).resolve().parents[1]
KB_DIR = BASE_DIR / "kb"
INDEX_DIR = BASE_DIR / "index"

def build_kb_index():
    print(f"Loading documents from: {KB_DIR}")
    loader = DirectoryLoader(str(KB_DIR), glob="*.md", loader_cls=TextLoader, show_progress=True)
    docs = loader.load()
    print(f"Loaded {len(docs)} documents.")

    # Split text into smaller chunks for embedding
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")

    # Create embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Create FAISS index
    db = FAISS.from_documents(chunks, embeddings)

    # Ensure index folder exists
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    # Save FAISS index
    index_path = INDEX_DIR / "faiss_index.bin"
    db.save_local(str(index_path))

    print(f"Index saved to: {index_path}")
    print("Build complete!")

if __name__ == "__main__":
    build_kb_index()
