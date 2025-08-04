#  RAG Chatbot with Gemma 3:1B and Pinecone

A **Retrieval-Augmented Generation (RAG)** chatbot built with **Streamlit**, **Gemma (via Ollama)**, and **Pinecone**.  
Upload **PDF, TXT, or DOCX files**, and chat with your documents in real time.


Demo
![alt text](<Screenshot 2025-08-04 172456.png>),![alt text](<Screenshot 2025-08-04 172524.png>),![alt text](<Screenshot 2025-08-04 172543.png>)

##  Features
✔ Upload **PDF, DOCX, or TXT** files  
✔ Automatic **text extraction and chunking**  
✔ **Embeddings with Sentence Transformers**  
✔ **Vector storage & similarity search using Pinecone**  
✔ **Gemma 3:1B LLM via Ollama** for contextual answers  
✔ **Chat UI with memory** (multi-turn conversations)  

---

##  Tech Stack
- [Streamlit](https://streamlit.io/) – Web UI
- [Pinecone](https://www.pinecone.io/) – Vector database
- [Sentence Transformers](https://www.sbert.net/) – Embeddings
- [Ollama](https://ollama.com/) – Local LLM runtime
- [Gemma 3:1B](https://ollama.com/library/gemma) – Google’s lightweight LLM
- [PyMuPDF](https://pymupdf.readthedocs.io/) – PDF text extraction
- [python-docx](https://python-docx.readthedocs.io/) – DOCX text extraction



---

##  Setup Instructions

###  1. Clone the repository
```bash
git clone https://github.com/SAMWEL-NYANGENA/rag-chatbot.git
cd rag-chatbot

## Create a Virtual Environment

python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

## Install dependencies

pip install -r requirements.txt

## set up environment variables

create a venv or export in your powershell:
PINECONE_API_KEY=your_pinecone_api_key

## Install and configure Ollama

Download Ollama: https://ollama.com/download

Pull Gemma model:
ollama pull gemma:1b

## Run the Streamlit app
streamlit runapp.py

## Usage
Upload a PDF, DOCX, or TXT file.

The app chunks and indexes the text in Pinecone.

Ask a question in the chat input.

Gemma 3:1B retrieves relevant context and generates an answer.






