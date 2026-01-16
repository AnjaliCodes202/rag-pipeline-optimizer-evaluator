from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

EMBEDDING_MODEL_MAP = {
    "minilm": "sentence-transformers/all-MiniLM-L6-v2",
    "mpnet": "sentence-transformers/all-mpnet-base-v2",
    "bge": "BAAI/bge-base-en",
}

class EmbeddingClient:
    """
    Embedding client bound to a specific model.
    """
    def __init__(self,embedding_model:str):
        if embedding_model not in EMBEDDING_MODEL_MAP:
            raise ValueError(f"Unsupported embedding model: {embedding_model}")
        model_name = EMBEDDING_MODEL_MAP[embedding_model]
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]):
        """
        Embedding client bound to a specific model.
        """
        if not texts:
            return []
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.tolist()



def get_embedding_client(embedding_model: str) -> EmbeddingClient:
    """
    Factory function used by executor.
    """
    return EmbeddingClient(embedding_model)


def generate_embeddings(
    texts: List[str],
    embedding_client: EmbeddingClient,
) -> List[List[float]]:
    """
    Thin wrapper used by executor.
    """
    return embedding_client.embed(texts)

