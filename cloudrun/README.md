# Cloud Run 배포 가이드

## 📋 사전 요구사항

- Google Cloud SDK (`gcloud`) 설치 및 인증
- Docker 설치 (로컬 빌드 테스트용)
- GCP 프로젝트 생성 및 Cloud Run API 활성화

## 🚀 배포 방법

### 1. GCP 인증 및 프로젝트 설정

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud config set run/region asia-northeast3
```

### 2. 환경 변수 설정

`env.yaml` 파일을 복사하여 실제 값으로 수정하세요:

```bash
cp env.yaml env.local.yaml
# env.local.yaml 편집
```

### 3. 배포 실행

```bash
chmod +x deploy_backend.sh
./deploy_backend.sh
```

또는 수동으로:

```bash
gcloud run deploy abc-backend \
  --source .. \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --env-vars-file env.yaml
```

## 📁 파일 설명

| 파일 | 설명 |
|------|------|
| `deploy_backend.sh` | 자동 배포 스크립트 |
| `env.yaml` | 환경 변수 템플릿 |
| `README.md` | 이 문서 |

## ⚙️ 환경 변수

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `PORT` | 서버 포트 | `8080` |
| `LOG_LEVEL` | 로그 레벨 | `INFO` |
| `CORS_ORIGINS` | CORS 허용 도메인 | `*` |

## 🔍 배포 확인

```bash
# 서비스 URL 확인
gcloud run services describe abc-backend --region asia-northeast3 --format='value(status.url)'

# 헬스체크
curl https://YOUR_SERVICE_URL/health
```

## ⚠️ 주의사항

- `env.local.yaml`은 `.gitignore`에 추가하여 민감 정보 유출 방지
- 프로덕션 배포 시 `--allow-unauthenticated` 대신 IAM 인증 고려
- Cloud SQL 연동 시 VPC Connector 설정 필요
