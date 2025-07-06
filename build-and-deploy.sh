#!/bin/bash
set -e  # Exit on any error

# ---------- CONFIGURACIÓN ----------
DOCKERHUB_USERNAME="dralquinta"
REPO_NAME="bank-landing"
TAG="v1"
FULL_IMAGE="${DOCKERHUB_USERNAME}/${REPO_NAME}:${TAG}"

# ---------- LOGIN ----------
echo "🔐 Iniciando sesión en Docker Hub..."
docker login -u "${DOCKERHUB_USERNAME}"

# ---------- BUILD MAVEN ----------
echo "⚙️  Construyendo artefacto Maven..."
if [[ -x "./mvnw" ]]; then
    ./mvnw clean package -DskipTests
else
    mvn clean package -DskipTests
fi

echo "✅ Build Maven OK"

# ---------- DOCKER BUILD ----------
echo "🔧 Construyendo imagen Docker..."
docker build -t "${FULL_IMAGE}" .
echo "✅ Imagen Docker creada correctamente"

# ---------- PUSH ----------
echo "🚀 Subiendo imagen a Docker Hub..."
docker push "${FULL_IMAGE}"
echo "✅ Imagen subida correctamente: ${FULL_IMAGE}"
