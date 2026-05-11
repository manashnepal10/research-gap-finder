import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from config import (
    pinecone_index_name,
    embedding_dimension,
)

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

def get_pinecone_index():
    pc = Pinecone(api_key=PINECONE_API_KEY)

    existing_indexes = [index.name for index in pc.list_indexes()]

    if pinecone_index_name not in existing_indexes:
        pc.create_index(
            name=pinecone_index_name,
            dimension=embedding_dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    return pc.Index(name=pinecone_index_name)


if __name__ == "__main__":
    pc = get_pinecone_index()
    print(pc)