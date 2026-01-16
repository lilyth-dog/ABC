"""
생성된 이미지 파일 검증 및 미리보기 정보 출력
"""
from PIL import Image
import os
from pathlib import Path

def verify_image(image_path):
    """이미지 파일 검증"""
    if not os.path.exists(image_path):
        return None
    
    try:
        img = Image.open(image_path)
        size_kb = os.path.getsize(image_path) // 1024
        return {
            'exists': True,
            'width': img.size[0],
            'height': img.size[1],
            'format': img.format,
            'mode': img.mode,
            'size_kb': size_kb,
            'dpi': img.info.get('dpi', (300, 300))[0] if 'dpi' in img.info else None
        }
    except Exception as e:
        return {'exists': True, 'error': str(e)}

def check_all_images():
    """모든 이미지 파일 확인"""
    demo_dir = Path(__file__).parent
    
    images = {
        '샘플 데이터 차트': [
            'demo_confidence_growth.png',
            'demo_personality_evolution.png',
            'demo_radar_prediction.png',
            'demo_behavioral_trends.png'
        ],
        '실제 데이터 차트': [
            'demo_real_confidence.png',
            'demo_real_personality_evolution.png',
            'demo_real_behavioral_trends.png'
        ]
    }
    
    print("=" * 60)
    print("이미지 파일 검증 결과")
    print("=" * 60)
    
    all_good = True
    
    for category, files in images.items():
        print(f"\n[{category}]")
        for filename in files:
            filepath = demo_dir / filename
            info = verify_image(filepath)
            
            if info is None:
                print(f"  ❌ {filename}: 파일 없음")
                all_good = False
            elif 'error' in info:
                print(f"  ❌ {filename}: 오류 - {info['error']}")
                all_good = False
            else:
                status = "✓" if info['width'] > 0 and info['height'] > 0 else "⚠️"
                print(f"  {status} {filename}")
                print(f"      크기: {info['width']}x{info['height']}px")
                print(f"      파일 크기: {info['size_kb']}KB")
                print(f"      포맷: {info['format']}")
                if info['dpi']:
                    print(f"      DPI: {info['dpi']}")
    
    print("\n" + "=" * 60)
    if all_good:
        print("✓ 모든 이미지 파일이 정상적으로 생성되었습니다!")
    else:
        print("⚠️ 일부 이미지 파일에 문제가 있습니다.")
    print("=" * 60)
    
    return all_good

if __name__ == '__main__':
    check_all_images()
