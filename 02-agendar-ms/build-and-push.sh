#!/bin/bash

# ======= VARIABLES DE CONFIGURACIÓN =======
APP_NAME="agendar-ms-fn"
FN_CONTEXT="us-sanjose-1"
OCI_COMPARTMENT_OCID="ocid1.compartment.oc1..aaaaaaaal7vn7wsy3qgizklrlfgo2vllfta3wkqlnfkvykoroite3lzxbnna"
SUBNET_OCID="ocid1.subnet.oc1.us-sanjose-1.aaaaaaaa23am2rdz7db7ty5btfdndlah2tusxbv52jb3sdaehrghwdbhv7ba"
REGION_KEY="sjc"
OCIR_NS="idi1o0a010nx"
OCI_USERNAME="oracleidentitycloudservice/denny.alquinta@oracle.com"
OCI_AUTH_TOKEN="T1R;m:O3onysya}OdnaI"
EXPECTED_API_URL="https://functions.us-sanjose-1.oci.oraclecloud.com"
# ===========================================

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "🔧 Validando autenticación y contexto..."

# Autenticación OCI CLI
if ! oci os ns get &>/dev/null; then
    echo -e "${RED}ERROR: No estás autenticado en OCI CLI.${NC}"
    exit 1
else
    echo -e "${GREEN}✅ OCI CLI autenticado.${NC}"
fi

# Setear y limpiar contexto
fn use context default
fn list context | awk 'NR>1 && $2 != "default" {print $1}' | while read ctx; do
    fn delete context "$ctx"
done
echo -e "${GREEN}✅ Contextos anteriores eliminados${NC}"

# Crear contexto si no existe
if ! fn list context | grep -wq "$FN_CONTEXT"; then
    fn create context "$FN_CONTEXT" --provider oracle    
fi
echo -e "${GREEN}✅ Contexto ${FN_CONTEXT} creado o ya existente${NC}"

fn use context "$FN_CONTEXT"
fn update context oracle.region us-sanjose-1
fn update context api-url "$EXPECTED_API_URL"
fn update context oracle.compartment-id "$OCI_COMPARTMENT_OCID"
fn update context registry "$REGION_KEY.ocir.io/$OCIR_NS"

echo -e "${GREEN}✅ Contexto configurado correctamente${NC}"

# Login a OCIR
docker logout "$REGION_KEY.ocir.io" 2>/dev/null || true
echo "$OCI_AUTH_TOKEN" | docker login "$REGION_KEY.ocir.io" -u "$OCIR_NS/$OCI_USERNAME" --password-stdin
echo -e "${GREEN}✅ Loggeado en OCIR${NC}"

# Crear aplicación si no existe
if ! fn list apps | grep -wq "$APP_NAME"; then
    echo "📦 Creando aplicación '$APP_NAME'..."
    echo "[\"$SUBNET_OCID\"]" > subnet-ids.json
    application_id=$(oci fn application create \
        --compartment-id "$OCI_COMPARTMENT_OCID" \
        --display-name "$APP_NAME" \
        --subnet-ids file://subnet-ids.json \
        --query data.id --raw-output)
    echo "✅ Application creada con OCID: $application_id"
    rm subnet-ids.json
else
    echo "📦 Aplicación '$APP_NAME' ya existe."
fi

# Desplegar cada función con su propio shared/
for dir in */; do
    if [[ "$dir" == "shared/" ]]; then
        continue
    fi
    if [[ -f "$dir/func.yaml" ]]; then
        FUNC_DIR=${dir%/}
        echo -e "\n🚀 Desplegando función: ${GREEN}$FUNC_DIR${NC}"

        cd "$FUNC_DIR"

        # Validar requirements.txt
        if ! grep -q "fdk" requirements.txt; then
            echo "fdk" >> requirements.txt
        fi
        if ! grep -q "requests" requirements.txt; then
            echo "requests" >> requirements.txt
        fi

        # Validar shared/__init__.py
        if [[ ! -f "shared/__init__.py" ]]; then
            touch shared/__init__.py
        fi

        # Despliegue
        if fn -v deploy --app "$APP_NAME" --no-bump; then
            echo -e "${GREEN}✅ Función '$FUNC_DIR' desplegada exitosamente${NC}"
        else
            echo -e "${RED}❌ Error al desplegar función '$FUNC_DIR'${NC}"
        fi

        cd ..
    else
        echo -e "${RED}⚠️  El directorio '$dir' no contiene func.yaml. Se omite.${NC}"
    fi
done

echo -e "\n${GREEN}🏁 Todas las funciones fueron construidas y desplegadas exitosamente.${NC}"