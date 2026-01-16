#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 결과 시각화 스크립트
최종 검증 테스트 결과를 다양한 차트로 시각화
"""
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False

# 색상 팔레트
COLORS = {
    'pass': '#4ecdc4',
    'fail': '#ff6b6b',
    'warning': '#ffd93d',
    'primary': '#00f2ff',
    'secondary': '#95e1d3',
    'accent': '#f38181'
}

def load_test_results() -> Dict[str, Any]:
    """테스트 결과 JSON 파일 로드"""
    results_path = Path(__file__).parent / 'test_results_final.json'
    
    if not results_path.exists():
        print(f"❌ 테스트 결과 파일을 찾을 수 없습니다: {results_path}")
        sys.exit(1)
    
    with open(results_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def plot_overall_summary(data: Dict[str, Any], output_dir: Path):
    """전체 테스트 요약 파이 차트"""
    summary = data['summary']
    total = summary['total_tests']
    passed = summary['total_passed']
    failed = total - passed
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 파이 차트
    if failed > 0:
        sizes = [passed, failed]
        labels = ['통과', '실패']
        colors = [COLORS['pass'], COLORS['fail']]
        explode = (0.05, 0.1)
    else:
        sizes = [passed]
        labels = ['통과']
        colors = [COLORS['pass']]
        explode = (0.05,)
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, explode=explode, shadow=True)
    ax1.set_title('전체 테스트 통과율', fontsize=14, fontweight='bold', pad=20)
    
    # 통계 정보
    stats_text = f"""
전체 테스트: {total}개
통과: {passed}개
실패: {failed}개
통과율: {summary['overall_percentage']:.1f}%
상태: {summary['status']}
    """
    ax2.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax2.axis('off')
    ax2.set_title('테스트 통계', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    output_path = output_dir / 'test_overall_summary.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 전체 요약 차트 생성: {output_path}")
    plt.close()

def plot_category_results(data: Dict[str, Any], output_dir: Path):
    """카테고리별 테스트 결과 바 차트"""
    tests = data['tests']
    
    categories = []
    passed_counts = []
    total_counts = []
    pass_rates = []
    
    for cat_name, cat_data in tests.items():
        categories.append(cat_name.replace('_', ' ').title())
        passed_counts.append(cat_data['passed'])
        total_counts.append(cat_data['total'])
        pass_rates.append((cat_data['passed'] / cat_data['total']) * 100)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # 바 차트: 통과/실패 수
    x = np.arange(len(categories))
    width = 0.35
    
    passed_bars = ax1.bar(x - width/2, passed_counts, width, 
                          label='통과', color=COLORS['pass'], alpha=0.8)
    failed_bars = ax1.bar(x + width/2, 
                          [total - passed for total, passed in zip(total_counts, passed_counts)],
                          width, label='실패', color=COLORS['fail'], alpha=0.8)
    
    ax1.set_xlabel('테스트 카테고리', fontsize=12)
    ax1.set_ylabel('테스트 수', fontsize=12)
    ax1.set_title('카테고리별 테스트 결과', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, rotation=15, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 바 위에 숫자 표시
    for i, (passed, total) in enumerate(zip(passed_counts, total_counts)):
        ax1.text(i - width/2, passed + 0.1, str(passed), 
                ha='center', va='bottom', fontweight='bold')
        failed = total - passed
        if failed > 0:
            ax1.text(i + width/2, failed + 0.1, str(failed), 
                    ha='center', va='bottom', fontweight='bold')
    
    # 통과율 바 차트
    colors = [COLORS['pass'] if rate == 100 else COLORS['warning'] 
              for rate in pass_rates]
    bars = ax2.bar(categories, pass_rates, color=colors, alpha=0.8)
    ax2.set_xlabel('테스트 카테고리', fontsize=12)
    ax2.set_ylabel('통과율 (%)', fontsize=12)
    ax2.set_title('카테고리별 통과율', fontsize=14, fontweight='bold')
    ax2.set_xticks(range(len(categories)))
    ax2.set_xticklabels(categories, rotation=15, ha='right')
    ax2.set_ylim(0, 105)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.axhline(y=100, color='green', linestyle='--', linewidth=2, alpha=0.5)
    
    # 바 위에 퍼센트 표시
    for bar, rate in zip(bars, pass_rates):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    output_path = output_dir / 'test_category_results.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 카테고리별 결과 차트 생성: {output_path}")
    plt.close()

def plot_performance_metrics(data: Dict[str, Any], output_dir: Path):
    """성능 메트릭 시각화"""
    performance_tests = data['tests'].get('performance', {}).get('results', [])
    
    if not performance_tests:
        print("⚠️ 성능 테스트 데이터가 없습니다.")
        return
    
    metrics = []
    values = []
    units = []
    
    for test in performance_tests:
        details = test.get('details', '')
        name = test.get('name', '')
        
        # 세부 정보에서 숫자 추출
        if 'events/sec' in details:
            # "0.84ms, 1186843 events/sec" 형식
            parts = details.split(',')
            if len(parts) >= 2:
                time_part = parts[0].strip()
                events_part = parts[1].strip()
                
                # 처리 시간
                if 'ms' in time_part:
                    time_val = float(time_part.replace('ms', '').strip())
                    metrics.append(f"{name}\n(처리 시간)")
                    values.append(time_val)
                    units.append('ms')
                
                # 이벤트 처리 속도
                if 'events/sec' in events_part:
                    events_val = float(events_part.replace('events/sec', '').replace(',', '').strip())
                    metrics.append(f"{name}\n(처리 속도)")
                    values.append(events_val / 1000)  # 천 단위로 변환
                    units.append('천 events/sec')
        elif 'ms' in details:
            # "3.62ms" 형식
            time_val = float(details.replace('ms', '').strip())
            metrics.append(name)
            values.append(time_val)
            units.append('ms')
    
    if not metrics:
        print("⚠️ 성능 메트릭을 추출할 수 없습니다.")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 바 차트
    colors = [COLORS['primary'] if '처리 속도' in m else COLORS['secondary'] 
              for m in metrics]
    bars = ax.bar(metrics, values, color=colors, alpha=0.8)
    
    ax.set_ylabel('값', fontsize=12)
    ax.set_title('성능 메트릭', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(metrics)))
    ax.set_xticklabels(metrics, rotation=15, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    
    # 바 위에 값과 단위 표시
    for bar, val, unit in zip(bars, values, units):
        height = bar.get_height()
        if unit == 'ms':
            label = f'{val:.2f} {unit}'
        else:
            label = f'{val:.1f} {unit}'
        ax.text(bar.get_x() + bar.get_width()/2., height + height*0.05,
                label, ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    output_path = output_dir / 'test_performance_metrics.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 성능 메트릭 차트 생성: {output_path}")
    plt.close()

def plot_test_status_breakdown(data: Dict[str, Any], output_dir: Path):
    """테스트 상태 상세 분석"""
    tests = data['tests']
    
    all_results = []
    for cat_name, cat_data in tests.items():
        for result in cat_data.get('results', []):
            all_results.append({
                'category': cat_name.replace('_', ' ').title(),
                'name': result.get('name', ''),
                'status': result.get('status', 'UNKNOWN')
            })
    
    # 상태별 집계
    status_counts = {}
    for result in all_results:
        status = result['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # 파이 차트
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if status_counts:
        labels = list(status_counts.keys())
        sizes = list(status_counts.values())
        colors_list = [COLORS.get(status.lower(), COLORS['primary']) 
                      for status in labels]
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors_list,
                                          autopct='%1.1f%%', startangle=90,
                                          shadow=True, explode=[0.05]*len(sizes))
        
        # 텍스트 스타일 조정
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(12)
        
        ax.set_title('테스트 상태 분포', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    output_path = output_dir / 'test_status_breakdown.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 테스트 상태 분석 차트 생성: {output_path}")
    plt.close()

def generate_test_dashboard(data: Dict[str, Any], output_dir: Path):
    """종합 대시보드 생성"""
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. 전체 요약 (좌상)
    ax1 = fig.add_subplot(gs[0, 0])
    summary = data['summary']
    total = summary['total_tests']
    passed = summary['total_passed']
    failed = total - passed
    
    if failed > 0:
        sizes = [passed, failed]
        labels = ['통과', '실패']
        colors = [COLORS['pass'], COLORS['fail']]
    else:
        sizes = [passed]
        labels = ['통과']
        colors = [COLORS['pass']]
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, shadow=True)
    ax1.set_title('전체 통과율', fontsize=12, fontweight='bold')
    
    # 2. 카테고리별 통과율 (우상)
    ax2 = fig.add_subplot(gs[0, 1:])
    tests = data['tests']
    categories = []
    pass_rates = []
    
    for cat_name, cat_data in tests.items():
        categories.append(cat_name.replace('_', ' ').title())
        rate = (cat_data['passed'] / cat_data['total']) * 100
        pass_rates.append(rate)
    
    colors_list = [COLORS['pass'] if rate == 100 else COLORS['warning'] 
                  for rate in pass_rates]
    bars = ax2.bar(categories, pass_rates, color=colors_list, alpha=0.8)
    ax2.set_ylabel('통과율 (%)', fontsize=11)
    ax2.set_title('카테고리별 통과율', fontsize=12, fontweight='bold')
    ax2.set_xticks(range(len(categories)))
    ax2.set_xticklabels(categories, rotation=15, ha='right', fontsize=9)
    ax2.set_ylim(0, 105)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.axhline(y=100, color='green', linestyle='--', linewidth=1, alpha=0.5)
    
    for bar, rate in zip(bars, pass_rates):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{rate:.0f}%', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # 3. 테스트 통계 (좌중)
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.axis('off')
    stats_text = f"""
전체 테스트: {total}개
통과: {passed}개
실패: {failed}개
통과율: {summary['overall_percentage']:.1f}%
상태: {summary['status']}
    """
    ax3.text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax3.set_title('테스트 통계', fontsize=12, fontweight='bold')
    
    # 4. 카테고리별 상세 (우중)
    ax4 = fig.add_subplot(gs[1, 1:])
    category_names = []
    passed_counts = []
    total_counts = []
    
    for cat_name, cat_data in tests.items():
        category_names.append(cat_name.replace('_', ' ').title())
        passed_counts.append(cat_data['passed'])
        total_counts.append(cat_data['total'])
    
    x = np.arange(len(category_names))
    width = 0.35
    
    ax4.bar(x - width/2, passed_counts, width, label='통과', 
           color=COLORS['pass'], alpha=0.8)
    ax4.bar(x + width/2, [t - p for t, p in zip(total_counts, passed_counts)],
           width, label='실패', color=COLORS['fail'], alpha=0.8)
    
    ax4.set_xlabel('테스트 카테고리', fontsize=11)
    ax4.set_ylabel('테스트 수', fontsize=11)
    ax4.set_title('카테고리별 테스트 수', fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(category_names, rotation=15, ha='right', fontsize=9)
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 5. 성능 메트릭 (하단 전체)
    ax5 = fig.add_subplot(gs[2, :])
    performance_tests = data['tests'].get('performance', {}).get('results', [])
    
    if performance_tests:
        perf_names = []
        perf_values = []
        
        for test in performance_tests:
            details = test.get('details', '')
            name = test.get('name', '')
            
            if 'events/sec' in details:
                parts = details.split(',')
                if len(parts) >= 2:
                    events_part = parts[1].strip()
                    if 'events/sec' in events_part:
                        events_val = float(events_part.replace('events/sec', '').replace(',', '').strip())
                        perf_names.append(f"{name}\n(처리 속도)")
                        perf_values.append(events_val / 1000)  # 천 단위
            elif 'ms' in details:
                time_val = float(details.replace('ms', '').strip())
                perf_names.append(f"{name}\n(응답 시간)")
                perf_values.append(time_val)
        
        if perf_names:
            colors_list = [COLORS['primary'] if '속도' in n else COLORS['secondary'] 
                          for n in perf_names]
            bars = ax5.bar(perf_names, perf_values, color=colors_list, alpha=0.8)
            ax5.set_ylabel('값', fontsize=11)
            ax5.set_title('성능 메트릭', fontsize=12, fontweight='bold')
            ax5.set_xticks(range(len(perf_names)))
            ax5.set_xticklabels(perf_names, rotation=15, ha='right', fontsize=9)
            ax5.grid(True, alpha=0.3, axis='y')
            
            for bar, val in zip(bars, perf_values):
                height = bar.get_height()
                if val > 100:
                    label = f'{val:.1f}K'
                else:
                    label = f'{val:.2f}'
                ax5.text(bar.get_x() + bar.get_width()/2., height + height*0.05,
                        label, ha='center', va='bottom', fontweight='bold', fontsize=9)
    else:
        ax5.text(0.5, 0.5, '성능 테스트 데이터 없음', 
                ha='center', va='center', fontsize=12)
        ax5.set_title('성능 메트릭', fontsize=12, fontweight='bold')
    
    # 전체 제목
    fig.suptitle('테스트 결과 종합 대시보드', fontsize=18, fontweight='bold', y=0.98)
    
    output_path = output_dir / 'test_dashboard.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 종합 대시보드 생성: {output_path}")
    plt.close()

def main():
    """메인 함수"""
    print("=" * 70)
    print("테스트 결과 시각화 시작")
    print("=" * 70)
    
    # 출력 디렉토리 생성
    output_dir = Path(__file__).parent / 'test_visualizations'
    output_dir.mkdir(exist_ok=True)
    
    # 테스트 결과 로드
    print("\n📊 테스트 결과 로드 중...")
    data = load_test_results()
    print(f"✓ 테스트 결과 로드 완료: {data['summary']['total_tests']}개 테스트")
    
    # 차트 생성
    print("\n📈 차트 생성 중...")
    print("-" * 70)
    
    try:
        plot_overall_summary(data, output_dir)
        plot_category_results(data, output_dir)
        plot_performance_metrics(data, output_dir)
        plot_test_status_breakdown(data, output_dir)
        generate_test_dashboard(data, output_dir)
        
        print("\n" + "=" * 70)
        print("✅ 테스트 결과 시각화 완료!")
        print("=" * 70)
        print(f"\n📁 생성된 차트 위치: {output_dir}")
        print("\n생성된 파일:")
        for file in sorted(output_dir.glob('*.png')):
            print(f"  - {file.name}")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
