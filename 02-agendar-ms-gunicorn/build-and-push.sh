#!/bin/bash

# ======= EDITAR ESTAS VARIABLES =======
APP_NAME="agendar-ms-fn"
FUNC_NAME="agendar-ms"
FN_CONTEXT="us-sanjose-1"
OCI_COMPARTMENT_OCID="ocid1.compartment.oc1..aaaaaaaal7vn7wsy3qgizklrlfgo2vllfta3wkqlnfkvykoroite3lzxbnna"
REGION_KEY="sjc"
OCIR_NS="idi1o0a010nx"
OCI_USERNAME="oracleidentitycloudservice/denny.alquinta@oracle.com"
OCI_AUTH_TOKEN="T1R;m:O3onysya}OdnaI"
DOCKER_IMAGE="$REGION_KEY.ocir.io/$OCIR_NS/$FUNC_NAME:latest"
EXPECTED_API_URL="https://functions.us-sanjose-1.oci.oraclecloud.com"
# =======================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Verifica autenticación OCI CLI
if ! oci os ns get &>/dev/null; then
    echo -e "${RED}ERROR: No estás autenticado en OCI CLI. Revisa tu configuración y credenciales.${NC}"
    exit 1
else
    echo -e "${GREEN}OK: OCI CLI está autenticado.${NC}"
fi

# 2. Crear contexto si no existe
if ! fn list context | grep -wq "$FN_CONTEXT"; then
    echo "Contexto '$FN_CONTEXT' no existe. Creando..."
    fn create context "$FN_CONTEXT" --provider oracle
else
    echo "Contexto '$FN_CONTEXT' ya existe y está sano."
fi

# Setea la región en el contexto si no está seteada correctamente
CURRENT_REGION=$(fn inspect context | grep 'oracle.region' | awk '{print $2}')
if [[ "$CURRENT_REGION" != "us-sanjose-1" ]]; then
    fn update context oracle.region us-sanjose-1
    echo "Contexto '$FN_CONTEXT' actualizado con region us-sanjose-1."
fi

# Setea el api-url de Functions (clave para Fn CLI)
CURRENT_API_URL=$(fn inspect context | grep "api-url" | awk '{print $2}' || true)
if [[ "$CURRENT_API_URL" != "$EXPECTED_API_URL" ]]; then
    fn update context api-url "$EXPECTED_API_URL"
    echo "api-url del contexto seteado a $EXPECTED_API_URL"
else
    echo "api-url ya está seteado correctamente."
fi

# Usar contexto si no está activo
CURRENT_CONTEXT=$(fn list context | grep '*' | awk '{print $2}')
if [[ "$CURRENT_CONTEXT" != "$FN_CONTEXT" ]]; then
    fn use context "$FN_CONTEXT" || true
    echo "Contexto cambiado a '$FN_CONTEXT'."
else
    echo "Ya estás usando el contexto '$FN_CONTEXT'."
fi

# 3. Set compartment-id (idempotente)
fn update context oracle.compartment-id "$OCI_COMPARTMENT_OCID"
echo "Contexto '$FN_CONTEXT' actualizado con compartment OCID."

# 4. Setea Registry si no está definido
CURRENT_REGISTRY=$(fn inspect context | grep "registry" | awk '{print $2}' || true)
EXPECTED_REGISTRY="$REGION_KEY.ocir.io/$OCIR_NS"
if [[ "$CURRENT_REGISTRY" != "$EXPECTED_REGISTRY" ]]; then
    fn update context registry "$EXPECTED_REGISTRY"
    echo "Registry actualizado: $EXPECTED_REGISTRY"
else
    echo "Registry ya está seteado correctamente."
fi

# 5. Docker login a OCIR (idempotente)
docker logout "$REGION_KEY.ocir.io" 2>/dev/null || true
sleep 1
echo "Haciendo login a OCIR..."
if ! echo "$OCI_AUTH_TOKEN" | docker login "$REGION_KEY.ocir.io" -u "$OCIR_NS/$OCI_USERNAME" --password-stdin; then
    echo "ERROR: Falló el login a OCIR. Revisa tu token, usuario y namespace."
    exit 1
fi

# 6. Verifica que exista func.yaml
if [[ ! -f func.yaml ]]; then
    fn init --runtime python
    echo "fn init ejecutado (func.yaml creado)."
else
    echo "func.yaml ya existe."
fi

# 7. Build y deploy function (Fn CLI se encarga del push)
echo "Construyendo y desplegando función Fn..."
fn -v deploy --app "$APP_NAME"

echo -e "${GREEN}✅ Build & deploy completo para Oracle Functions con Fn CLI.${NC}"