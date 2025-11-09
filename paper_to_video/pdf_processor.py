import PyPDF2
from pathlib import Path

def extract_text(pdf_path: Path) -> str:
    """Extract all text from PDF"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def chunk_by_sections(text: str) -> list[str]:
    """Split text into major sections"""
    sections = []
    current_section = ""
    
    lines = text.split('\n')
    for line in lines:
        # Detect section headers (customize based on paper format)
        if any(keyword in line.upper() for keyword in 
               ['ABSTRACT', 'INTRODUCTION', 'METHOD', 'RESULTS', 'DISCUSSION', 'CONCLUSION']):
            if current_section:
                sections.append(current_section)
            current_section = line + "\n"
        else:
            current_section += line + "\n"
    
    if current_section:
        sections.append(current_section)
    
    return sections