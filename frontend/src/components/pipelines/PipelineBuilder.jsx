import React, { useEffect, useState } from "react";
import { useExperimentStore } from "../../store/experimentStore";

export default function PipelineBuilder() {
  const setPipelines = useExperimentStore((s) => s.setPipelines);
  const pipelines = useExperimentStore((s) => s.pipelines);
  // local UI state (single pipeline)
  const [config, setConfig] = useState({
    chunking_strategy: "fixed",
    chunk_size: 512,
    chunk_overlap: 50,
    top_k: 5,
    temperature: 0.2,
    embedding_model: "minilm",
    generator_model: "distilgpt2",
    reranker: false,
  });

  // whenever config changes, update Zustand with ONE pipeline
  // useEffect(() => {
  //   setPipelines([
  //     {
  //       pipeline_id: "pipeline_1",
  //       pipeline_config: config,
  //     },
  //   ]);
  // }, [config, setPipelines]);

  const addPipeline = () => {
    const nextId = `pipeline_${pipelines.length + 1}`;
    setPipelines([
      ...pipelines,
      {
        pipeline_id: nextId,
        pipeline_config: { ...config },
      },
    ]);
  };

  const removePipeline = (pipeline_id) => {
    const updated = pipelines.filter((p) => p.pipeline_id !== pipeline_id);
    setPipelines(updated);
  };

  const update = (key, value) => {
    setConfig((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div className="pipeline-builder">
      <h3>Pipeline Configuration</h3>

      <label>
        Chunk Size
        <input
          type="number"
          value={config.chunk_size}
          onChange={(e) => update("chunk_size", Number(e.target.value))}
        />
      </label>

      <label>
        Chunk Overlap
        <input
          type="number"
          value={config.chunk_overlap}
          onChange={(e) => update("chunk_overlap", Number(e.target.value))}
        />
      </label>

      <label>
        Top-K
        <input
          type="number"
          value={config.top_k}
          onChange={(e) => update("top_k", Number(e.target.value))}
        />
      </label>

      <label>
        Temperature
        <input
          type="number"
          step="0.1"
          value={config.temperature}
          onChange={(e) => update("temperature", Number(e.target.value))}
        />
      </label>

      <label>
        Embedding Model
        <select
          value={config.embedding_model}
          onChange={(e) => update("embedding_model", e.target.value)}
        >
          <option value="minilm">MiniLM</option>
          <option value="mpnet">MPNet</option>
          <option value="bge">BGE</option>
        </select>
      </label>

      <label>
        Generator Model
        <select
          value={config.generator_model}
          onChange={(e) => update("generator_model", e.target.value)}
        >
          <option value="distilgpt2">distilgpt2</option>
          <option value="facebook/opt-125m">facebook/opt-125m</option>
          <option value="facebook/opt-350m">facebook/opt-350m</option>
          <option value="TinyLlama/TinyLlama-1.1B-Chat-v1.0">
            TinyLlama 1.1B
          </option>
        </select>
      </label>

      <label>
        <input
          type="checkbox"
          checked={config.reranker}
          onChange={(e) => update("reranker", e.target.checked)}
        />
        Enable Reranker
      </label>
      <button onClick={addPipeline}>Add Pipeline</button>

      {/* PIPELINE LIST WITH DELETE */}
      {pipelines.length > 0 && (
        <div className="pipeline-list">
          <h4>Added Pipelines</h4>
          <ul>
            {pipelines.map((p) => (
              <li key={p.pipeline_id}>
                {p.pipeline_id} — chunk={p.pipeline_config.chunk_size}, top_k=
                {p.pipeline_config.top_k}, embed=
                {p.pipeline_config.embedding_model}
                <button
                  style={{ marginLeft: "10px" }}
                  onClick={() => removePipeline(p.pipeline_id)}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
