#!/bin/bash
# Cloud Run 백엔드 배포 스크립트

set -e

# 기본값 설정
PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project)}"
REGION="${GCP_REGION:-asia-northeast3}"
SERVICE_NAME="${SERVICE_NAME:-abc-backend}"

echo "🚀 Cloud Run 배포 시작"
echo "   프로젝트: $PROJECT_ID"
echo "   리전: $REGION"
echo "   서비스: $SERVICE_NAME"

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.."

# Cloud Run 배포
gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --allow-unauthenticated \
  --env-vars-file cloudrun/env.yaml \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300

echo "✅ 배포 완료!"
echo "📍 서비스 URL:"
gcloud run services describe "$SERVICE_NAME" \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --format='value(status.url)'
