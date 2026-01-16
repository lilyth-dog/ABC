"""
실제 데이터베이스에서 사용자 데이터를 추출하여 시연용 JSON으로 변환
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "backend" / "user_profiles.db"

def extract_real_user_data(user_id: str = None):
    """실제 데이터베이스에서 사용자 데이터 추출"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 사용자 목록 가져오기 (진화 기록이 있는 사용자 우선)
    if user_id:
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    else:
        # 진화 기록이 있는 사용자 찾기
        cursor.execute("""
            SELECT DISTINCT u.* FROM users u
            INNER JOIN profile_evolution pe ON u.id = pe.user_id
            WHERE pe.logic_weight IS NOT NULL AND pe.logic_weight != 0.5
            ORDER BY u.created_at DESC LIMIT 1
        """)
        user = cursor.fetchone()
        if not user:
            # 진화 기록이 없으면 최근 사용자
            cursor.execute("SELECT * FROM users ORDER BY created_at DESC LIMIT 1")
    
    user = cursor.fetchone()
    
    if not user:
        print("사용자 데이터를 찾을 수 없습니다.")
        return None
    
    user_id = user['id']
    print(f"사용자 ID: {user_id}")
    
    # 세션 데이터 가져오기
    cursor.execute("""
        SELECT * FROM behavioral_sessions 
        WHERE user_id = ? 
        ORDER BY session_timestamp ASC
    """, (user_id,))
    sessions = cursor.fetchall()
    
    # 진화 기록 가져오기
    cursor.execute("""
        SELECT * FROM profile_evolution 
        WHERE user_id = ? 
        ORDER BY timestamp ASC
    """, (user_id,))
    evolution = cursor.fetchall()
    
    conn.close()
    
    # 데이터 구조화
    result = {
        "user_id": user_id,
        "name": user['display_name'] if user['display_name'] else '실제 사용자',
        "sessions": [],
        "evolution": []
    }
    
    # 세션 데이터 변환
    for i, session in enumerate(sessions, 1):
        raw_metrics = {}
        if session['raw_metrics']:
            try:
                raw_metrics = json.loads(session['raw_metrics'])
            except:
                pass
        
        session_data = {
            "session": i,
            "timestamp": session['session_timestamp'],
            "behavioral_profile": {
                "pathEfficiency": session['path_efficiency'] if session['path_efficiency'] else 0.0,
                "avgDecisionLatency": session['avg_decision_latency'] if session['avg_decision_latency'] else 0,
                "revisionRate": int(session['revision_rate'] if session['revision_rate'] else 0),
                "jitterIndex": 0.0,  # DB에 없으면 기본값
                "intensity": 1.0
            }
        }
        
        # 진화 기록에서 가중치 가져오기
        if i <= len(evolution):
            evo = evolution[i-1]
            session_data["personality_weights"] = {
                "Logic": evo['logic_weight'] if evo['logic_weight'] else 0.5,
                "Intuition": evo['intuition_weight'] if evo['intuition_weight'] else 0.5,
                "Fluidity": evo['fluidity_weight'] if evo['fluidity_weight'] else 0.5,
                "Complexity": evo['complexity_weight'] if evo['complexity_weight'] else 0.5
            }
            session_data["confidence"] = evo['confidence_score'] if evo['confidence_score'] else 0.0
            session_data["maturity_level"] = user['maturity_level'] if user['maturity_level'] else 1
            session_data["sync_score"] = user['sync_score'] if user['sync_score'] else 0.0
        else:
            # 기본값
            session_data["personality_weights"] = {
                "Logic": 0.5,
                "Intuition": 0.5,
                "Fluidity": 0.5,
                "Complexity": 0.5
            }
            session_data["confidence"] = 0.3
            session_data["maturity_level"] = 1
            session_data["sync_score"] = 0.5
        
        result["sessions"].append(session_data)
    
    # 진화 기록 변환
    for evo in evolution:
        result["evolution"].append({
            "timestamp": evo['timestamp'],
            "weights": {
                "Logic": evo['logic_weight'] if evo['logic_weight'] else 0.5,
                "Intuition": evo['intuition_weight'] if evo['intuition_weight'] else 0.5,
                "Fluidity": evo['fluidity_weight'] if evo['fluidity_weight'] else 0.5,
                "Complexity": evo['complexity_weight'] if evo['complexity_weight'] else 0.5
            },
            "confidence": evo['confidence_score'] if evo['confidence_score'] else 0.0,
            "archetype": evo['archetype'] if evo['archetype'] else 'Unknown'
        })
    
    return result

if __name__ == '__main__':
    print("=" * 60)
    print("실제 데이터베이스에서 사용자 데이터 추출")
    print("=" * 60)
    
    # 진화 기록이 있는 사용자 찾기
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT user_id FROM profile_evolution 
        WHERE logic_weight IS NOT NULL AND logic_weight != 0.5
        LIMIT 1
    """)
    result = cursor.fetchone()
    conn.close()
    
    user_id = result['user_id'] if result else None
    
    if user_id:
        print(f"진화 기록이 있는 사용자 발견: {user_id}")
        data = extract_real_user_data(user_id)
    else:
        print("진화 기록이 있는 사용자를 찾을 수 없습니다. 최근 사용자로 시도...")
        data = extract_real_user_data()
    
    if data:
        output_path = Path(__file__).parent / "real_user_profile.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 데이터 추출 완료: {output_path}")
        print(f"  - 사용자: {data['user_id']}")
        print(f"  - 세션 수: {len(data['sessions'])}")
        print(f"  - 진화 기록: {len(data['evolution'])}")
    else:
        print("\n✗ 데이터를 추출할 수 없습니다.")
