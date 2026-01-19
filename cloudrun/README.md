# Cloud Run 배포 가이드 (백엔드)

이 가이드는 FastAPI 백엔드를 Cloud Run에 배포하는 방법을 설명합니다.

## 사전 준비
- gcloud CLI 설치
- GCP 프로젝트 생성
- 결제 계정 연결
 - `gcloud auth login` 또는 서비스 계정 인증

## 환경 변수 설정
`cloudrun/env.yaml`을 수정해 실제 값으로 변경하세요.

필수/권장 항목:
- `CORS_ORIGINS`: 프론트엔드 도메인 목록
- `LOG_LEVEL`: INFO 권장
- `PORT`: 8080 (Cloud Run 기본)
- `DB_PATH`: `/tmp/user_profiles.db` 권장 (임시 저장)

## 배포 (권장 스크립트)
```bash
bash cloudrun/deploy_backend.sh <gcp-project-id> [region] [service-name]
```

예시:
```bash
bash cloudrun/deploy_backend.sh my-gcp-project asia-northeast3 nexus-backend
```

## 참고 사항
- SQLite는 컨테이너 파일시스템에 저장되므로 **재시작 시 데이터가 유실**됩니다.
- 영구 저장이 필요하면 Cloud SQL 또는 Firestore를 사용하세요.
