# Given a user query, find the most relevant chunks using vector similarity.
from typing import List,Tuple
import numpy as np
import math

def cosine_similarity(vec1: List[float], vec2: List[float]):
    dot_product = sum(a*b for a,b in zip(vec1,vec2))
    norm_vec1 = math.sqrt(sum(a*a for a in vec1))
    norm_vec2 = math.sqrt(sum(b*b for b in vec2))
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return dot_product/(norm_vec2*norm_vec1)

def retrieve_top_k(query_embedding:List[float], chunk_embeddings: List[List[float]], chunks: List[str], top_k:int):
    scores = []
    if not chunk_embeddings or not chunks:
        return []
    for chunk_text, chunk_vector in zip(chunks,chunk_embeddings):
        score = cosine_similarity(query_embedding,chunk_vector)
        scores.append((chunk_text,score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]
