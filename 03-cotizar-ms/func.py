from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.orm import sessionmaker
from models import metadata, reserva
from auth import get_current_user
import config
import datetime

# --- Inicialización FastAPI ---
app = FastAPI(
    title="Cotizador de Créditos",
    version="1.0.0",
    root_path="/cotizar",
    docs_url="/cotizar/swagger-ui/index.html",
    openapi_url="/cotizar/openapi.json",
    redirect_slashes=True
)

# --- Middleware CORS ---
origins = [
    "https://portalbancario.alquinta.xyz",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Conexión DB ---
engine = create_engine(config.DATABASE_URL)
metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------- Esquemas --------
class Reserva(BaseModel):
    id: int
    usuario_id: int
    sucursal: str
    fecha: datetime.date
    hora: datetime.time
    created_at: datetime.datetime

class ReservaCreate(BaseModel):
    sucursal: str
    fecha: datetime.date
    hora: datetime.time

# -------- Dependencia DB --------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------- RUTA CORS MANUAL (para compatibilidad con API Gateway o Functions) --------
@app.options("/cotizar", tags=["CORS"])
def options_cotizar():
    return JSONResponse(
        content={},
        status_code=204,
        headers={
            "Access-Control-Allow-Origin": "https://portalbancario.alquinta.xyz",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )

# -------- ENDPOINTS --------

@app.post("/cotizar", response_model=Reserva, tags=["Cotización"])
def crear_cotizacion(
    reserva_in: ReservaCreate,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    now = datetime.datetime.utcnow()
    ins = reserva.insert().values(
        usuario_id=user["id"],
        sucursal=reserva_in.sucursal,
        fecha=reserva_in.fecha,
        hora=reserva_in.hora,
        created_at=now
    )
    result = db.execute(ins)
    db.commit()
    reserva_id = result.lastrowid
    return {
        **reserva_in.dict(),
        "id": reserva_id,
        "usuario_id": user["id"],
        "created_at": now
    }

@app.get("/cotizar", response_model=List[Reserva], tags=["Cotización"])
def listar_cotizaciones(
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    result = db.execute(select(reserva).where(reserva.c.usuario_id == user["id"]))
    return [dict(row._mapping) for row in result]

@app.get("/cotizar/{reserva_id}", response_model=Reserva, tags=["Cotización"])
def obtener_cotizacion(
    reserva_id: int,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    result = db.execute(
        select(reserva).where(
            (reserva.c.id == reserva_id) & (reserva.c.usuario_id == user["id"])
        )
    ).first()
    if result:
        return dict(result._mapping)
    raise HTTPException(status_code=404, detail="Cotización no encontrada")

@app.put("/cotizar/{reserva_id}", response_model=Reserva, tags=["Cotización"])
def actualizar_cotizacion(
    reserva_id: int,
    reserva_in: ReservaCreate,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    upd = update(reserva).where(
        (reserva.c.id == reserva_id) & (reserva.c.usuario_id == user["id"])
    ).values(
        sucursal=reserva_in.sucursal,
        fecha=reserva_in.fecha,
        hora=reserva_in.hora
    )
    result = db.execute(upd)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    r = db.execute(select(reserva).where(reserva.c.id == reserva_id)).first()
    return dict(r._mapping)

@app.delete("/cotizar/{reserva_id}", tags=["Cotización"])
def eliminar_cotizacion(
    reserva_id: int,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    result = db.execute(
        delete(reserva).where(
            (reserva.c.id == reserva_id) & (reserva.c.usuario_id == user["id"])
        )
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    return {"detail": "Cotización eliminada"}

# -------- ENDPOINTS INFORMACION --------

@app.get("/cotizar/info", tags=["Estado del Servicio"])
def cotizar_info():
    return {"message": "Cotizador activo"}

@app.get("/cotizar/swagger", include_in_schema=False)
def redirigir_a_swagger():
    return RedirectResponse(url="/cotizar/swagger-ui/index.html")

@app.get("/cotizar/health", tags=["Estado del Servicio"])
def health():
    return {"status": "ok"}