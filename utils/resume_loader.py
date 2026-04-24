import os
from pathlib import Path
from typing import Dict, List

from docx import Document
from pypdf import PdfReader


def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def load_resumes(folder: str = "resumes") -> List[Dict[str, str]]:
    """Load resume files from the resume folder."""
    resume_dir = Path(folder)
    resume_dir.mkdir(exist_ok=True)

    resumes = []
    for file_path in sorted(resume_dir.iterdir()):
        if not file_path.is_file() or file_path.name == ".gitkeep":
            continue

        suffix = file_path.suffix.lower()
        try:
            if suffix == ".pdf":
                text = read_pdf(str(file_path))
            elif suffix == ".docx":
                text = read_docx(str(file_path))
            elif suffix == ".txt":
                text = read_txt(str(file_path))
            else:
                continue
        except Exception as exc:
            text = f"Unable to parse resume: {exc}"

        resumes.append({
            "file_name": file_path.name,
            "path": str(file_path),
            "text": text,
        })

    return resumes
