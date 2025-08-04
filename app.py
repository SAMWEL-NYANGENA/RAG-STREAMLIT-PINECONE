import streamlit as st
import fitz  # PyMuPDF for PDF
import docx
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
import ollama
import os


# 1. Pinecone Setup

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "pcsk_5HuJT1_NpYLisqPo8qTke2Y7WXrpWvCqjaXVqevf1kAdoCGaYDiusAA8f4uSyNhodgorjR")
INDEX_NAME = "rag-app"

pc = Pinecone(api_key=PINECONE_API_KEY)
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
index = pc.Index(INDEX_NAME)

# Embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')


# 2. Helper Functions

def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def add_to_pinecone(chunks):
    embeddings = embedder.encode(chunks).tolist()
    vectors = [(f"id-{i}", embeddings[i], {"text": chunks[i]}) for i in range(len(chunks))]
    index.upsert(vectors)

def rag_query(query, top_k=3):
    q_embedding = embedder.encode([query]).tolist()[0]
    results = index.query(vector=q_embedding, top_k=top_k, include_metadata=True)
    context = "\n".join([match['metadata']['text'] for match in results['matches']])
    
    prompt = f"""Use the following context to answer the question:

{context}

Question: {query}
Answer:
"""
    response = ollama.chat(model="gemma3:1b", messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']


# 3. Streamlit App

st.title(" RAG App with gemma3:1b")
st.write("Upload a PDF, TXT, or DOCX file and ask questions.")

# File upload
uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt", "docx"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(uploaded_file)
    
    st.success("File uploaded successfully!")
    st.write(f"Document length: {len(text)} characters")

    # Chunk and add to Pinecone
    chunks = chunk_text(text)
    add_to_pinecone(chunks)
    st.info(f"Indexed {len(chunks)} chunks into Pinecone.")

# User query
query = st.text_input("Ask a question about your document:")
if st.button("Get Answer") and query:
    with st.spinner("Thinking..."):
        answer = rag_query(query)
    st.subheader("Answer:")
    st.write(answer)
