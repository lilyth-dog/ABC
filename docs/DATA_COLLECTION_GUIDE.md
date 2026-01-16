# 공개 데이터 수집 가이드
## 실제 게임 플레이 데이터를 우리 파이프라인에 연결하기

---

## 🎯 개요

인터넷에서 찾은 공개 게임 데이터셋을 우리 시스템에 연결하는 방법을 설명합니다.

---

## 📦 필요한 패키지 설치

### MineRL (Minecraft 데이터)
```bash
pip install minerl
```

### OpenDota (Dota 2 데이터)
```bash
pip install pyopendota
```

### Riot Watcher (LoL 데이터)
```bash
pip install riotwatcher
```

---

## 🔧 사용 방법

### 1. MineRL 데이터 다운로드

```python
from download_public_data import PublicDataDownloader

downloader = PublicDataDownloader(output_dir="datasets/public")

# MineRL 샘플 데이터 다운로드
events = downloader.download_minerl_sample("MineRLObtainDiamond-v0")
```

### 2. OpenDota 데이터 다운로드

```python
# OpenDota 공개 매치 샘플 다운로드
events = downloader.download_opendota_sample(limit=5)
```

### 3. 우리 파이프라인에 연결

```python
from game_event_parser import parse_game_events
from game_behavior_processor import GameBehaviorProcessor, GameBehavioralData

# 다운로드한 이벤트를 우리 형식으로 변환
raw_events = downloader.download_minerl_sample()

# 파싱
metrics = parse_game_events("minecraft", raw_events)

# 표준 프로필로 변환
processor = GameBehaviorProcessor()
game_data = GameBehavioralData(
    game_id="minecraft",
    session_id="public_data_session",
    planning_time=metrics["planning_time"],
    revision_count=metrics["revision_count"],
    complexity=metrics["complexity"],
    path_efficiency=metrics["path_efficiency"],
    diversity=metrics["diversity"],
    game_specific_metrics={"riskTaking": metrics["risk_taking"]}
)

profile = processor.process(game_data)
```

---

## 🚀 빠른 시작

### 명령줄에서 실행

```bash
# 모든 데이터 소스 다운로드
python backend/download_public_data.py --source all

# MineRL만 다운로드
python backend/download_public_data.py --source minerl

# OpenDota만 다운로드
python backend/download_public_data.py --source opendota
```

---

## 📊 데이터 소스별 상세 정보

자세한 내용은 `docs/PUBLIC_GAME_DATA_SOURCES.md` 참고

---

**© 2026 Nexus Entertainment**
