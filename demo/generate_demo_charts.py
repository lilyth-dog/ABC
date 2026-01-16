"""
시연용 차트 생성 스크립트
세션별 신뢰도, 성격 가중치 변화, 예측 결과를 시각화
"""
import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def load_sample_data():
    """샘플 데이터 로드"""
    with open('sample_user_profile.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def plot_confidence_growth(data):
    """세션별 신뢰도 증가 그래프"""
    sessions = [s['session'] for s in data['sessions']]
    confidence = [s['confidence'] for s in data['sessions']]
    
    plt.figure(figsize=(10, 6))
    plt.plot(sessions, confidence, marker='o', linewidth=2, markersize=10, color='#00f2ff')
    plt.fill_between(sessions, confidence, alpha=0.3, color='#00f2ff')
    plt.xlabel('세션 수', fontsize=12)
    plt.ylabel('신뢰도', fontsize=12)
    plt.title('세션별 신뢰도 증가 추이', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig('demo_confidence_growth.png', dpi=300, bbox_inches='tight')
    print("✓ 신뢰도 그래프 생성: demo_confidence_growth.png")
    plt.close()

def plot_personality_evolution(data):
    """성격 가중치 진화 그래프"""
    sessions = [s['session'] for s in data['sessions']]
    logic = [s['personality_weights']['Logic'] for s in data['sessions']]
    intuition = [s['personality_weights']['Intuition'] for s in data['sessions']]
    fluidity = [s['personality_weights']['Fluidity'] for s in data['sessions']]
    complexity = [s['personality_weights']['Complexity'] for s in data['sessions']]
    
    plt.figure(figsize=(12, 7))
    plt.plot(sessions, logic, marker='o', label='Logic', linewidth=2, color='#ff6b6b')
    plt.plot(sessions, intuition, marker='s', label='Intuition', linewidth=2, color='#4ecdc4')
    plt.plot(sessions, fluidity, marker='^', label='Fluidity', linewidth=2, color='#95e1d3')
    plt.plot(sessions, complexity, marker='d', label='Complexity', linewidth=2, color='#f38181')
    
    plt.xlabel('세션 수', fontsize=12)
    plt.ylabel('가중치', fontsize=12)
    plt.title('성격 가중치 진화 (세션별 변화)', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig('demo_personality_evolution.png', dpi=300, bbox_inches='tight')
    print("✓ 성격 진화 그래프 생성: demo_personality_evolution.png")
    plt.close()

def plot_radar_comparison(data):
    """현재 vs 30일 후 예측 레이더 차트"""
    current = data['sessions'][-1]['personality_weights']
    predicted = data['predictions']['30days']
    
    categories = ['Logic', 'Intuition', 'Fluidity', 'Complexity']
    current_values = [current['Logic'], current['Intuition'], current['Fluidity'], current['Complexity']]
    predicted_values = [predicted['Logic'], predicted['Intuition'], predicted['Fluidity'], predicted['Complexity']]
    
    # 레이더 차트를 위한 각도 계산
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # 닫기
    
    current_values += current_values[:1]
    predicted_values += predicted_values[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    ax.plot(angles, current_values, 'o-', linewidth=2, label='현재', color='#00f2ff')
    ax.fill(angles, current_values, alpha=0.25, color='#00f2ff')
    
    ax.plot(angles, predicted_values, 's-', linewidth=2, label='30일 후 예측', color='#ff6b6b')
    ax.fill(angles, predicted_values, alpha=0.25, color='#ff6b6b')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=10)
    ax.grid(True)
    
    plt.title('30일 후 성격 진화 예측', fontsize=14, fontweight='bold', pad=20)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.savefig('demo_radar_prediction.png', dpi=300, bbox_inches='tight')
    print("✓ 레이더 차트 생성: demo_radar_prediction.png")
    plt.close()

def plot_behavioral_trends(data):
    """행동 트렌드 영역 차트"""
    sessions = [s['session'] for s in data['sessions']]
    latency = [s['behavioral_profile']['avgDecisionLatency'] / 1000 for s in data['sessions']]  # 초 단위
    efficiency = [s['behavioral_profile']['pathEfficiency'] * 100 for s in data['sessions']]  # 퍼센트
    revisions = [s['behavioral_profile']['revisionRate'] for s in data['sessions']]
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    
    # 의사결정 지연시간
    ax1.fill_between(sessions, latency, alpha=0.3, color='#ff6b6b')
    ax1.plot(sessions, latency, marker='o', linewidth=2, color='#ff6b6b')
    ax1.set_ylabel('의사결정 지연시간 (초)', fontsize=11)
    ax1.set_title('행동 트렌드 분석', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 경로 효율성
    ax2.fill_between(sessions, efficiency, alpha=0.3, color='#4ecdc4')
    ax2.plot(sessions, efficiency, marker='s', linewidth=2, color='#4ecdc4')
    ax2.set_ylabel('경로 효율성 (%)', fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # 수정 빈도
    ax3.fill_between(sessions, revisions, alpha=0.3, color='#95e1d3')
    ax3.plot(sessions, revisions, marker='^', linewidth=2, color='#95e1d3')
    ax3.set_xlabel('세션 수', fontsize=12)
    ax3.set_ylabel('수정 빈도', fontsize=11)
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('demo_behavioral_trends.png', dpi=300, bbox_inches='tight')
    print("✓ 행동 트렌드 차트 생성: demo_behavioral_trends.png")
    plt.close()

def generate_summary_report(data):
    """시연용 요약 리포트 생성"""
    latest = data['sessions'][-1]
    summary = f"""
# 행동 기반 디지털 휴먼 트윈 - 시연 결과 요약

## 사용자 프로필
- **사용자 ID**: {data['user_id']}
- **총 세션 수**: {len(data['sessions'])}
- **현재 신뢰도**: {latest['confidence']:.0%}
- **성숙도 레벨**: {latest['maturity_level']}

## 현재 성격 가중치
- **Logic**: {latest['personality_weights']['Logic']:.2f} ({latest['personality_weights']['Logic']*100:.0f}%)
- **Intuition**: {latest['personality_weights']['Intuition']:.2f} ({latest['personality_weights']['Intuition']*100:.0f}%)
- **Fluidity**: {latest['personality_weights']['Fluidity']:.2f} ({latest['personality_weights']['Fluidity']*100:.0f}%)
- **Complexity**: {latest['personality_weights']['Complexity']:.2f} ({latest['personality_weights']['Complexity']*100:.0f}%)

## 30일 후 예측
- **Logic**: {data['predictions']['30days']['Logic']:.2f} ({data['predictions']['trend']['Logic']})
- **Intuition**: {data['predictions']['30days']['Intuition']:.2f} ({data['predictions']['trend']['Intuition']})
- **Fluidity**: {data['predictions']['30days']['Fluidity']:.2f} ({data['predictions']['trend']['Fluidity']})
- **Complexity**: {data['predictions']['30days']['Complexity']:.2f} ({data['predictions']['trend']['Complexity']})

## 스트레스 분석
- **레벨**: {data['stress_analysis']['level']:.1f} ({data['stress_analysis']['category']})
- **권장사항**: {data['stress_analysis']['recommendation']}

## 진화 요약
- **신뢰도 성장**: {data['evolution_summary']['confidence_growth']}
- **주요 특성**: {data['evolution_summary']['primary_trait']}
- **안정성**: {data['evolution_summary']['stability']}
"""
    
    with open('demo_summary_report.md', 'w', encoding='utf-8') as f:
        f.write(summary)
    print("✓ 요약 리포트 생성: demo_summary_report.md")

if __name__ == '__main__':
    print("=" * 60)
    print("시연용 차트 생성 시작")
    print("=" * 60)
    
    # 데이터 로드
    data = load_sample_data()
    
    # 차트 생성
    plot_confidence_growth(data)
    plot_personality_evolution(data)
    plot_radar_comparison(data)
    plot_behavioral_trends(data)
    generate_summary_report(data)
    
    print("=" * 60)
    print("모든 차트 생성 완료!")
    print("=" * 60)
