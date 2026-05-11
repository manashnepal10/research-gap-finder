from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langsmith import traceable
import os
from dotenv import load_dotenv

from core.prompts import (
    GAP_FINDER_PROMPT,
    CONTRADICTION_DETECTOR_PROMPT,
    QA_PROMPT
)
from core.retriever import get_retriever
from utils.bedrock_client import get_model

load_dotenv()

retriever = get_retriever()
model = get_model()
parser = StrOutputParser()

def get_chain(mode):
    prompt = None

    if mode == "gap_finder":
        prompt = GAP_FINDER_PROMPT
    elif mode == "contradiction_detector":
        prompt = CONTRADICTION_DETECTOR_PROMPT
    elif mode == "qa":
        prompt = QA_PROMPT
    else:
        raise ValueError(f"Invalid mode: {mode}. Choose from 'gap_finder', 'contradiction_detector' and 'qa'.")
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | parser
    )

    return chain

@traceable(run_type="chain")
def run_chain(mode, question):
    chain = get_chain(mode)

    response = chain.invoke(question)

    return response