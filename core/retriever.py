from langchain_pinecone import PineconeVectorStore
from config import (
    pinecone_index_name,
    retriever_k,
)
from utils.pinecone_client import get_pinecone_index
from utils.bedrock_client import get_embedding

def get_retriever():
    index = get_pinecone_index()
    embedding = get_embedding()
    vectorstore = PineconeVectorStore(index=index, embedding=embedding)

    retriever = vectorstore.as_retriever(
        search_kwargs = {"k": retriever_k}
    )

    return retriever