import os 
from dotenv import load_dotenv
import boto3
from langchain_aws import BedrockEmbeddings, ChatBedrockConverse
from config import (
    embedding_model_id,
    llm_model_id,
)

load_dotenv()

AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_REGION=os.getenv("AWS_REGION")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN=os.getenv("AWS_SESSION_TOKEN")

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)

def get_embedding():
    embeddings=BedrockEmbeddings(
        client=bedrock_client,
        model_id=embedding_model_id,
    )
    return embeddings

def get_model():
    llm=ChatBedrockConverse(
        client=bedrock_client,
        model=llm_model_id,
        max_tokens=2048,
    )
    return llm

if __name__ == "__main__":
    embeddding = get_embedding()
    llm = get_model()
    print(llm.invoke("Hello!"))