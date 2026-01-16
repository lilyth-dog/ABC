#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
종합 테스트 및 평가 스크립트
전체 파이프라인을 테스트하고 성능/정확도를 평가
"""
import sys
import json
import time
import os
from typing import Dict, List, Tuple
from datetime import datetime

def test_event_parsing_accuracy():
    """이벤트 파싱 정확도 테스트"""
    print("=" * 60)
    print("1. 이벤트 파싱 정확도 테스트")
    print("=" * 60)
    
    from game_event_parser import parse_game_events
    
    test_cases = [
        {
            "name": "계획 시간 테스트",
            "events": [
                {"type": "inventory_change", "timestamp": 1000, "items": ["stone"]},
                {"type": "inventory_change", "timestamp": 2000, "items": ["dirt"]},
                {"type": "block_place", "timestamp": 5000, "position": {"x": 0, "y": 64, "z": 0}}
            ],
            "expected": {"planning_time": 4000}  # 5000 - 1000
        },
        {
            "name": "수정 빈도 테스트",
            "events": [
                {"type": "block_place", "timestamp": 1000, "position": {"x": 0, "y": 64, "z": 0}},
                {"type": "block_break", "timestamp": 2000, "position": {"x": 0, "y": 64, "z": 0}}
            ],
            "expected": {"revision_count": 1}
        },
        {
            "name": "경로 효율성 테스트",
            "events": [
                {"type": "player_move", "timestamp": 1000, "from": {"x": 0, "y": 64, "z": 0}, "to": {"x": 10, "y": 64, "z": 10}},
                {"type": "player_move", "timestamp": 2000, "from": {"x": 10, "y": 64, "z": 10}, "to": {"x": 20, "y": 64, "z": 20}}
            ],
            "expected": {"path_efficiency": 1.0}  # 직선 이동
        }
    ]
    
    results = []
    for test_case in test_cases:
        metrics = parse_game_events("minecraft", test_case["events"])
        
        # 정확도 계산
        accuracy = {}
        for key, expected_value in test_case["expected"].items():
            actual_value = metrics.get(key, 0)
            if isinstance(expected_value, float):
                diff = abs(actual_value - expected_value)
                accuracy[key] = 1.0 - min(1.0, diff / max(expected_value, 1.0))
            else:
                accuracy[key] = 1.0 if actual_value == expected_value else 0.0
        
        avg_accuracy = sum(accuracy.values()) / len(accuracy) if accuracy else 0.0
        
        results.append({
            "test_name": test_case["name"],
            "metrics": metrics,
            "expected": test_case["expected"],
            "accuracy": accuracy,
            "avg_accuracy": avg_accuracy
        })
        
        print(f"\n✓ {test_case['name']}")
        print(f"  예상: {test_case['expected']}")
        print(f"  실제: {metrics}")
        print(f"  정확도: {avg_accuracy:.2%}")
    
    overall_accuracy = sum(r["avg_accuracy"] for r in results) / len(results) if results else 0.0
    print(f"\n전체 파싱 정확도: {overall_accuracy:.2%}")
    
    return results, overall_accuracy

def test_pipeline_performance():
    """파이프라인 성능 테스트"""
    print("\n" + "=" * 60)
    print("2. 파이프라인 성능 테스트")
    print("=" * 60)
    
    from game_event_parser import parse_game_events
    from game_behavior_processor import GameBehaviorProcessor, GameBehavioralData
    
    # 다양한 크기의 이벤트 세트 테스트
    event_sizes = [10, 50, 100, 500, 1000]
    
    results = []
    for size in event_sizes:
        # Mock 이벤트 생성
        events = []
        for i in range(size):
            events.append({
                "type": "block_place" if i % 2 == 0 else "player_move",
                "timestamp": i * 1000,
                "position": {"x": i, "y": 64, "z": i},
                "block_type": "minecraft:stone" if i % 2 == 0 else None
            })
        
        # 성능 측정
        start_time = time.time()
        
        # 1단계: 파싱
        metrics = parse_game_events("minecraft", events)
        parse_time = time.time() - start_time
        
        # 2단계: 프로필 변환
        start_time = time.time()
        processor = GameBehaviorProcessor()
        game_data = GameBehavioralData(
            game_id="minecraft",
            session_id=f"perf_test_{size}",
            planning_time=metrics["planning_time"],
            revision_count=metrics["revision_count"],
            path_efficiency=metrics["path_efficiency"],
            task_efficiency=0.8,
            complexity=metrics["complexity"],
            diversity=metrics["diversity"],
            game_specific_metrics={}
        )
        profile = processor.process(game_data)
        process_time = time.time() - start_time
        
        total_time = parse_time + process_time
        
        events_per_sec = size / total_time if total_time > 0.0001 else float('inf')
        
        results.append({
            "event_count": size,
            "parse_time": parse_time,
            "process_time": process_time,
            "total_time": total_time,
            "events_per_second": events_per_sec
        })
        
        print(f"\n이벤트 수: {size}")
        print(f"  파싱 시간: {parse_time*1000:.2f}ms")
        print(f"  처리 시간: {process_time*1000:.2f}ms")
        print(f"  총 시간: {total_time*1000:.2f}ms")
        if total_time > 0.0001:
            print(f"  처리 속도: {events_per_sec:.0f} events/sec")
        else:
            print(f"  처리 속도: 매우 빠름 (< 0.1ms)")
    
    return results

def test_data_consistency():
    """데이터 일관성 테스트"""
    print("\n" + "=" * 60)
    print("3. 데이터 일관성 테스트")
    print("=" * 60)
    
    from game_event_parser import parse_game_events
    from game_behavior_processor import GameBehaviorProcessor, GameBehavioralData
    
    # 동일한 이벤트를 여러 번 처리
    events = [
        {"type": "block_place", "timestamp": 1000, "position": {"x": 0, "y": 64, "z": 0}},
        {"type": "block_place", "timestamp": 2000, "position": {"x": 1, "y": 64, "z": 0}},
        {"type": "player_move", "timestamp": 3000, "from": {"x": 0, "y": 64, "z": 0}, "to": {"x": 10, "y": 64, "z": 10}}
    ]
    
    results = []
    for i in range(5):
        metrics = parse_game_events("minecraft", events)
        processor = GameBehaviorProcessor()
        game_data = GameBehavioralData(
            game_id="minecraft",
            session_id=f"consistency_test_{i}",
            planning_time=metrics["planning_time"],
            revision_count=metrics["revision_count"],
            path_efficiency=metrics["path_efficiency"],
            task_efficiency=0.8,
            complexity=metrics["complexity"],
            diversity=metrics["diversity"],
            game_specific_metrics={}
        )
        profile = processor.process(game_data)
        results.append(profile)
    
    # 일관성 확인
    first_result = results[0]
    consistent = True
    for i, result in enumerate(results[1:], 1):
        for key in first_result:
            if isinstance(first_result[key], float):
                diff = abs(first_result[key] - result.get(key, 0))
                if diff > 0.0001:  # 부동소수점 오차 허용
                    consistent = False
                    print(f"⚠ 불일치 발견 (실행 {i+1}): {key} = {result.get(key)} (예상: {first_result[key]})")
            elif first_result[key] != result.get(key):
                consistent = False
                print(f"⚠ 불일치 발견 (실행 {i+1}): {key} = {result.get(key)} (예상: {first_result[key]})")
    
    if consistent:
        print("✓ 모든 실행에서 일관된 결과")
    else:
        print("⚠ 일관성 문제 발견")
    
    return consistent, results

def test_edge_cases():
    """엣지 케이스 테스트"""
    print("\n" + "=" * 60)
    print("4. 엣지 케이스 테스트")
    print("=" * 60)
    
    from game_event_parser import parse_game_events
    from game_behavior_processor import GameBehaviorProcessor, GameBehavioralData
    
    edge_cases = [
        {
            "name": "빈 이벤트 리스트",
            "events": []
        },
        {
            "name": "단일 이벤트",
            "events": [
                {"type": "block_place", "timestamp": 1000, "position": {"x": 0, "y": 64, "z": 0}}
            ]
        },
        {
            "name": "타임스탬프 없음",
            "events": [
                {"type": "block_place", "position": {"x": 0, "y": 64, "z": 0}}
            ]
        },
        {
            "name": "위치 정보 없음",
            "events": [
                {"type": "block_place", "timestamp": 1000}
            ]
        }
    ]
    
    results = []
    for case in edge_cases:
        try:
            metrics = parse_game_events("minecraft", case["events"])
            processor = GameBehaviorProcessor()
            game_data = GameBehavioralData(
                game_id="minecraft",
                session_id="edge_test",
                planning_time=metrics.get("planning_time", 0),
                revision_count=metrics.get("revision_count", 0),
                path_efficiency=metrics.get("path_efficiency", 0.5),
                task_efficiency=0.8,
                complexity=metrics.get("complexity", 0.5),
                diversity=metrics.get("diversity", 0.5),
                game_specific_metrics={}
            )
            profile = processor.process(game_data)
            
            results.append({
                "case": case["name"],
                "status": "success",
                "profile": profile
            })
            print(f"✓ {case['name']}: 성공")
            
        except Exception as e:
            results.append({
                "case": case["name"],
                "status": "error",
                "error": str(e)
            })
            print(f"⚠ {case['name']}: 오류 - {e}")
    
    return results

def test_real_data_integration():
    """실제 데이터 통합 테스트"""
    print("\n" + "=" * 60)
    print("5. 실제 데이터 통합 테스트")
    print("=" * 60)
    
    # 실제 다운로드한 데이터 확인
    real_data_files = [
        "datasets/public/opendota_real_match_8650963582.json",
        "datasets/public/full_pipeline_result.json"
    ]
    
    results = []
    for file_path in real_data_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                file_size = os.path.getsize(file_path)
                results.append({
                    "file": file_path,
                    "status": "exists",
                    "size": file_size,
                    "keys": list(data.keys()) if isinstance(data, dict) else "N/A"
                })
                print(f"✓ {file_path}: {file_size} bytes")
                
            except Exception as e:
                results.append({
                    "file": file_path,
                    "status": "error",
                    "error": str(e)
                })
                print(f"⚠ {file_path}: 오류 - {e}")
        else:
            results.append({
                "file": file_path,
                "status": "not_found"
            })
            print(f"⚠ {file_path}: 파일 없음")
    
    return results

def generate_evaluation_report():
    """종합 평가 리포트 생성"""
    print("\n" + "=" * 60)
    print("종합 평가 리포트 생성")
    print("=" * 60)
    
    report = {
        "test_date": datetime.now().isoformat(),
        "tests": {}
    }
    
    # 1. 파싱 정확도
    parse_results, parse_accuracy = test_event_parsing_accuracy()
    report["tests"]["parsing_accuracy"] = {
        "overall_accuracy": parse_accuracy,
        "details": parse_results
    }
    
    # 2. 성능
    perf_results = test_pipeline_performance()
    report["tests"]["performance"] = perf_results
    
    # 3. 일관성
    consistent, consistency_results = test_data_consistency()
    report["tests"]["consistency"] = {
        "is_consistent": consistent,
        "results": len(consistency_results)
    }
    
    # 4. 엣지 케이스
    edge_results = test_edge_cases()
    report["tests"]["edge_cases"] = edge_results
    
    # 5. 실제 데이터
    real_data_results = test_real_data_integration()
    report["tests"]["real_data"] = real_data_results
    
    # 종합 평가
    perf_summary = "N/A"
    if perf_results:
        last_perf = perf_results[-1]
        if last_perf['events_per_second'] == float('inf'):
            perf_summary = "매우 빠름 (< 0.1ms)"
        else:
            perf_summary = f"{last_perf['events_per_second']:.0f} events/sec"
    
    report["summary"] = {
        "parsing_accuracy": f"{parse_accuracy:.2%}",
        "performance": perf_summary,
        "consistency": "✓" if consistent else "⚠",
        "edge_cases_handled": sum(1 for r in edge_results if r["status"] == "success"),
        "real_data_files": sum(1 for r in real_data_results if r.get("status") == "exists")
    }
    
    # 저장
    output_dir = "datasets/public"
    os.makedirs(output_dir, exist_ok=True)
    
    report_path = f"{output_dir}/evaluation_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ 평가 리포트 저장: {report_path}")
    
    # 요약 출력
    print("\n" + "=" * 60)
    print("종합 평가 요약")
    print("=" * 60)
    print(f"파싱 정확도: {report['summary']['parsing_accuracy']}")
    print(f"성능: {report['summary']['performance']}")
    print(f"일관성: {report['summary']['consistency']}")
    print(f"엣지 케이스 처리: {report['summary']['edge_cases_handled']}/{len(edge_results)}")
    print(f"실제 데이터 파일: {report['summary']['real_data_files']}")
    
    return report

if __name__ == "__main__":
    try:
        report = generate_evaluation_report()
        
        print("\n" + "=" * 60)
        print("✓ 종합 테스트 및 평가 완료!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
