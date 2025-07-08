#!/bin/bash

# Script para testear funciones OCI en el proyecto agendar-ms
# Requiere: OCI CLI, jq, curl

# ======= EDITAR ESTAS VARIABLES =======
FN_APP_NAME="agendar-ms-fn"
FN_CONTEXT="us-sanjose-1"
OCI_PROFILE="DEFAULT"
API_URL="https://functions.us-sanjose-1.oci.oraclecloud.com"
COMPARTMENT_OCID="ocid1.compartment.oc1..aaaaaaaal7vn7wsy3qgizklrlfgo2vllfta3wkqlnfkvykoroite3lzxbnna"
EXPECTED_API_URL="https://functions.us-sanjose-1.oci.oraclecloud.com"
# ======================================


# Crear contexto si no existe

fn use context default
fn list context | awk 'NR>1 && $2 != "default" {print $1}' | while read ctx; do   echo "Deleting context: $ctx";   fn delete context "$ctx"; done
echo -e "${GREEN}✅ Borrado de contextos completado"

if ! fn list context | grep -wq "$FN_CONTEXT"; then
    fn create context "$FN_CONTEXT" --provider oracle    
fi
echo -e "${GREEN}✅ Contexto ${FN_CONTEXT} creado"

fn use context "$FN_CONTEXT"
fn update context oracle.region us-sanjose-1
fn update context api-url "$EXPECTED_API_URL"
fn update context oracle.compartment-id "$COMPARTMENT_OCID"
fn update context registry "$REGION_KEY.ocir.io/$OCIR_NS"

echo -e "${GREEN}✅ Setteo de Contexto ${FN_CONTEXT} OK"


#Listar functions en app
echo "🔍 Listando funciones en la app $FN_APP_NAME..."

FUNCS=$(fn list functions $FN_APP_NAME | awk 'NR>1 {print $1}')

if [ -z "$FUNCS" ]; then
    echo "❌ No se encontraron funciones en la app $FN_APP_NAME."
    exit 1
fi

echo "✅ Funciones encontradas:  $FUNCS"

# Mock payloads por función
get_mock_body() {
    case "$1" in
        crear-reserva)
            echo '{"sucursal": "Sucursal Central", "fecha": "2025-07-08", "hora": "10:00:00"}'
            ;;
        obtener-reserva)
            echo '{"reserva_id": 1}'
            ;;
        actualizar-reserva)
            echo '{"reserva_id": 2,"sucursal": "Sucursal Actualizada","fecha": "2025-07-08","hora": "15:30:00"}'
            ;;
        eliminar-reserva)
            echo '{"reserva_id": 1}'
            ;;
        listar-reservas)
            echo '{}'
            ;;
        *)
            echo '{}'
            ;;
    esac
}


# Test individual para cada función
test_function() {
    FUNC_NAME="$1"
    MOCK_BODY=$(get_mock_body "$FUNC_NAME")
    FUNC_ID=$(oci fn function list --application-id $(oci fn application list --compartment-id $COMPARTMENT_OCID --query "data[?\"display-name\"=='$FN_APP_NAME'].id | [0]" --raw-output --profile $OCI_PROFILE) --query "data[?\"display-name\"=='$FUNC_NAME'].id | [0]" --raw-output --profile $OCI_PROFILE)
    if [ -z "$FUNC_ID" ]; then
        echo "❌ No se encontró el OCID de la función $FUNC_NAME."
        return
    fi
    echo -e "\n🚦 Testeando función: $FUNC_NAME"
    echo "OCID: $FUNC_ID"
    echo "Invocando función $FUNC_NAME con body: $MOCK_BODY"
    echo "$MOCK_BODY" > /tmp/fn-mock-body.json
    HTTP_STATUS=$(oci fn function invoke --function-id $FUNC_ID --file /tmp/fn-mock-body.json --body "$MOCK_BODY" --full-response --profile $OCI_PROFILE | jq -r '.status')
    RESP=$(oci fn function invoke --function-id $FUNC_ID --file /tmp/fn-mock-body.json --body "$MOCK_BODY" --query 'data' --raw-output --profile $OCI_PROFILE| base64 -d)
    echo "Respuesta: $RESP"
    echo "HTTP Status: $HTTP_STATUS"
}

# Llama a test_function para cada función encontrada
for FUNC in $FUNCS; do
    test_function "$FUNC"
done

echo -e "\n🏁 Test de funciones finalizado."
