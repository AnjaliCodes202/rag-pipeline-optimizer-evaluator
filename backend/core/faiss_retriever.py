import faiss
import numpy as np

class FaissRetriever:
    def __init__(self, embedding_dim: int):
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.chunks = []

    def build_index(self, embeddings: np.ndarray, chunks: list[str]):
        """
        embeddings: shape (N, D)
        chunks: List[str]
        """
        self.index.add(embeddings.astype("float32"))
        self.chunks = chunks

    def search(self, query_embedding: np.ndarray, top_k: int):
        """
        query_embedding: shape (1, D)
        returns: List[str]
        """
        distances, indices = self.index.search(
            query_embedding.astype("float32"),
            top_k
        )

        return [self.chunks[i] for i in indices[0] if i < len(self.chunks)]

