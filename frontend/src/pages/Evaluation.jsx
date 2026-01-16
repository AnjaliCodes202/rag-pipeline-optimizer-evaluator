// 1️⃣ PURPOSE (system terms)
// This page is the dashboard container.
// It:
// arranges all evaluation-related panels
// defines visual flow, not data flow
// acts as the single screen where experiments happen
// It does not:
// hold state
// call APIs
// compute anything

import React from "react";

import QueryInput from "../components/evaluation/QueryInput";
import EvaluationRunner from "../components/evaluation/EvaluationRunner";
import AnswerComparison from "../components/evaluation/AnswerComparison";
import RetrievedChunksView from "../components/explainability/RetrievedChunksView";
import DocumentUpload from "../components/documents/DocumentUpload";
import PipelineBuilder from "../components/pipelines/PipelineBuilder";

export default function Evaluation(){
    return(
        <div className="page evaluation-page">
            <h2 className="page-title">RAG Evaluation Dashboard</h2>
            
            <section className="evaluation-section glass-card input-section">
                <DocumentUpload/>
                <QueryInput/>
            </section>
            <section className="evaluation-section glass-card pipeline-section">
                <PipelineBuilder/>
            </section>
            <section className="evaluation-section glass-card action-section">
                <EvaluationRunner/>
            </section>
            <section className="evaluation-section result-section">
                <AnswerComparison/>
            </section>
            <section className="evaluation-section glass-card explainability-section">
              <details>
                <summary>Explainability & Retrieved Chunks</summary>
                <RetrievedChunksView/>
              </details>
            </section>
        </div>
    );
};
