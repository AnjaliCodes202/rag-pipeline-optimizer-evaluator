from pathlib import Path
from utils.file_parser import parse_file
from utils.text_processing import clean_text

def ingest_document(file_path:Path, content_type:str):
    raw_text = parse_file(file_path,content_type)
    cleaned_text = clean_text(raw_text)
    return cleaned_text