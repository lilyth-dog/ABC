
from xhtml2pdf import pisa
import os

def convert_html_to_pdf(html_path, pdf_path):
    with open(html_path, "r", encoding="utf-8") as html_file:
        source_html = html_file.read()
        
    with open(pdf_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(source_html, dest=pdf_file)
        
    if pisa_status.err:
        print(f"Error occurred during PDF conversion")
    else:
        print(f"PDF successfully generated: {pdf_path}")

if __name__ == "__main__":
    convert_html_to_pdf("docs/preview.html", "docs/ABC해커톤_논문_제출용_preview.pdf")
