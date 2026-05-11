from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.bedrock_client import get_embedding
from langchain_pinecone import PineconeVectorStore
import os
from config import (
    chunk_size,
    chunk_overlap,
    pinecone_index_name,
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
)

embedding_model = get_embedding()

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
    documents = load_and_chunk_pdf(file_path=file_path)

    vectorstore = ingest_documents(chunks=documents)

    return vectorstore

