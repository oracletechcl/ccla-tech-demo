from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from auth import get_current_user
from generator import generar_si_es_necesario, movimientos_por_usuario, cupo_por_usuario, ingresos_por_usuario, egresos_por_usuario

app = FastAPI(
    title="Microservicio de Movimientos de Tarjeta de Crédito",
    version="1.0.0",
    docs_url="/cc-movimientos/swagger-ui/index.html",
    openapi_url="/cc-movimientos/openapi.json"
)

@app.get("/cc-movimientos", tags=["Movimientos"])
def listar_movimientos(user=Depends(get_current_user)):
    uid = user["id"]
    generar_si_es_necesario(uid)
    return movimientos_por_usuario[uid]

@app.get("/cc-movimientos/cupo", tags=["Resumen"])
def obtener_cupo(user=Depends(get_current_user)):
    data = cupo_por_usuario.get(user["id"], 700000)
    return {"cupo_disponible": round(data, 2)}

@app.get("/cc-movimientos/ingresos", tags=["Resumen"])
def obtener_ingresos(user=Depends(get_current_user)):
    data = ingresos_por_usuario.get(user["id"], 0.0)
    return {"total_pagos": round(data, 2)}

@app.get("/cc-movimientos/egresos", tags=["Resumen"])
def obtener_egresos(user=Depends(get_current_user)):
    data = egresos_por_usuario.get(user["id"], 0.0)
    return {"total_gastos": round(data, 2)}

@app.get("/cc-movimientos/swagger", include_in_schema=False)
def redirigir_swagger():
    return RedirectResponse(url="/cc-movimientos/swagger-ui/index.html")

@app.get("/cc-movimientos/health", tags=["Estado"])
def health():
    return {"status": "ok"}