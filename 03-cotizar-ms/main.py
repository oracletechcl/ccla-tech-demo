from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.orm import sessionmaker
from models import metadata, cotizacion
from auth import get_current_user
import config
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Cotizacion CRUD API",
    version="1.0.0",
    docs_url="/swagger-ui/index.html",
    openapi_url="/openapi.json",
    redirect_slashes=True
)

# Database setup
engine = create_engine(config.DATABASE_URL)
metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Pydantic Schemas
class CotizacionBase(BaseModel):
    usuario_id: int
    producto_id: Optional[int] = None
    monto: float
    plazo_meses: int
    tasa_anual: float
    cuota_mensual: float
    total_pagado: float
    cae: float
    created_at: Optional[datetime.datetime] = None

class CotizacionCreate(CotizacionBase):
    pass

class Cotizacion(CotizacionBase):
    id: int

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Endpoints
@app.post("/cotizacion", response_model=Cotizacion, tags=["Cotizacion"])
def create_cotizacion(
    cotizacion_in: CotizacionCreate,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    now = datetime.datetime.utcnow()
    ins = cotizacion.insert().values(
        usuario_id=user["id"],
        producto_id=cotizacion_in.producto_id,
        monto=cotizacion_in.monto,
        plazo_meses=cotizacion_in.plazo_meses,
        tasa_anual=cotizacion_in.tasa_anual,
        cuota_mensual=cotizacion_in.cuota_mensual,
        total_pagado=cotizacion_in.total_pagado,
        cae=cotizacion_in.cae,
        created_at=now
    )
    result = db.execute(ins)
    db.commit()
    cotizacion_id = result.lastrowid
    return Cotizacion(id=cotizacion_id, created_at=now, **cotizacion_in.dict())

@app.get("/cotizacion", response_model=List[Cotizacion], tags=["Cotizacion"])
def list_cotizaciones(user=Depends(get_current_user), db=Depends(get_db)):
    result = db.execute(select(cotizacion).where(cotizacion.c.usuario_id == user["id"]))
    return [Cotizacion(**dict(row._mapping)) for row in result]

@app.get("/cotizacion/{cotizacion_id}", response_model=Cotizacion, tags=["Cotizacion"])
def get_cotizacion(cotizacion_id: int, user=Depends(get_current_user), db=Depends(get_db)):
    result = db.execute(
        select(cotizacion).where(
            (cotizacion.c.id == cotizacion_id) & (cotizacion.c.usuario_id == user["id"])
        )
    ).first()
    if result:
        return Cotizacion(**dict(result._mapping))
    raise HTTPException(status_code=404, detail="Cotización no encontrada")

@app.put("/cotizacion/{cotizacion_id}", response_model=Cotizacion, tags=["Cotizacion"])
def update_cotizacion(
    cotizacion_id: int,
    cotizacion_in: CotizacionCreate,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    upd = update(cotizacion).where(
        (cotizacion.c.id == cotizacion_id) & (cotizacion.c.usuario_id == user["id"])
    ).values(**cotizacion_in.dict())
    result = db.execute(upd)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    r = db.execute(select(cotizacion).where(cotizacion.c.id == cotizacion_id)).first()
    return Cotizacion(**dict(r._mapping))

@app.delete("/cotizacion/{cotizacion_id}", tags=["Cotizacion"])
def delete_cotizacion(
    cotizacion_id: int,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    result = db.execute(
        delete(cotizacion).where(
            (cotizacion.c.id == cotizacion_id) & (cotizacion.c.usuario_id == user["id"])
        )
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    return {"detail": "Cotización eliminada"}

@app.get("/cotizacion/health", tags=["Estado del Servicio"])
def health():
    return {"status": "ok"}

@app.get("/cotizacion/swagger", include_in_schema=False)
def redirigir_a_swagger():
    return RedirectResponse(url="/cotizacion/swagger-ui/index.html")
