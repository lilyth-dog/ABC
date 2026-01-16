#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
성격 특성 분석 결과 시각화 스크립트
사용자 프로필 데이터에서 성격 가중치, 행동 패턴, 개인 특성을 시각화
"""
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False

# 색상 팔레트
COLORS = {
    'logic': '#ff6b6b',
    'intuition': '#4ecdc4',
    'fluidity': '#95e1d3',
    'complexity': '#f38181',
    'primary': '#00f2ff',
    'secondary': '#ffd93d',
    'accent': '#6c5ce7'
}

def get_db_connection():
    """데이터베이스 연결"""
    db_path = Path(__file__).parent / 'user_profiles.db'
    if not db_path.exists():
        return None
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

def load_user_profiles_from_db() -> List[Dict[str, Any]]:
    """데이터베이스에서 사용자 프로필 데이터 로드"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        
        # 사용자 목록 조회
        cursor.execute("SELECT id, display_name, maturity_level, sync_score FROM users")
        users = cursor.fetchall()
        
        profiles = []
        for user in users:
            user_id = user['id']
            
            # 프로필 진화 데이터 조회
            cursor.execute("""
                SELECT timestamp, logic_weight, intuition_weight, 
                       fluidity_weight, complexity_weight, confidence_score, archetype
                FROM profile_evolution
                WHERE user_id = ?
                ORDER BY timestamp
            """, (user_id,))
            
            evolution = []
            for row in cursor.fetchall():
                evolution.append({
                    'timestamp': row['timestamp'],
                    'personality_weights': {
                        'Logic': row['logic_weight'] or 0.5,
                        'Intuition': row['intuition_weight'] or 0.5,
                        'Fluidity': row['fluidity_weight'] or 0.5,
                        'Complexity': row['complexity_weight'] or 0.5
                    },
                    'confidence': row['confidence_score'] or 0.0,
                    'archetype': row['archetype'] or 'Unknown'
                })
            
            # 행동 세션 데이터 조회
            cursor.execute("""
                SELECT session_timestamp, avg_decision_latency, revision_rate,
                       path_efficiency, total_interactions, raw_metrics
                FROM behavioral_sessions
                WHERE user_id = ?
                ORDER BY session_timestamp
            """, (user_id,))
            
            sessions = []
            for idx, row in enumerate(cursor.fetchall(), 1):
                raw_metrics = json.loads(row['raw_metrics']) if row['raw_metrics'] else {}
                sessions.append({
                    'session': idx,
                    'timestamp': row['session_timestamp'],
                    'behavioral_profile': {
                        'avgDecisionLatency': row['avg_decision_latency'] or 0,
                        'revisionRate': row['revision_rate'] or 0,
                        'pathEfficiency': row['path_efficiency'] or 0.5,
                        'totalInteractions': row['total_interactions'] or 0,
                        **raw_metrics
                    }
                })
            
            if evolution or sessions:
                profiles.append({
                    'user_id': user_id,
                    'name': user['display_name'] or user_id,
                    'maturity_level': user['maturity_level'] or 1,
                    'sync_score': user['sync_score'] or 0.0,
                    'evolution': evolution,
                    'sessions': sessions
                })
        
        return profiles
    
    except Exception as e:
        print(f"⚠️ 데이터베이스 로드 오류: {e}")
        return []
    finally:
        conn.close()

def load_sample_data() -> Optional[Dict[str, Any]]:
    """샘플 데이터 로드 (데이터베이스가 없을 경우)"""
    sample_path = Path(__file__).parent.parent / 'demo' / 'sample_user_profile.json'
    if sample_path.exists():
        with open(sample_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def plot_personality_radar(profile: Dict[str, Any], output_dir: Path):
    """성격 가중치 레이더 차트"""
    if not profile.get('evolution'):
        return False
    
    # 최신 성격 가중치
    latest = profile['evolution'][-1]
    weights = latest['personality_weights']
    
    # 레이더 차트 데이터
    categories = ['Logic', 'Intuition', 'Fluidity', 'Complexity']
    values = [weights.get(cat, 0.5) for cat in categories]
    
    # 각도 계산
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]  # 닫기 위해 첫 값 추가
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # 레이더 차트 그리기
    ax.plot(angles, values, 'o-', linewidth=2, color=COLORS['primary'], label='현재')
    ax.fill(angles, values, alpha=0.25, color=COLORS['primary'])
    
    # 축 설정
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # 제목
    ax.set_title(f'성격 특성 분석 - {profile["name"]}\n'
                 f'아키타입: {latest.get("archetype", "Unknown")} | '
                 f'신뢰도: {latest.get("confidence", 0):.1%}',
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    output_path = output_dir / f'personality_radar_{profile["user_id"]}.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 성격 레이더 차트 생성: {output_path.name}")
    plt.close()
    return True

def plot_personality_evolution(profile: Dict[str, Any], output_dir: Path):
    """성격 가중치 진화 라인 차트"""
    if len(profile.get('evolution', [])) < 2:
        return False
    
    evolution = profile['evolution']
    timestamps = [e['timestamp'] for e in evolution]
    session_nums = list(range(1, len(evolution) + 1))
    
    logic = [e['personality_weights']['Logic'] for e in evolution]
    intuition = [e['personality_weights']['Intuition'] for e in evolution]
    fluidity = [e['personality_weights']['Fluidity'] for e in evolution]
    complexity = [e['personality_weights']['Complexity'] for e in evolution]
    confidence = [e.get('confidence', 0) for e in evolution]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # 성격 가중치 진화
    ax1.plot(session_nums, logic, marker='o', label='Logic', 
            linewidth=2, color=COLORS['logic'], markersize=8)
    ax1.plot(session_nums, intuition, marker='s', label='Intuition',
            linewidth=2, color=COLORS['intuition'], markersize=8)
    ax1.plot(session_nums, fluidity, marker='^', label='Fluidity',
            linewidth=2, color=COLORS['fluidity'], markersize=8)
    ax1.plot(session_nums, complexity, marker='d', label='Complexity',
            linewidth=2, color=COLORS['complexity'], markersize=8)
    
    ax1.set_xlabel('세션', fontsize=12)
    ax1.set_ylabel('가중치', fontsize=12)
    ax1.set_title(f'성격 가중치 진화 - {profile["name"]}', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 1)
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # 신뢰도 변화
    ax2.plot(session_nums, confidence, marker='o', linewidth=2, 
            color=COLORS['primary'], markersize=8)
    ax2.fill_between(session_nums, confidence, alpha=0.3, color=COLORS['primary'])
    ax2.set_xlabel('세션', fontsize=12)
    ax2.set_ylabel('신뢰도', fontsize=12)
    ax2.set_title('신뢰도 변화', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = output_dir / f'personality_evolution_{profile["user_id"]}.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 성격 진화 차트 생성: {output_path.name}")
    plt.close()
    return True

def plot_behavioral_patterns(profile: Dict[str, Any], output_dir: Path):
    """행동 패턴 분석 차트"""
    if not profile.get('sessions'):
        return False
    
    sessions = profile['sessions']
    session_nums = [s['session'] for s in sessions]
    
    latency = [s['behavioral_profile'].get('avgDecisionLatency', 0) / 1000 for s in sessions]  # 초
    efficiency = [s['behavioral_profile'].get('pathEfficiency', 0) * 100 for s in sessions]  # %
    revisions = [s['behavioral_profile'].get('revisionRate', 0) for s in sessions]
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    
    # 의사결정 지연시간
    ax1.fill_between(session_nums, latency, alpha=0.3, color=COLORS['logic'])
    ax1.plot(session_nums, latency, marker='o', linewidth=2, color=COLORS['logic'])
    ax1.set_ylabel('의사결정 지연시간 (초)', fontsize=11)
    ax1.set_title(f'행동 패턴 분석 - {profile["name"]}', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 경로 효율성
    ax2.fill_between(session_nums, efficiency, alpha=0.3, color=COLORS['intuition'])
    ax2.plot(session_nums, efficiency, marker='s', linewidth=2, color=COLORS['intuition'])
    ax2.set_ylabel('경로 효율성 (%)', fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # 수정 빈도
    ax3.fill_between(session_nums, revisions, alpha=0.3, color=COLORS['fluidity'])
    ax3.plot(session_nums, revisions, marker='^', linewidth=2, color=COLORS['fluidity'])
    ax3.set_xlabel('세션', fontsize=12)
    ax3.set_ylabel('수정 빈도', fontsize=11)
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = output_dir / f'behavioral_patterns_{profile["user_id"]}.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 행동 패턴 차트 생성: {output_path.name}")
    plt.close()
    return True

def plot_personality_comparison(profiles: List[Dict[str, Any]], output_dir: Path):
    """여러 사용자 성격 비교 차트"""
    if len(profiles) < 2:
        return False
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    categories = ['Logic', 'Intuition', 'Fluidity', 'Complexity']
    x = np.arange(len(categories))
    width = 0.8 / len(profiles)
    
    # 각 사용자의 최신 성격 가중치
    for idx, profile in enumerate(profiles):
        if not profile.get('evolution'):
            continue
        
        latest = profile['evolution'][-1]
        weights = [latest['personality_weights'].get(cat, 0.5) for cat in categories]
        
        offset = (idx - len(profiles)/2 + 0.5) * width
        ax1.bar(x + offset, weights, width, label=profile['name'], alpha=0.8)
    
    ax1.set_xlabel('성격 특성', fontsize=12)
    ax1.set_ylabel('가중치', fontsize=12)
    ax1.set_title('사용자별 성격 특성 비교', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    ax1.set_ylim(0, 1)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 신뢰도 비교
    user_names = []
    confidences = []
    for profile in profiles:
        if profile.get('evolution'):
            latest = profile['evolution'][-1]
            user_names.append(profile['name'])
            confidences.append(latest.get('confidence', 0))
    
    if user_names:
        colors_list = [COLORS['primary'] if c > 0.7 else COLORS['secondary'] 
                      for c in confidences]
        bars = ax2.bar(user_names, confidences, color=colors_list, alpha=0.8)
        ax2.set_ylabel('신뢰도', fontsize=12)
        ax2.set_title('사용자별 신뢰도 비교', fontsize=14, fontweight='bold')
        ax2.set_ylim(0, 1)
        ax2.grid(True, alpha=0.3, axis='y')
        
        for bar, conf in zip(bars, confidences):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{conf:.1%}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    output_path = output_dir / 'personality_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 성격 비교 차트 생성: {output_path.name}")
    plt.close()
    return True

def generate_personality_dashboard(profile: Dict[str, Any], output_dir: Path):
    """개인 특성 분석 종합 대시보드"""
    if not profile.get('evolution'):
        return False
    
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    latest = profile['evolution'][-1]
    weights = latest['personality_weights']
    
    # 1. 레이더 차트 (좌상)
    ax1 = fig.add_subplot(gs[0, 0], projection='polar')
    categories = ['Logic', 'Intuition', 'Fluidity', 'Complexity']
    values = [weights.get(cat, 0.5) for cat in categories]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    
    ax1.plot(angles, values, 'o-', linewidth=2, color=COLORS['primary'])
    ax1.fill(angles, values, alpha=0.25, color=COLORS['primary'])
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(categories, fontsize=10)
    ax1.set_ylim(0, 1)
    ax1.set_title('성격 특성', fontsize=12, fontweight='bold', pad=20)
    
    # 2. 성격 가중치 바 차트 (우상)
    ax2 = fig.add_subplot(gs[0, 1:])
    colors_list = [COLORS['logic'], COLORS['intuition'], COLORS['fluidity'], COLORS['complexity']]
    bars = ax2.bar(categories, values[:-1], color=colors_list, alpha=0.8)
    ax2.set_ylabel('가중치', fontsize=11)
    ax2.set_title('성격 가중치 분포', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, values[:-1]):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{val:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 3. 사용자 정보 (좌중)
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.axis('off')
    info_text = f"""
사용자: {profile['name']}
아키타입: {latest.get('archetype', 'Unknown')}
신뢰도: {latest.get('confidence', 0):.1%}
성숙도: {profile.get('maturity_level', 1)}
동기화 점수: {profile.get('sync_score', 0):.2f}
세션 수: {len(profile.get('evolution', []))}
    """
    ax3.text(0.1, 0.5, info_text, fontsize=11, verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 4. 성격 진화 (우중)
    if len(profile['evolution']) > 1:
        ax4 = fig.add_subplot(gs[1, 1:])
        evolution = profile['evolution']
        session_nums = list(range(1, len(evolution) + 1))
        
        logic = [e['personality_weights']['Logic'] for e in evolution]
        intuition = [e['personality_weights']['Intuition'] for e in evolution]
        fluidity = [e['personality_weights']['Fluidity'] for e in evolution]
        complexity = [e['personality_weights']['Complexity'] for e in evolution]
        
        ax4.plot(session_nums, logic, marker='o', label='Logic', color=COLORS['logic'], linewidth=2)
        ax4.plot(session_nums, intuition, marker='s', label='Intuition', color=COLORS['intuition'], linewidth=2)
        ax4.plot(session_nums, fluidity, marker='^', label='Fluidity', color=COLORS['fluidity'], linewidth=2)
        ax4.plot(session_nums, complexity, marker='d', label='Complexity', color=COLORS['complexity'], linewidth=2)
        
        ax4.set_xlabel('세션', fontsize=11)
        ax4.set_ylabel('가중치', fontsize=11)
        ax4.set_title('성격 가중치 진화', fontsize=12, fontweight='bold')
        ax4.legend(fontsize=9)
        ax4.grid(True, alpha=0.3)
    
    # 5. 행동 패턴 (하단)
    if profile.get('sessions'):
        ax5 = fig.add_subplot(gs[2, :])
        sessions = profile['sessions']
        session_nums = [s['session'] for s in sessions]
        
        latency = [s['behavioral_profile'].get('avgDecisionLatency', 0) / 1000 for s in sessions]
        efficiency = [s['behavioral_profile'].get('pathEfficiency', 0) * 100 for s in sessions]
        
        ax5_twin = ax5.twinx()
        line1 = ax5.plot(session_nums, latency, marker='o', color=COLORS['logic'], 
                        label='의사결정 지연시간', linewidth=2)
        line2 = ax5_twin.plot(session_nums, efficiency, marker='s', color=COLORS['intuition'],
                             label='경로 효율성', linewidth=2)
        
        ax5.set_xlabel('세션', fontsize=11)
        ax5.set_ylabel('의사결정 지연시간 (초)', fontsize=11, color=COLORS['logic'])
        ax5_twin.set_ylabel('경로 효율성 (%)', fontsize=11, color=COLORS['intuition'])
        ax5.set_title('행동 패턴 트렌드', fontsize=12, fontweight='bold')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax5.legend(lines, labels, loc='upper left', fontsize=9)
        ax5.grid(True, alpha=0.3)
    
    fig.suptitle(f'개인 특성 분석 대시보드 - {profile["name"]}', 
                fontsize=16, fontweight='bold', y=0.98)
    
    output_path = output_dir / f'personality_dashboard_{profile["user_id"]}.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 개인 특성 대시보드 생성: {output_path.name}")
    plt.close()
    return True

def main():
    """메인 함수"""
    print("=" * 70)
    print("성격 특성 분석 결과 시각화 시작")
    print("=" * 70)
    
    # 출력 디렉토리 생성
    output_dir = Path(__file__).parent / 'test_visualizations' / 'personality_analysis'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 데이터 로드
    print("\n📊 사용자 프로필 데이터 로드 중...")
    profiles = load_user_profiles_from_db()
    
    # 데이터베이스에 데이터가 없으면 샘플 데이터 사용
    if not profiles:
        print("⚠️ 데이터베이스에 사용자 데이터가 없습니다. 샘플 데이터를 사용합니다.")
        sample = load_sample_data()
        if sample:
            profiles = [sample]
        else:
            print("❌ 사용 가능한 데이터가 없습니다.")
            return
    
    print(f"✓ {len(profiles)}명의 사용자 프로필 로드 완료")
    
    # 차트 생성
    print("\n📈 성격 분석 차트 생성 중...")
    print("-" * 70)
    
    success_count = 0
    
    for profile in profiles:
        if plot_personality_radar(profile, output_dir):
            success_count += 1
        if plot_personality_evolution(profile, output_dir):
            success_count += 1
        if plot_behavioral_patterns(profile, output_dir):
            success_count += 1
        if generate_personality_dashboard(profile, output_dir):
            success_count += 1
    
    # 비교 차트
    if len(profiles) >= 2:
        if plot_personality_comparison(profiles, output_dir):
            success_count += 1
    
    print("\n" + "=" * 70)
    print(f"✅ 성격 특성 분석 시각화 완료! ({success_count}개 차트 생성)")
    print("=" * 70)
    print(f"\n📁 생성된 차트 위치: {output_dir}")
    print("\n생성된 파일:")
    for file in sorted(output_dir.glob('*.png')):
        print(f"  - {file.name}")

if __name__ == '__main__':
    main()
