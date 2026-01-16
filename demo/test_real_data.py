"""
실제 데이터로 차트 생성 및 테스트
"""
import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def load_real_data():
    """실제 데이터 로드 (보강된 버전 우선)"""
    enriched_path = Path('real_user_profile_enriched.json')
    real_path = Path('real_user_profile.json')
    
    if enriched_path.exists():
        print("보강된 데이터 사용: real_user_profile_enriched.json")
        with open(enriched_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif real_path.exists():
        print("실제 데이터 사용: real_user_profile.json")
        with open(real_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        raise FileNotFoundError("데이터 파일을 찾을 수 없습니다.")

def test_data_quality(data):
    """데이터 품질 검사"""
    print("=" * 60)
    print("실제 데이터 품질 검사")
    print("=" * 60)
    
    sessions = data['sessions']
    print(f"\n총 세션 수: {len(sessions)}")
    
    # 각 세션의 데이터 완성도 확인
    has_weights = sum(1 for s in sessions if 'personality_weights' in s)
    has_confidence = sum(1 for s in sessions if s.get('confidence', 0) > 0)
    has_behavioral = sum(1 for s in sessions if s['behavioral_profile'].get('avgDecisionLatency', 0) > 0)
    
    print(f"\n데이터 유형별 통계:")
    print(f"  - 성격 가중치: {has_weights}개 세션")
    print(f"  - 신뢰도: {has_confidence}개 세션")
    print(f"  - 행동 프로필: {has_behavioral}개 세션")
    
    # 최소한 성격 가중치나 신뢰도가 있으면 진행
    return has_weights > 0 or has_confidence > 0

def plot_real_confidence(data):
    """실제 데이터로 신뢰도 그래프"""
    sessions = data['sessions']
    
    # 신뢰도가 있는 세션만 필터링
    valid_sessions = [s for s in sessions if s.get('confidence', 0) > 0]
    
    if len(valid_sessions) < 2:
        print("⚠️ 신뢰도 데이터가 부족합니다 (최소 2개 세션 필요)")
        return False
    
    session_nums = [s['session'] for s in valid_sessions]
    confidence = [s['confidence'] for s in valid_sessions]
    
    plt.figure(figsize=(10, 6))
    plt.plot(session_nums, confidence, marker='o', linewidth=2, markersize=10, color='#00f2ff', label='실제 데이터')
    plt.fill_between(session_nums, confidence, alpha=0.3, color='#00f2ff')
    plt.xlabel('세션 수', fontsize=12)
    plt.ylabel('신뢰도', fontsize=12)
    plt.title(f'실제 사용자 신뢰도 추이 ({data["user_id"]})', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout()
    plt.savefig('demo_real_confidence.png', dpi=300, bbox_inches='tight')
    print("✓ 실제 신뢰도 그래프 생성: demo_real_confidence.png")
    plt.close()
    return True

def plot_real_behavioral_trends(data):
    """실제 행동 트렌드"""
    sessions = data['sessions']
    
    session_nums = [s['session'] for s in sessions]
    latency = [s['behavioral_profile'].get('avgDecisionLatency', 0) / 1000 for s in sessions]  # 초
    efficiency = [s['behavioral_profile'].get('pathEfficiency', 0) * 100 for s in sessions]  # %
    revisions = [s['behavioral_profile'].get('revisionRate', 0) for s in sessions]
    
    # 0이 아닌 데이터만 필터링
    valid_indices = [i for i, l in enumerate(latency) if l > 0]
    
    if len(valid_indices) < 2:
        print("⚠️ 행동 데이터가 부족합니다")
        return False
    
    valid_sessions = [session_nums[i] for i in valid_indices]
    valid_latency = [latency[i] for i in valid_indices]
    valid_efficiency = [efficiency[i] for i in valid_indices]
    valid_revisions = [revisions[i] for i in valid_indices]
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    
    ax1.fill_between(valid_sessions, valid_latency, alpha=0.3, color='#ff6b6b')
    ax1.plot(valid_sessions, valid_latency, marker='o', linewidth=2, color='#ff6b6b')
    ax1.set_ylabel('의사결정 지연시간 (초)', fontsize=11)
    ax1.set_title(f'실제 행동 트렌드 분석 ({data["user_id"]})', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    ax2.fill_between(valid_sessions, valid_efficiency, alpha=0.3, color='#4ecdc4')
    ax2.plot(valid_sessions, valid_efficiency, marker='s', linewidth=2, color='#4ecdc4')
    ax2.set_ylabel('경로 효율성 (%)', fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    ax3.fill_between(valid_sessions, valid_revisions, alpha=0.3, color='#95e1d3')
    ax3.plot(valid_sessions, valid_revisions, marker='^', linewidth=2, color='#95e1d3')
    ax3.set_xlabel('세션 수', fontsize=12)
    ax3.set_ylabel('수정 빈도', fontsize=11)
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('demo_real_behavioral_trends.png', dpi=300, bbox_inches='tight')
    print("✓ 실제 행동 트렌드 차트 생성: demo_real_behavioral_trends.png")
    plt.close()
    return True

def plot_real_personality_evolution(data):
    """실제 성격 진화"""
    sessions = data['sessions']
    
    # 가중치가 있는 세션만 필터링
    valid_sessions = [s for s in sessions if 'personality_weights' in s]
    
    if len(valid_sessions) < 2:
        print("⚠️ 성격 가중치 데이터가 부족합니다")
        return False
    
    session_nums = [s['session'] for s in valid_sessions]
    logic = [s['personality_weights']['Logic'] for s in valid_sessions]
    intuition = [s['personality_weights']['Intuition'] for s in valid_sessions]
    fluidity = [s['personality_weights']['Fluidity'] for s in valid_sessions]
    complexity = [s['personality_weights']['Complexity'] for s in valid_sessions]
    
    plt.figure(figsize=(12, 7))
    plt.plot(session_nums, logic, marker='o', label='Logic', linewidth=2, color='#ff6b6b')
    plt.plot(session_nums, intuition, marker='s', label='Intuition', linewidth=2, color='#4ecdc4')
    plt.plot(session_nums, fluidity, marker='^', label='Fluidity', linewidth=2, color='#95e1d3')
    plt.plot(session_nums, complexity, marker='d', label='Complexity', linewidth=2, color='#f38181')
    
    plt.xlabel('세션 수', fontsize=12)
    plt.ylabel('가중치', fontsize=12)
    plt.title(f'실제 성격 가중치 진화 ({data["user_id"]})', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig('demo_real_personality_evolution.png', dpi=300, bbox_inches='tight')
    print("✓ 실제 성격 진화 그래프 생성: demo_real_personality_evolution.png")
    plt.close()
    return True

def generate_real_data_summary(data):
    """실제 데이터 요약 리포트"""
    sessions = data['sessions']
    valid_sessions = [s for s in sessions if s.get('confidence', 0) > 0]
    
    if not valid_sessions:
        print("⚠️ 요약 리포트를 생성할 수 없습니다 (데이터 부족)")
        return
    
    latest = valid_sessions[-1]
    
    summary = f"""# 실제 사용자 데이터 요약 리포트

## 사용자 정보
- **사용자 ID**: {data['user_id']}
- **총 세션 수**: {len(sessions)}
- **유효 세션 수**: {len(valid_sessions)}

## 최신 세션 데이터
- **세션 번호**: {latest['session']}
- **신뢰도**: {latest.get('confidence', 0):.0%}
- **성숙도 레벨**: {latest.get('maturity_level', 1)}

## 행동 프로필
- **의사결정 지연시간**: {latest['behavioral_profile'].get('avgDecisionLatency', 0):.0f}ms
- **경로 효율성**: {latest['behavioral_profile'].get('pathEfficiency', 0):.2f}
- **수정 빈도**: {latest['behavioral_profile'].get('revisionRate', 0)}

## 성격 가중치
"""
    
    if 'personality_weights' in latest:
        pw = latest['personality_weights']
        summary += f"""- **Logic**: {pw.get('Logic', 0):.2f} ({pw.get('Logic', 0)*100:.0f}%)
- **Intuition**: {pw.get('Intuition', 0):.2f} ({pw.get('Intuition', 0)*100:.0f}%)
- **Fluidity**: {pw.get('Fluidity', 0):.2f} ({pw.get('Fluidity', 0)*100:.0f}%)
- **Complexity**: {pw.get('Complexity', 0):.2f} ({pw.get('Complexity', 0)*100:.0f}%)
"""
    else:
        summary += "- 성격 가중치 데이터 없음\n"
    
    summary += f"""
## 데이터 품질
- **완전한 세션**: {len(valid_sessions)}개
- **불완전한 세션**: {len(sessions) - len(valid_sessions)}개
- **데이터 완성도**: {len(valid_sessions)/len(sessions)*100:.0f}%

## 주의사항
이 데이터는 실제 시스템에서 수집된 데이터입니다. 
일부 세션은 데이터가 불완전할 수 있습니다.
"""
    
    with open('demo_real_summary.md', 'w', encoding='utf-8') as f:
        f.write(summary)
    print("✓ 실제 데이터 요약 리포트 생성: demo_real_summary.md")

if __name__ == '__main__':
    print("=" * 60)
    print("실제 데이터 테스트 시작")
    print("=" * 60)
    
    # 데이터 로드
    try:
        data = load_real_data()
    except FileNotFoundError:
        print("❌ real_user_profile.json 파일을 찾을 수 없습니다.")
        print("   먼저 demo/extract_real_data.py를 실행하세요.")
        exit(1)
    
    # 데이터 품질 검사
    if not test_data_quality(data):
        print("\n⚠️ 데이터가 충분하지 않아 차트를 생성할 수 없습니다.")
        exit(1)
    
    # 차트 생성
    print("\n" + "=" * 60)
    print("차트 생성 중...")
    print("=" * 60)
    
    success_count = 0
    
    if plot_real_confidence(data):
        success_count += 1
    
    if plot_real_behavioral_trends(data):
        success_count += 1
    
    if plot_real_personality_evolution(data):
        success_count += 1
    
    generate_real_data_summary(data)
    
    print("\n" + "=" * 60)
    print(f"테스트 완료! {success_count}개 차트 생성됨")
    print("=" * 60)
