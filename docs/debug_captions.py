
from docx import Document

def debug_docx(path):
    doc = Document(path)
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if not text: continue
        # Detect headers (starting with number) or captions
        if text[0].isdigit() or "(" in text or "<" in text or "그림" in text or "표" in text:
            print(f"L{i}: [{p.style.name}] {text}")

if __name__ == "__main__":
    debug_docx("docs/ABC해커톤_논문_제출용.docx")
