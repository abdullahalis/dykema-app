from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict
import os
import pickle

class VectorManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", persist_dir: str = "llm/rag/stored_vectors"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)

    def save(self):
        # Save FAISS index
        faiss.write_index(self.index, os.path.join(self.persist_dir, "index.faiss"))
        # Save chunks metadata
        with open(os.path.join(self.persist_dir, "chunks.pkl"), "wb") as f:
            pickle.dump(self.chunks, f)

    def load(self):
        # Load FAISS index
        index_path = os.path.join(self.persist_dir, "index.faiss")
        chunks_path = os.path.join(self.persist_dir, "chunks.pkl")

        if os.path.exists(index_path) and os.path.exists(chunks_path):
            self.index = faiss.read_index(index_path)
            with open(chunks_path, "rb") as f:
                self.chunks = pickle.load(f)
            return True
        return False

    def chunk_document(self, text, chunk_size=1000, overlap=200):
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks
    
    def add_documents(self, pdf_documents: List[Dict[str, str]]):
        if self.load():  # load from disk if available
            print("Loaded existing vector store")
            return
        
        # Split into chunks
        doc_chunks = []
        embeddings_chunks = []
        for doc in pdf_documents:
            chunks = self.chunk_document(doc["text"])
            for chunk in chunks:
                doc_chunks.append({"filename": doc["filename"], "content": chunk})
                embeddings_chunks.append(chunk)
        self.chunks = doc_chunks

        embeddings = self.model.encode(embeddings_chunks, convert_to_numpy=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

        self.save()  # save to disk
        print("Vector store built and saved")

    def search(self, query: str, k: int = 3) -> List[Dict[str, str]]:
        query_vec = self.model.encode([query], convert_to_numpy=True)
        scores, idx = self.index.search(query_vec, k)

        results = []
        for rank, i in enumerate(idx[0]):
            results.append({
                "filename": self.chunks[i]["filename"],
                "content": self.chunks[i]["content"],
            })
        return results
