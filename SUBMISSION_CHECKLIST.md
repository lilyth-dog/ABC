# 제출 체크리스트

## 📦 제출 구성

### 1. 논문 제출 ✅
- [x] 논문 아카이브 생성 완료
- [x] 제출용 DOCX 파일 준비
- [x] 마크다운 소스 파일 포함
- [x] 양식 파일 포함
- [x] 로고 이미지 포함
- [x] README 파일 작성

**위치**: `archive/paper_submission/`

### 2. 코드 제출 (클라우드 업로드) ✅

#### 제출 전 확인 사항
- [x] `.gitignore` 확인 (불필요한 파일 제외)
- [x] 환경 변수 파일 제외 (`.env`)
- [x] 로그 파일 제외 (`logs/`, `*.log`)
- [x] 데이터베이스 파일 제외 (`*.db`, `*.sqlite`)
- [x] 빌드 산출물 제외 (`dist/`, `build/`)
- [x] 캐시 파일 제외 (`__pycache__/`, `node_modules/`)
- [x] 대용량 데이터셋 제외 (`datasets/*.zip`, `datasets/tess/`)

#### 포함해야 할 파일
- [x] 소스 코드 (`.py`, `.tsx`, `.ts`)
- [x] 설정 파일 (`package.json`, `requirements.txt`, `vite.config.js`)
- [x] 문서 (`README.md`, `docs/`)
- [x] 테스트 파일 (`tests/`, `test_*.py`)

#### 제출 전 최종 확인
- [ ] 코드 정상 작동 확인
- [ ] README 파일 최신 상태 확인
- [ ] 환경 변수 예시 파일 포함 (`.env.example`)
- [ ] 의존성 파일 최신 상태 확인

---

## 📋 클라우드 업로드 준비

### 압축 전 확인
1. **불필요한 파일 제거**
   - `node_modules/` (npm install로 재설치 가능)
   - `__pycache__/` (자동 생성됨)
   - `dist/`, `build/` (빌드 산출물)
   - `*.log` (로그 파일)
   - `*.db`, `*.sqlite` (데이터베이스 파일)

2. **환경 변수 파일**
   - `.env` 파일은 제외
   - `.env.example` 파일 포함 (예시)

3. **대용량 파일**
   - `datasets/*.zip` 제외
   - `datasets/tess/` 제외 (대용량 데이터셋)

### 압축 방법

#### Windows (PowerShell)
```powershell
# 7-Zip 사용
7z a -xr!node_modules -xr!__pycache__ -xr!dist -xr!build -xr!*.log -xr!*.db submission.zip .

# 또는 Git Bash
tar -czf submission.tar.gz --exclude=node_modules --exclude=__pycache__ --exclude=dist --exclude=build --exclude='*.log' --exclude='*.db' .
```

#### Linux/Mac
```bash
tar -czf submission.tar.gz \
  --exclude=node_modules \
  --exclude=__pycache__ \
  --exclude=dist \
  --exclude=build \
  --exclude='*.log' \
  --exclude='*.db' \
  --exclude='.env' \
  .
```

---

## 📤 클라우드 업로드 플랫폼

### 추천 플랫폼
1. **GitHub**
   - 공개 저장소로 업로드
   - 버전 관리 가능
   - 이슈 트래킹

2. **Google Drive / Dropbox**
   - 압축 파일로 업로드
   - 간단한 공유

3. **GitLab**
   - GitHub와 유사
   - 프라이빗 저장소 지원

---

## ✅ 최종 확인

### 논문
- [x] DOCX 파일 최종 확인
- [x] 내용 오타 검토
- [x] 양식 준수 확인

### 코드
- [ ] 코드 정상 작동 확인
- [ ] README 파일 확인
- [ ] 의존성 파일 확인
- [ ] 환경 변수 예시 파일 포함

---

## 📝 제출 시 포함할 파일

### 논문
- `archive/paper_submission/ABC해커톤_논문_제출용.docx` (필수)

### 코드
- 전체 프로젝트 폴더 (압축 파일)
- 또는 Git 저장소 링크

---

**제출 준비 완료일**: 2026년 1월 16일  
**상태**: ✅ 준비 완료
