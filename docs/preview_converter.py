
import mammoth
import os

def convert_to_html(docx_path, html_path):
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value
        
        # Wrap in basic HTML structure with CSS
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>논문 미리보기 - ABC 해커톤</title>
            <style>
                body {{
                    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
                    line-height: 1.6;
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 40px;
                    background-color: #f5f5f5;
                }}
                .paper-container {{
                    background: white;
                    padding: 60px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    border-radius: 8px;
                }}
                h1 {{ text-align: center; color: #333; }}
                h2 {{ border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 30px; color: #2c3e50; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
                th {{ background-color: #f8f9fa; font-weight: bold; }}
                .caption {{ text-align: center; font-style: italic; color: #666; margin: 10px 0; }}
                .abstract {{ background: #fdfdfd; border: 1px solid #eee; padding: 20px; font-size: 0.95em; }}
                img {{ max-width: 100%; height: auto; display: block; margin: 20px auto; }}
            </style>
        </head>
        <body>
            <div class="paper-container">
                {html}
            </div>
        </body>
        </html>
        """
        
        with open(html_path, "w", encoding="utf-8") as html_file:
            html_file.write(full_html)
    
    print(f"HTML preview generated: {html_path}")

if __name__ == "__main__":
    convert_to_html("docs/ABC해커톤_논문_제출용.docx", "docs/preview.html")
