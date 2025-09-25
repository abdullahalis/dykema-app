from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict
import os
import pickle

class VectorManager:
    """Manages vector embeddings and FAISS index for document retrieval."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", persist_dir: str = "llm/rag/stored_vectors"):
        """Initialize the vector manager with a specified embedding model and persistence directory."""
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)

    def _save(self) -> None:
        """Persist the FAISS index and chunks metadata to disk."""
        faiss.write_index(self.index, os.path.join(self.persist_dir, "index.faiss"))
        # Save chunks metadata
        with open(os.path.join(self.persist_dir, "chunks.pkl"), "wb") as f:
            pickle.dump(self.chunks, f)

    def _load(self) -> bool:
        """Load the FAISS index and chunks metadata from disk."""
        index_path = os.path.join(self.persist_dir, "index.faiss")
        chunks_path = os.path.join(self.persist_dir, "chunks.pkl")

        if os.path.exists(index_path) and os.path.exists(chunks_path):
            self.index = faiss.read_index(index_path)
            with open(chunks_path, "rb") as f:
                self.chunks = pickle.load(f)
            return True
        return False

    def _chunk_document(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split document text into overlapping chunks to keep context."""
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks
    
    def add_documents(self, pdf_documents: List[Dict[str, str]]) -> None:
        """Add documents to the vector store, creating embeddings and building the FAISS index."""
        if self._load():
            print("Loaded existing vector store.")
            return
        
        doc_chunks = [] # keep filename with chunk
        embeddings_chunks = [] # chunks to be embedded

        for doc in pdf_documents:
            chunks = self._chunk_document(doc["text"])
            for chunk in chunks:
                doc_chunks.append({"filename": doc["filename"], "content": chunk})
                embeddings_chunks.append(chunk)
        self.chunks = doc_chunks

        # create embeddings and build index
        embeddings = self.model.encode(embeddings_chunks, convert_to_numpy=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

        self._save()  # save to disk for later use
        print("Vector store built and saved.")

    def search(self, query: str, k: int = 3) -> List[Dict[str, str]]:
        """Search the vector store for the top-k most similar document chunks to the query."""
        # encode query to vector to find similar vectors from documents
        query_vec = self.model.encode([query], convert_to_numpy=True)
        scores, idx = self.index.search(query_vec, k)

        results = []
        for i in idx[0]:
            results.append({
                "filename": self.chunks[i]["filename"],
                "content": self.chunks[i]["content"],
            })
        return results
