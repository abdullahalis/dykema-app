import os
from pypdf import PdfReader
from typing import List, Dict

def load_pdfs_from_folder(folder_path: str) -> List[Dict[str, str]]:
    """Load all PDF files from a specified folder and extract their text content."""
    docs = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            reader = PdfReader(os.path.join(folder_path, file))
            all_text =[]
            for page in reader.pages:
                all_text.append(page.extract_text())
            docs.append({"filename": file, "text": "".join(all_text)})
    return docs