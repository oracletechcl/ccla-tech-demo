
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
class CotizacionCreate(BaseModel):
    producto_seguro_id: int
    plazo_meses: int

class Cotizacion(BaseModel):
    id: int
    usuario_id: int
    producto_seguro_id: int
    producto_nombre: str
    monto: float
    plazo_meses: int
    tasa_anual: float
    cuota_mensual: float
    total_pagado: float
    cae: float
    created_at: Optional[datetime.datetime] = None

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD Endpoints
import random
from fastapi import Depends
from sqlalchemy import select
from models import producto_seguro

# Expose /productos endpoint after app and dependencies are defined
@app.get("/productos", tags=["Productos"])
def list_productos(db=Depends(get_db)):
    result = db.execute(select(producto_seguro))
    return [dict(row._mapping) for row in result]


@app.post("/cotizacion", response_model=Cotizacion, tags=["Cotizacion"])
def create_cotizacion(
    cotizacion_in: CotizacionCreate,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    now = datetime.datetime.now()
    # Fetch product details
    prod = db.execute(select(producto_seguro).where(producto_seguro.c.id == cotizacion_in.producto_seguro_id)).first()
    if not prod:
        raise HTTPException(status_code=400, detail="Producto no encontrado")
    prod_data = dict(prod._mapping)
    # Calculate quote fields
    monto = float(prod_data.get('prima_base', 0))
    tasa_anual = 5.0  # Example: fixed or from product
    plazo_meses = cotizacion_in.plazo_meses
    cuota_mensual = round(monto / plazo_meses, 2) if plazo_meses else 0
    total_pagado = round(cuota_mensual * plazo_meses, 2)
    cae = round(random.uniform(1, 5), 2)
    ins = cotizacion.insert().values(
        usuario_id=user["id"],
        producto_seguro_id=cotizacion_in.producto_seguro_id,
        monto=monto,
        plazo_meses=plazo_meses,
        tasa_anual=tasa_anual,
        cuota_mensual=cuota_mensual,
        total_pagado=total_pagado,
        cae=cae,
        created_at=now
    )
    result = db.execute(ins)
    db.commit()
    return Cotizacion(
        id=result.lastrowid,
        usuario_id=user["id"],
        producto_seguro_id=cotizacion_in.producto_seguro_id,
        producto_nombre=prod_data.get('nombre', ''),
        monto=monto,
        plazo_meses=plazo_meses,
        tasa_anual=tasa_anual,
        cuota_mensual=cuota_mensual,
        total_pagado=total_pagado,
        cae=cae,
        created_at=now
    )

@app.get("/cotizacion", response_model=List[Cotizacion], tags=["Cotizacion"])
def list_cotizaciones(user=Depends(get_current_user), db=Depends(get_db)):
    result = db.execute(select(cotizacion).where(cotizacion.c.usuario_id == user["id"]))
    cotizaciones = []
    for row in result:
        cot_dict = dict(row._mapping)
        # If producto_nombre is missing, fetch it from producto_seguro
        if 'producto_nombre' not in cot_dict or not cot_dict['producto_nombre']:
            prod = db.execute(select(producto_seguro).where(producto_seguro.c.id == cot_dict['producto_seguro_id'])).first()
            cot_dict['producto_nombre'] = prod._mapping['nombre'] if prod else ''
        cotizaciones.append(Cotizacion(**cot_dict))
    return cotizaciones

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
