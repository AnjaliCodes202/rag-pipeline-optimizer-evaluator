#this files knows how to read files, nothing else
from pathlib import Path
from pypdf import PdfReader
import docx

def parse_text(file_path:Path):
    with open(file_path, "r", encoding="utf-8") as f:
         return f.read()


def parse_pdf(file_path: Path):
    text=""
    with open(file_path,'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text+=page.extract_text() or ""
        return text

def parse_docx(file_path:Path):
    doc = docx.Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)

def parse_file(file_path:Path, content_type:str):
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return parse_pdf(file_path)
    if suffix == ".docx":
        return parse_docx(file_path)
    if suffix == ".txt":
        return parse_text(file_path)

    raise ValueError("Unsupported File type")