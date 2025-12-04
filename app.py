from fastapi import FastAPI, UploadFile, File, HTTPException

from core.pdf import extract_text_pages
from core.splitter import split_text
from core.embed import embed_texts
from core.vectordb import init_pinecone, upsert_vectors


app = FastAPI(title="DocQuery - Minimal Ingest")


pine_index = init_pinecone()


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
                "chunk_text": chunk[:1000],
            }
            docs.append((doc_id, chunk, meta))

    if not docs:
        return {"status": "no_text_found", "chunks": 0}

    texts = [t for (_id, t, _m) in docs]
    embeddings = embed_texts(texts)

    vectors = []
    for i, emb in enumerate(embeddings):
        vectors.append((docs[i][0], emb, docs[i][2]))

    upsert_vectors(vectors)

    return {"status": "indexed", "chunks": len(vectors)}
