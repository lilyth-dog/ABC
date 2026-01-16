
from docx import Document
import sys

def list_styles(path):
    doc = Document(path)
    print(f"Styles in {path}:")
    for s in doc.styles:
        if s.type == 1: # Paragraph styles
            print(f" {s.name}")

if __name__ == "__main__":
    list_styles(sys.argv[1])
