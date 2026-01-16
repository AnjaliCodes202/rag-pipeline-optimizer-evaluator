#Improve retrieval quality by re-evaluating relevance using a query–chunk pair scoring mechanism.
from typing import List,Tuple

class Reranker:
    def score(self, query: str, chunk: str):
        raise NotImplementedError


class DummyCrossEncoderReranker(Reranker):
    def score(self, query:str, chunk:str):
        query_terms = set(query.lower().split())
        chunk_terms = set(chunk.lower().split())
        return float(len(query_terms & chunk_terms))


def rerank_chunks(query:str, retrieved_chunks: List[Tuple[str,float]], reranker: Reranker):
    reranked = []
    for chunk_text,score in retrieved_chunks:
        new_score = reranker.score(query,chunk_text)
        reranked.append((chunk_text,new_score))
    reranked.sort(key=lambda x:x[1],reverse=True)
    return reranked


