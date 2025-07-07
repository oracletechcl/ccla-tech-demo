#!/bin/bash

# ---------- CONFIGURACIÓN ----------
DOCKERHUB_USERNAME="dralquinta"
REPO_NAME="movimientos-ms"
TAG="v1"
FULL_IMAGE="${DOCKERHUB_USERNAME}/${REPO_NAME}:${TAG}"

# ---------- CONSTRUCCIÓN ----------
echo "🔧 Building Docker Image..."
if ! docker build -t ${FULL_IMAGE} .; then
    echo "❌ Error: Failure in Docker image construction. No further actions will be done. Fix and retry"
    exit 1
fi

# ---------- PUSH ----------
echo "🚀 Uploading image to Docker Hub..."
if ! docker push ${FULL_IMAGE}; then
    echo "❌ Error: Failure in docker push. Fix and retry."
    exit 1
fi

echo "✅ Imagen subida correctamente: ${FULL_IMAGE}"

# ---------- REINICIAR DEPLOYMENT ----------
echo "♻️  Reiniciando deployment"
if ! kubectl rollout restart deployment movimientos-ms -n movimientos-ms-namespace; then
    echo "⚠️  Warning: Deployment restart failed. Check status with kubectl or k9s."
    exit 1
fi

echo "🏁 Build and push completed successfully."