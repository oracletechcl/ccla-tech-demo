#!/usr/bin/env bash
set -euo pipefail

# Usage: ./build-and-deploy.sh <ocir-namespace> <repo-name> <region> <tag>
# Example: ./build-and-deploy.sh axaxxx base-app phx v1

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <ocir-namespace> <repo-name> <region> <tag>"
  exit 1
fi

NAMESPACE="$1"
REPO="$2"
REGION="$3"
TAG="$4"

IMAGE="$REGION.ocir.io/$NAMESPACE/$REPO:$TAG"

# Build Docker image

echo "[1/3] Building Docker image: $IMAGE"
docker build -t "$IMAGE" .

# Login to OCIR

echo "[2/3] Logging in to OCIR: $REGION.ocir.io"
echo "Enter your OCIR auth token (not your password):"
docker login "$REGION.ocir.io" -u "$NAMESPACE/$(whoami)" --password-stdin

# Push Docker image

echo "[3/3] Pushing Docker image to OCIR"
docker push "$IMAGE"

echo "Image pushed: $IMAGE"
