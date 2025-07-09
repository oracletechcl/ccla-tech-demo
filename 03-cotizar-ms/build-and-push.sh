#!/bin/bash

# ---------- CONFIGURACIÓN ----------
DOCKERHUB_USERNAME="dralquinta"
REPO_NAME="cotizar-ms"
TAG="v1"
DOCKER_IMAGE="${DOCKERHUB_USERNAME}/${REPO_NAME}:${TAG}"

COMPARTMENT_OCID="ocid1.compartment.oc1..aaaaaaaal7vn7wsy3qgizklrlfgo2vllfta3wkqlnfkvykoroite3lzxbnna"
SUBNET_OCID="ocid1.subnet.oc1.us-sanjose-1.aaaaaaaaydads5e35xkxhkiajee77j5qlqtpzd77czjwonncahblx6pvrdza" # public - for testing
#SUBNET_OCID="ocid1.subnet.oc1.us-sanjose-1.aaaaaaaa23am2rdz7db7ty5btfdndlah2tusxbv52jb3sdaehrghwdbhv7ba" #private
CONTAINER_NAME="cotizar-ms"
SHAPE="CI.Standard.E4.Flex"

# --------- CHEQUEO DE VARIABLES ----------
for v in DOCKER_IMAGE CONTAINER_NAME COMPARTMENT_OCID SUBNET_OCID SHAPE; do
  if [ -z "${!v}" ]; then
    echo "❌ Error: Variable $v está vacía. Abortando."
    exit 1
  fi
done

# ---------- BUILD IMAGE ----------
echo "🔧 Building Docker Image..."
if ! docker build -t "$DOCKER_IMAGE" .; then
    echo "❌ Error: Failure in Docker image construction. No further actions will be done. Fix and retry"
    exit 1
fi

# ---------- PUSH ----------
echo "🚀 Uploading image to Docker Hub..."
if ! docker push "$DOCKER_IMAGE"; then
    echo "❌ Error: Failure in docker push. Fix and retry."
    exit 1
fi
echo "✅ Imagen subida correctamente: ${DOCKER_IMAGE}"


# ------------ ELIMINAR INSTANCIAS PREVIAS Y FAILED ------------
echo "🔎 Buscando instancias previas y FAILED de $CONTAINER_NAME..."

# Elimina instancias activas y en estado FAILED
INSTANCE_IDS=$(oci container-instances container-instance list \
  --compartment-id "$COMPARTMENT_OCID" \
  --query "data.items[?\"display-name\"=='$CONTAINER_NAME' && (\"lifecycle-state\"!='DELETED')].id" \
  --raw-output)

if [[ -n "$INSTANCE_IDS" ]]; then
  echo "$INSTANCE_IDS" | while IFS= read -r CI_ID; do
    CLEAN_ID=$(echo "$CI_ID" | sed 's/[", ]//g')
    if [[ "$CLEAN_ID" =~ ^ocid1\.computecontainerinstance\. ]]; then
      echo "🗑️  Eliminando Container Instance previa o FAILED ($CLEAN_ID)..."
      oci container-instances container-instance delete --container-instance-id "$CLEAN_ID" --force &
    fi
  done
  echo "⏳ Borrado de instancias solicitado (no se espera confirmación, puedes crear inmediatamente)"
else
  echo "🟢 No hay instancias previas ni FAILED de $CONTAINER_NAME"
fi

# ------------ CREAR NUEVA INSTANCIA ------------
echo "🚀 Creando nueva Container Instance: $CONTAINER_NAME"
AVAILABILITY_DOMAIN=$(oci iam availability-domain list --compartment-id "$COMPARTMENT_OCID" --query "data[0].name" --raw-output)

SHAPE_CONFIG='{"ocpus": 2, "memoryInGBs": 16}'

oci container-instances container-instance create \
  --compartment-id "$COMPARTMENT_OCID" \
  --availability-domain "$AVAILABILITY_DOMAIN" \
  --shape "$SHAPE" \
  --shape-config "$SHAPE_CONFIG" \
  --display-name "$CONTAINER_NAME" \
  --containers '[
  {
    "imageUrl": "'"$DOCKER_IMAGE"'",
    "command": ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"],
    "name": "'"$CONTAINER_NAME"'",
    "portMappings": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]
  }
]' \
  --vnics '[{"subnetId": "'"$SUBNET_OCID"'", "assignPublicIp": true}]' \
  --wait-for-state SUCCEEDED \
  --wait-for-state FAILED

echo "🏁 OCI Container Instance deployment triggered. Revisa la OCI Console para la IP pública."