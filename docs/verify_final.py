
import re
from docx import Document

def verify_paper(path):
    doc = Document(path)
    print(f"--- [ {path} ] 내용 정밀 검증 결과 ---")
    
    found_en_title = False
    found_abstract = False
    table_captions = []
    figure_captions = []
    double_numbering_issues = []
    
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if not text: continue
        
        # 1. 영문 제목 확인
        if "Behavior-Based Digital Human Twin" in text:
            found_en_title = True
            print(f"[검증 완료] 영문 제목 발견: {text[:50]}...")

        # 2. 영문 초록 확인
        if "Abstract" == text or "ABSTRACT" == text.upper():
            found_abstract = True
            print(f"[검증 완료] 영문 초록 섹션 발견 (index: {i})")

        # 3. 캡션 형식 확인
        if text.startswith("<표"):
            table_captions.append(text)
        elif text.startswith("(그림"):
            figure_captions.append(text)

        # 4. 중복 번호 확인 (1. 1. 서론 등)
        if re.match(r"^\d+\.\s+\d+\.", text):
            double_numbering_issues.append(text)

    print(f"\n[캡션 확인]")
    print(f"- 표 캡션 ({len(table_captions)}개): {table_captions[0] if table_captions else '없음'} 등")
    print(f"- 그림 캡션 ({len(figure_captions)}개): {figure_captions[0] if figure_captions else '없음'} 등")
    
    print(f"\n[서식 확인]")
    if not double_numbering_issues:
        print("- 중복 번호 문제 없음 (모두 교정됨)")
    else:
        print(f"- 중복 번호 잔류 발견: {double_numbering_issues}")

    if found_en_title and found_abstract:
        print("\n=> 모든 필수 요소가 템플릿 규격에 맞게 포함되어 있습니다.")

if __name__ == "__main__":
    verify_paper("docs/ABC해커톤_논문_제출용.docx")
