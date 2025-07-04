#!/bin/bash

# ---------- CONFIGURACIÓN ----------
DOCKERHUB_USERNAME="dralquinta"   # 🔁 Reemplaza con tu usuario Docker Hub
REPO_NAME="bank-landing"
TAG="v1"
FULL_IMAGE="${DOCKERHUB_USERNAME}/${REPO_NAME}:${TAG}"


# ---------- CONSTRUCCIÓN ----------
echo "🔧 Construyendo imagen Docker..."
docker build -t ${FULL_IMAGE} .

# ---------- PUSH ----------
echo "🚀 Subiendo imagen a Docker Hub..."
docker push ${FULL_IMAGE}

echo "✅ Imagen subida correctamente: ${FULL_IMAGE}"

echo "Reiniciando deployment"
kubectl rollout restart deployment springbank-portal
