# 공개 게임 플레이 데이터 소스
## 인터넷에서 찾은 실제 사용 가능한 데이터셋

---

## 🎮 즉시 사용 가능한 공개 데이터셋

### 1. Minecraft (마인크래프트)

#### MineRL 데이터셋
- **설명**: 인간 플레이 시연 데이터 (비디오 + 키/마우스 액션)
- **규모**: 
  - MineRL 2019: 6천만 프레임 규모
  - BASALT BEDD: 2,600만 이미지-액션 페어, 1.4만 비디오
- **포함 내용**: 상태-행동-보상 시퀀스, ObtainDiamond, Treechop 등 환경별 데이터
- **다운로드**:
  - Zenodo 미러: https://zenodo.org/records/11996496
  - GitHub: https://github.com/minerllabs/minerl
  - Python 패키지: `pip install minerl`
- **용량**: 전체 약 700GB (테스트용 5GB 제공)
- **라이선스**: 연구용 공개

#### MineDojo
- **설명**: 인터넷 스케일 지식 베이스
- **포함 내용**:
  - 73만 YouTube 영상 (자막 정렬)
  - 7천 Wiki 페이지
  - 34만 Reddit 포스트
- **다운로드**: https://docs.minedojo.org/sections/getting_started/data.html

---

### 2. Dota 2

#### OpenDota API
- **설명**: Dota 2 리플레이에서 추출한 고급 매치 데이터
- **제공 데이터**:
  - 매치 상세 정보
  - 영웅/아이템 통계
  - 타임라인 이벤트
  - 플레이어 행동 패턴
- **API 엔드포인트**: https://www.opendota.com/api
- **제한**: 비키 2,000회/일 (프리미엄 무제한)
- **Python 클라이언트**: `pip install pyopendota`

---

### 3. League of Legends

#### Riot Games 공식 API
- **설명**: LoL/TFT 매치 데이터 및 타임라인
- **제공 데이터**:
  - 매치 상세 정보
  - 타임라인 (프레임별 이벤트)
  - 플레이어 통계
  - 챔피언/아이템 데이터
- **API 문서**: https://developer.riotgames.com/
- **보존 기간**: 매치 데이터 2년, 타임라인 1년
- **Python 라이브러리**: `pip install riotwatcher`

#### Oracle's Elixir
- **설명**: 프로 리그 매치/선수/팀 통계 CSV
- **다운로드**: 연도별 대량 다운로드 경로 제공
- **참고**: https://dsc80.com/proj04/league-of-legends/

---

### 4. PUBG

#### PUBG 공식 API
- **설명**: 매치별 텔레메트리 데이터
- **제공 데이터**:
  - 이벤트 스트림 (킬, 사망, 아이템 등)
  - 플레이어 위치 데이터
  - 무기/생존 마스터리 통계
- **API 문서**: https://documentation.pubg.com/en/getting-started.html
- **포맷**: gzip JSON
- **TypeScript SDK**: https://github.com/martinsileno/pubg-typescript-api

#### Kaggle PUBG 데이터셋
- **설명**: "Finish Placement Prediction" 대회 데이터
- **규모**: 수백만 라운드의 매치 통계
- **다운로드**: Kaggle API 사용
- **참고**: https://pubg-prediction.github.io/project/

---

### 5. CS:GO / CS2

#### PureSkill.gg 공개 데이터셋
- **설명**: 경쟁전 텔레메트리 데이터
- **포함 내용**:
  - 플레이어 텔레메트리
  - 타임스탬프 이벤트
  - 전체 이벤트 로그
- **다운로드**: AWS Data Exchange (비영리 CC BY-NC-SA)
- **문서**: https://docs.pureskill.gg/datascience/adx/csgo/csds/

#### 데모 파일 파서
- **demofile** (Node.js): https://demofile.dev/
- **demoparser2** (Python/JS): https://github.com/LaihoE/demoparser
- **Awpy** (Python): `pip install awpy`

---

### 6. Stardew Valley

#### 세이브 파일 기반 데이터
- **설명**: 세이브 파일은 XML 구조로 저장됨
- **위치**: 게임 설치 폴더의 세이브 디렉토리
- **문서**: https://stardewvalleywiki.com/Saves
- **파싱**: XML 파서로 직접 추출 가능

---

### 7. StarCraft

#### StarData (SC: Brood War)
- **규모**: 6.5만 리플레이, 365GB, 15.35억 프레임
- **GitHub**: https://github.com/TorchCraft/StarData

#### StarCraft II
- **공식 파서**: Blizzard s2protocol (Python)
- **GitHub**: https://github.com/Blizzard/s2protocol
- **SC2EGSet**: e스포츠 경기 데이터 (2025-03 공개)
- **StarCraftImage**: 360만 샘플 이미지 데이터

---

## 🔧 사용자 행동 데이터셋

### 마우스 움직임 / 클릭 행동
- **Atari-HEAD**: 인간 시선·행동 동시 기록 (20여 종, 117h)
- **PubMed**: https://pubmed.ncbi.nlm.nih.gov/32901213/
- **포함**: 토렌트/링크로 배포되는 메타·압축 파일

---

## 📊 Steam 데이터

### Steam Web API
- **제공 데이터**:
  - 유저 소유 게임
  - 플레이타임 (전체/2주)
  - 업적/게임 통계
- **API 문서**: https://wiki.teamfortress.com/wiki/WebAPI/GetOwnedGames
- **제한**: 공개 프로필 또는 API 키 필요

### Steam 데이터셋 (오픈 수집본)
- **규모**: 1억+ 리뷰
- **GitHub**: https://github.com/vintagedon/steam-dataset-2025

---

## 🎯 우리 프로젝트에 적용 가능한 데이터

### 우선순위 1: Minecraft (MineRL)
- ✅ **이유**: 우리가 언급한 게임 중 하나
- ✅ **데이터 형식**: 상태-행동 시퀀스 (우리 파이프라인과 유사)
- ✅ **규모**: 대규모 데이터셋 (6천만 프레임)
- ✅ **사용 방법**: 
  ```python
  import minerl
  # 데이터 로드 및 파싱
  data = minerl.data.make('MineRLObtainDiamond-v0')
  ```

### 우선순위 2: Dota 2 (OpenDota)
- ✅ **이유**: 실시간 매치 데이터, 타임라인 이벤트
- ✅ **데이터 형식**: JSON API (우리 API와 유사)
- ✅ **사용 방법**:
  ```python
  from pyopendota import OpenDota
  client = OpenDota()
  match = client.get_match(match_id)
  ```

### 우선순위 3: PUBG 텔레메트리
- ✅ **이유**: 상세한 이벤트 스트림
- ✅ **데이터 형식**: gzip JSON (우리 파이프라인과 호환)
- ✅ **사용 방법**: API 호출 후 JSON 파싱

---

## 💡 실제 사용 예시

### MineRL 데이터를 우리 파이프라인에 연결

```python
import minerl
from game_event_parser import parse_game_events

# MineRL 데이터 로드
data = minerl.data.make('MineRLObtainDiamond-v0')

# 샘플 데이터 추출
for obs, act, rew, next_obs, done in data.batch_iter(1, 1, 1):
    # MineRL 데이터를 우리 형식으로 변환
    raw_events = convert_minerl_to_our_format(obs, act)
    
    # 우리 파이프라인으로 처리
    metrics = parse_game_events("minecraft", raw_events)
    
    # 성격 추론
    # ... (기존 로직)
```

### OpenDota API를 우리 파이프라인에 연결

```python
from pyopendota import OpenDota
from game_event_parser import parse_game_events

client = OpenDota()
match = client.get_match(match_id)

# Dota 2 이벤트를 우리 형식으로 변환
raw_events = convert_dota2_to_our_format(match)

# 우리 파이프라인으로 처리
metrics = parse_game_events("dota2", raw_events)
```

---

## 📝 데이터 수집 스크립트 예시

### MineRL 데이터 다운로드

```python
import minerl

# 데이터셋 다운로드
data = minerl.data.make('MineRLObtainDiamond-v0')

# 샘플 데이터 확인
for obs, act, rew, next_obs, done in data.batch_iter(1, 1, 1):
    print(f"Observation: {obs.keys()}")
    print(f"Action: {act.keys()}")
    break
```

### OpenDota API 사용

```python
from pyopendota import OpenDota
import requests

client = OpenDota()

# 공개 매치 조회
matches = client.get_public_matches(limit=10)

for match in matches:
    match_id = match['match_id']
    match_detail = client.get_match(match_id)
    
    # 이벤트 추출
    events = extract_events_from_match(match_detail)
    
    # 우리 파이프라인으로 처리
    # ...
```

---

## ⚠️ 주의사항

### 라이선스 및 약관
- **Riot API**: 약관 준수 필수, 일부 데이터 제한
- **OpenDota**: 프라이버시 설정에 따라 데이터 공백 가능
- **PUBG API**: 인증키 필요, 사용 제한 확인
- **MineRL**: 연구용 공개, 라이선스 확인 필요

### 데이터 제한
- **API 레이트리밋**: OpenDota (2,000회/일), Riot (지역별 제한)
- **보존 기간**: Riot 타임라인 (1년), 매치 데이터 (2년)
- **프라이버시**: 공개 설정에 따라 데이터 접근 제한

---

## 🔗 유용한 링크

### 데이터셋 다운로드
- **MineRL**: https://zenodo.org/records/11996496
- **MineDojo**: https://docs.minedojo.org/sections/getting_started/data.html
- **PureSkill.gg**: https://docs.pureskill.gg/datascience/

### API 문서
- **Riot Games**: https://developer.riotgames.com/
- **OpenDota**: https://www.opendota.com/api
- **PUBG**: https://documentation.pubg.com/en/getting-started.html
- **Steam**: https://wiki.teamfortress.com/wiki/WebAPI/GetOwnedGames

### 파서 라이브러리
- **MineRL Python**: `pip install minerl`
- **OpenDota Python**: `pip install pyopendota`
- **Riot Watcher**: `pip install riotwatcher`
- **Awpy (CS:GO)**: `pip install awpy`

---

## 📊 데이터 활용 전략

### 단기 (데모/시연용)
1. **MineRL 샘플 데이터** 사용 (5GB 테스트 데이터)
2. **OpenDota 공개 매치** 몇 개만 수집
3. **Mock 데이터 생성** (기존 방식 유지)

### 중기 (연구/개발용)
1. **MineRL 전체 데이터셋** 다운로드 (700GB)
2. **OpenDota API** 정기 수집 스크립트 구축
3. **PUBG 텔레메트리** 샘플 수집

### 장기 (프로덕션용)
1. **실시간 API 연동** (Riot, OpenDota, PUBG)
2. **대규모 데이터 파이프라인** 구축
3. **데이터 저장소** 구축 (S3, 데이터베이스)

---

**© 2026 Nexus Entertainment**
