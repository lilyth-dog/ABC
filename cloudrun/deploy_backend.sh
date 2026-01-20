#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID=${1:-}
REGION=${2:-asia-northeast3}
SERVICE_NAME=${3:-nexus-backend}

if [ -z "$PROJECT_ID" ]; then
  echo "Usage: $0 <gcp-project-id> [region] [service-name]" >&2
  exit 1
fi

IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

gcloud config set project "$PROJECT_ID"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
gcloud builds submit --tag "$IMAGE" .
gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE" \
  --region "$REGION" \
  --allow-unauthenticated \
  --port 8080 \
  --env-vars-file cloudrun/env.yaml
