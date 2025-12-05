import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from core.embed import embed_texts
from core.llm import ask_llm
from core.vectordb import init_pinecone, upsert_vectors, clear_index

from core.pdf import extract_text_pages
from core.splitter import split_text

app = FastAPI(title="DocQuery - Minimal Ingest")


pine_index = init_pinecone()


def clean_matches(matches):
    cleaned = []
    for m in matches:
        cleaned.append({
            "id": m["id"],
            "score": float(m["score"]),
            "metadata": dict(m["metadata"])
        })
    return cleaned


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    pdf_bytes = await file.read()
    pages = extract_text_pages(pdf_bytes)

    docs = []

    for p in pages:
        chunks = split_text(p["text"])
        for i, chunk in enumerate(chunks):
            doc_id = f"{file.filename}_p{p['page_no']}_c{i}"
            meta = {
                "source": file.filename,
                "page": p["page_no"],
                "chunk_text": chunk[:1000]
            }
            docs.append((doc_id, chunk, meta))

    if not docs:
        return {"status": "no_text_found", "chunks": 0}
    clear_index()

    texts = [t for (_id, t, _m) in docs]
    embeddings = embed_texts(texts)

    vectors = []
    for i, emb in enumerate(embeddings):
        vectors.append((docs[i][0], emb, docs[i][2]))

    upsert_vectors(vectors)

    return {"status": "indexed", "chunks": len(vectors)}


@app.post("/query")
async def query_api(question: str):

    q_emb = embed_texts([question])[0]
    q_emb = q_emb.tolist()  

    results = pine_index.query(
        vector=q_emb,
        top_k=5,
        include_metadata=True
    )

    context = ""
    for match in results["matches"]:
        chunk = match["metadata"].get("chunk_text", "")
        context += chunk + "\n\n"

    answer = ask_llm(question, context)

    return {
        "question": question,
        "answer": str(answer),
        "sources": clean_matches(results["matches"])
    }
