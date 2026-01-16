#Estimate token usage and monetary cost per pipeline run.
#backend/app/services/cost_tracker.py

from typing import Dict,List

TOKEN_COST_PER_1K = {
    "embedding": 0.0001,
    "generation": 0.002
}

def estimate_tokens(text:str):
    return max(1,len(text)//4)

def calculate_cost(embedding_text:List[str], generated_text:str):
    embedding_tokens = sum(estimate_tokens(t) for t in embedding_text)
    generated_tokens = estimate_tokens(generated_text)

    embedding_cost = (embedding_tokens/1000)*TOKEN_COST_PER_1K['embedding']
    generation_cost = (generated_tokens/1000)*TOKEN_COST_PER_1K['generation']

    total_cost = embedding_cost+generation_cost

    return {
        "embedding_tokens": embedding_tokens,
        "generation_tokens": generation_cost,
        "embedding_cost": embedding_cost,
        "generation_cost": generation_cost,
        "total_cost": total_cost
    }