from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.bedrock_client import get_embedding
from langchain_pinecone import PineconeVectorStore
import os
import random
from config import (
    chunk_size,
    chunk_overlap,
    pinecone_index_name,
    embedding_dimension,
)
from utils.pinecone_client import get_pinecone_index

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
)
embedding_model = get_embedding()

def is_file_already_ingested(filename):
    index = get_pinecone_index()
    random_vector = [random.uniform(-1, 1) for _ in range(embedding_dimension)]

    results = index.query(
        vector=random_vector,
        top_k=1,
        filter={"source": {"$eq": filename}},
        include_metadata=True,
    )

    return len(results["matches"]) > 0

def load_and_chunk_pdf(file_path):
    pdf_loader = PyPDFLoader(file_path=file_path)

    pdf_documents = pdf_loader.load()

    chunked_documents = text_splitter.split_documents(documents=pdf_documents)

    for doc in chunked_documents:
        doc.metadata["source"] = os.path.basename(file_path)

    return chunked_documents


def ingest_documents(chunks):
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embedding_model,
        index_name=pinecone_index_name,
    )
    
    return vectorstore

def process_pdf(file_path):
    # Prevent duplicate
    filename = os.path.basename(file_path)
    if is_file_already_ingested(filename):
        return f"{filename} has already been ingested!"

    documents = load_and_chunk_pdf(file_path=file_path)

    vectorstore = ingest_documents(chunks=documents)

    return vectorstore

