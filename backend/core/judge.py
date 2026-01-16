# Evaluate answer quality using a judge model on three axes:
# Relevance
# Faithfulness (groundedness)
# Completeness
# This enables automatic, repeatable evaluation.

from typing import Dict,List
import re
import json

from schemas.evaluation import (
    EvaluationResult,
    QualityScores,
    HallucinationAnalysis,
    RetrievalCoverage
)

class JudgeClient:
    def judge(self,question:str, answer:str, context:List[str]):
        raise NotImplementedError


class OpenAIJudgeClient(JudgeClient):
    def __init__(self):
        pass

    def judge(self, question: str, answer: str, context: List[str]) -> Dict:
        answer_lower = answer.lower()
        # context_text = "\n\n".join(context).lower()

        question_keywords = set(re.findall(r"\w+", question.lower()))
        relevance_hits = sum(1 for w in question_keywords if w in answer_lower)
        relevance = min(1.0, relevance_hits / max(len(question_keywords), 1))

        # ---------- Faithfulness ----------
        faithful = any(
            chunk.lower() in answer_lower
            for chunk in context
        )
        faithfulness = 1.0 if faithful else 0.3

        hallucinated = not faithful
          # ---------- Completeness ----------
        completeness = min(1.0, len(answer.split()) / 120)

        # ---------- Quality Scores ----------
        quality_scores = QualityScores(
            relevance=round(relevance, 3),
            faithfulness=round(faithfulness, 3),
            completeness=round(completeness, 3),
        )
     
        #  ---------- Hallucination ----------
        hallucination  = HallucinationAnalysis(
            hallucinated=hallucinated,
            confidence=round(1 - faithfulness, 3),
            cause="generation_failure" if hallucinated else None,
        )
   
        # ---------- Retrieval Coverage ----------
        coverage_hits = sum(1 for c in context if c.lower() in answer_lower)
        coverage_score = min(1.0, coverage_hits / max(len(context), 1))
        retrieval_coverage = RetrievalCoverage(
            coverage_score=round(coverage_score, 3),
            missing_sections=None
            if coverage_score > 0.5
            else "Low context usage",
        )
        


        return EvaluationResult(
            quality_scores=quality_scores,
            hallucination=hallucination,
            retrieval_coverage=retrieval_coverage,
            judge_reasoning=(
                "Scores computed using lexical overlap and "
                "context grounding heuristics."
            ),
        )


def evaluate_answer(question:str, answer:str, retrieved_chunks:List[str],judge_client:JudgeClient):
    scores = judge_client.judge(question=question,answer=answer,context=retrieved_chunks)
    return scores

