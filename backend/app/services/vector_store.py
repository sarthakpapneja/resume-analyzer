import faiss
import numpy as np
import pickle
import os

class VectorStore:
    def __init__(self, dimension: int = 384, index_path: str = "faiss_index.bin"):
        self.dimension = dimension
        self.index_path = index_path
        self.index = faiss.IndexFlatIP(dimension)  # Inner Product (Cosine Sim if normalized)
        self.metadata = {}  # Map ID to metadata
        self.id_counter = 0

    def add_vector(self, vector: np.ndarray, meta: dict) -> int:
        """Add a vector to the index."""
        if vector.shape[0] != self.dimension:
            raise ValueError(f"Vector dimension mismatch: {vector.shape[0]} vs {self.dimension}")
        
        # FAISS expects float32
        vector = vector.astype('float32').reshape(1, -1)
        faiss.normalize_L2(vector)  # Normalize for Cosine Similarity via IP
        
        self.index.add(vector)
        doc_id = self.id_counter
        self.metadata[doc_id] = meta
        self.id_counter += 1
        return doc_id

    def search(self, vector: np.ndarray, k: int = 5):
        """Search for compliant vectors."""
        vector = vector.astype('float32').reshape(1, -1)
        faiss.normalize_L2(vector)
        
        distances, indices = self.index.search(vector, k)
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx in self.metadata:
                results.append({
                    "id": int(idx),
                    "score": float(distances[0][i]),
                    "metadata": self.metadata[idx]
                })
        return results

    def save(self):
        """Save index and metadata to disk."""
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + ".meta", "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        """Load index and metadata from disk."""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.index_path + ".meta", "rb") as f:
                self.metadata = pickle.load(f)
