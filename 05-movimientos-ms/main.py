from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from auth import get_current_user
from generator import (
    generar_lote_de_movimientos,
    obtener_movimientos,
    obtener_saldo,
    obtener_resumen
)
from models import Movimiento
from typing import List

app = FastAPI(
    title="Microservicio de Movimientos Bancarios",
    version="1.0.0",
    docs_url="/movimientos/swagger-ui/index.html",
    openapi_url="/movimientos/openapi.json"
)

@app.get("/movimientos", response_model=List[Movimiento], tags=["Movimientos"])
def listar_movimientos(user=Depends(get_current_user)):
    user_id = str(user.get("id") or user.get("sub"))
    generar_lote_de_movimientos(user_id, cantidad=5)
    return obtener_movimientos(user_id)

@app.get("/movimientos/saldo", tags=["Resumen"])
def saldo(user=Depends(get_current_user)):
    user_id = str(user.get("id") or user.get("sub"))
    return {"saldo_actual": obtener_saldo(user_id)}

@app.get("/movimientos/resumen", tags=["Resumen"])
def resumen(user=Depends(get_current_user)):
    user_id = str(user.get("id") or user.get("sub"))
    return obtener_resumen(user_id)

@app.get("/movimientos/swagger", include_in_schema=False)
def redirigir_swagger():
    return RedirectResponse(url="/movimientos/swagger-ui/index.html")

@app.get("/movimientos/health", tags=["Estado"])
def health():
    return {"status": "ok"}