from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from auth import get_current_user
from generator import iniciar_generador, movimientos_por_usuario, saldos_por_usuario

app = FastAPI(
    title="Microservicio de Movimientos Bancarios",
    version="1.0.0",
    docs_url="/movimientos/swagger-ui/index.html",
    openapi_url="/movimientos/openapi.json"
)

@app.on_event("startup")
def startup_event():
    iniciar_generador()

@app.get("/movimientos", tags=["Movimientos"])
def listar_movimientos(user=Depends(get_current_user)):
    return movimientos_por_usuario.get(user["id"], [])

@app.get("/movimientos/saldo", tags=["Resumen"])
def obtener_saldo(user=Depends(get_current_user)):
    data = saldos_por_usuario.get(user["id"], {"saldo": 0.0})
    return {"saldo_actual": round(data["saldo"], 2)}

@app.get("/movimientos/ingresos", tags=["Resumen"])
def obtener_ingresos(user=Depends(get_current_user)):
    data = saldos_por_usuario.get(user["id"], {"ingresos": 0.0})
    return {"total_ingresos": round(data["ingresos"], 2)}

@app.get("/movimientos/egresos", tags=["Resumen"])
def obtener_egresos(user=Depends(get_current_user)):
    data = saldos_por_usuario.get(user["id"], {"egresos": 0.0})
    return {"total_egresos": round(data["egresos"], 2)}

@app.get("/movimientos/swagger", include_in_schema=False)
def redirigir_swagger():
    return RedirectResponse(url="/movimientos/swagger-ui/index.html")

@app.get("/movimientos/health", tags=["Estado"])
def health():
    return {"status": "ok"}