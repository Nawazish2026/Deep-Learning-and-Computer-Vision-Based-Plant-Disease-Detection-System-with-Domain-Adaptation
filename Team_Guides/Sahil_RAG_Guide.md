# 🧠 AI RAG Developer Guide - Sahil (`2201085CS`)

Welcome to the AI Intelligence phase! Your mission is to build the "Real RAG" (Retrieval-Augmented Generation) system. This is what elevates our project from a simple classifier to an advanced agricultural assistant.

## Your Domain
Everything you do should be entirely inside the `/rag-engine` folder. **Do not touch the `ml-training` or `frontend` folders.**

## Your Primary Tasks
1. **Data Sourcing:** Find 2-3 PDF manuals on treating plant diseases (e.g., Apple Scab treatments, Tomato Blight prevention). Put these in `rag-engine/documents/`.
2. **Knowledge Ingestion:** Write an ingestion Python script (`ingest.py`) using **LangChain**. It needs to read your PDFs, split the text into chunks, convert them to embeddings using `Sentence-Transformers`, and save them into a local **FAISS** vector database.
3. **Retrieval Endpoint:** Write a query script (`chat.py`) that takes a user's question, searches FAISS for the right PDF paragraph, and feeds that paragraph into an LLM (like Llama 3 or Gemini) to give a verified, sourced answer.
4. **Integration:** Once your script works, hand it to Ankit so he can wrap it in a FastAPI endpoint!

## Helpful AI Prompt for you to use:
*When you are ready to start coding, paste this exact prompt into the AI assistant:*

> "Pretend to be the AI Integration Lead for this Major Project. Please read my guide at `Team_Guides/Sahil_RAG_Guide.md`. My first task is to write a script to convert agricultural PDFs into a FAISS Vector Database. Please give me the `requirements.txt` I need, and write `rag-engine/ingest.py` using LangChain to split and embed the PDFs."
