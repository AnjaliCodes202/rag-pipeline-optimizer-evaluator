from typing import List

# Fixed-size chunking (no overlap) => Character-based chunking
def fixed_size_chunking(text:str, chunk_size:int):
    chunks = []
    start = 0
    text_length = len(text)
    while start<text_length:
        end = start+chunk_size
        chunks.append(text[start:end])
        start = end
    return chunks

#Fixed-size chunking WITH overlap =>Preserve context between adjacent chunks.
def overlap_chunking(text:str, chunk_size:int, overlap:int):
    if overlap>=chunk_size:
        raise ValueError("overlap must be smaller than chunk size")
    chunks = []
    start = 0
    text_length = len(text)

    while start<text_length:
        end = start+chunk_size
        chunks.append(text[start:end])
        start = end-overlap
    return chunks

#Sentence-based chunking =>Create chunks that respect sentence boundaries.
def sentence_chunking(text:str, max_chunk_size:int):
    sentences = text.split(".")
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def chunk_text_with_pipeline(text:str, pipeline_config:dict):
    strategy = pipeline_config.get("chunking_strategy","fixed")
    chunk_size = pipeline_config.get("chunk_size")
    overlap = pipeline_config.get("chunk_overlap",0)

    if strategy == "fixed":
        return fixed_size_chunking(text,chunk_size)
    if strategy == "overlap":
        return overlap_chunking(text, chunk_size, overlap)
    if strategy == "sentence":
        return sentence_chunking(text,max_chunk_size=chunk_size)
    raise ValueError(f"Unsupported chunking strategy: {strategy}")

