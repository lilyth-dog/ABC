# 데이터셋 (Datasets)

이 폴더에는 프로젝트에 필요한 대용량 데이터셋 파일들이 포함되어 있습니다.

## 📦 포함된 데이터셋

### 1. TESS (Toronto Emotional Speech Set)
- **파일**: `toronto-emotional-speech-set-tess.zip` (427.79 MB)
- **용도**: 감정 인식 및 오디오 분석
- **다운로드**: [TESS 공식 사이트](https://tspace.library.utoronto.ca/handle/1807/24487)
- **설명**: 다양한 감정 상태(angry, happy, sad, neutral 등)의 음성 데이터셋

### 2. Workout Fitness Video
- **파일**: `workoutfitness-video.zip` (330.12 MB)
- **용도**: 모션 분석 및 바이오시그널 통합
- **설명**: 피트니스 동작 분석을 위한 비디오 데이터셋

## ⚠️ 중요 사항

이 파일들은 **GitHub에 포함되지 않습니다** (100MB 제한).

### 로컬에서 사용하는 방법

1. **데이터셋 다운로드**:
   - TESS: 위 링크에서 직접 다운로드
   - Workout Fitness Video: 필요시 별도 제공

2. **압축 해제**:
   ```bash
   # TESS 데이터셋
   unzip toronto-emotional-speech-set-tess.zip -d tess/
   
   # Workout Fitness Video
   unzip workoutfitness-video.zip
   ```

3. **폴더 구조 확인**:
   ```
   datasets/
   ├── tess/
   │   └── TESS Toronto emotional speech set data/
   │       ├── YAF_neutral/
   │       ├── YAF_happy/
   │       └── ...
   └── workoutfitness-video/
   ```

## 🔄 Git LFS 사용 (선택사항)

대용량 파일을 Git에 포함하려면 Git LFS를 사용할 수 있습니다:

```bash
# Git LFS 설치
git lfs install

# 큰 파일 추적
git lfs track "*.zip"
git lfs track "datasets/**"

# 커밋
git add .gitattributes
git add datasets/
git commit -m "Add datasets with Git LFS"
git push
```

## 📝 대안 방법

### 방법 1: 클라우드 스토리지
- Google Drive, Dropbox, OneDrive 등에 업로드
- README에 다운로드 링크 추가

### 방법 2: 별도 저장소
- 데이터셋 전용 GitHub 저장소 생성
- Git LFS 또는 Releases 기능 사용

### 방법 3: 데이터셋 제공자 링크
- 공식 다운로드 링크를 README에 명시
- 사용자가 직접 다운로드하도록 안내

## 🚀 빠른 시작

프로젝트를 처음 클론한 경우:

```bash
# 1. 저장소 클론
git clone https://github.com/lilyth-dog/ABC.git
cd ABC

# 2. 데이터셋 다운로드 (필요시)
# TESS: https://tspace.library.utoronto.ca/handle/1807/24487
# 또는 팀 내부에서 공유된 링크 사용

# 3. 데이터셋 압축 해제
cd datasets
unzip toronto-emotional-speech-set-tess.zip
unzip workoutfitness-video.zip
```

## 📌 참고

- 데이터셋 파일은 `.gitignore`에 포함되어 있습니다
- 로컬 개발 환경에서만 사용됩니다
- 프로덕션 배포 시에는 별도 스토리지에 저장하는 것을 권장합니다
