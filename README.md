# Research Gap Finder

A Generative AI-powered application that helps researchers and students analyze academic research papers to identify gaps, contradictions, and insights using Retrieval-Augmented Generation (RAG).

## Overview

Upload a collection of research papers in PDF format and the application will analyze them using large language models to surface meaningful insights that would otherwise require hours of manual reading.

## Features

- **Gap Finder**: Identifies underexplored topics, missing methodologies, and future research directions across the uploaded papers.
- **Contradiction Detector**: Finds conflicting findings and disagreements between papers on the same topic.
- **General Q&A**: Ask any question and receive a cited answer grounded strictly in the uploaded papers.

## Tech Stack

- **Frontend**: Streamlit
- **Orchestration**: LangChain
- **LLM and Embeddings**: Amazon Bedrock (Amazon Nova Lite, Amazon Titan Embeddings v2)
- **Vector Store**: Pinecone
- **Observability**: LangSmith

## Architecture

The application follows a RAG architecture. Uploaded PDFs are parsed, chunked, and embedded using Amazon Titan Embeddings v2, then stored in a Pinecone vector store. On each query, relevant chunks are retrieved and passed alongside a structured prompt to Amazon Nova Lite via LangChain, which generates a grounded response.
