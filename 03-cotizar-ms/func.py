from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.orm import sessionmaker
from models import metadata, cotizacion, producto, precios_consumo
from auth import get_current_user
import config
import datetime
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Cotizador de Créditos de Consumo",
    version="1.0.0",
    docs_url="/cotizar/swagger-ui/index.html",
    openapi_url="/cotizar/openapi.json"
)

engine = create_engine(config.DATABASE_URL)
metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ----------- Esquemas Pydantic -----------

class PrecioConsumo(BaseModel):
    id: int
    producto: str
    tasa: float
    max_monto: int
    min_monto: int
    created_at: datetime.datetime

class PrecioConsumoCreate(BaseModel):
    producto: str
    tasa: float
    max_monto: int
    min_monto: int

class Cotizacion(BaseModel):
    id: int
    usuario_id: int
    producto_id: int = None
    monto: float
    plazo_meses: int
    tasa_anual: float
    cuota_mensual: float
    total_pagado: float
    cae: float
    created_at: datetime.datetime

class CotizacionCreate(BaseModel):
    producto_id: int = None
    monto: float
    plazo_meses: int
    tasa_anual: float
    cuota_mensual: float
    total_pagado: float
    cae: float

# ----------- DB Dependency -----------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------- CRUD Precios Consumo -----------

@app.post("/precios/", response_model=PrecioConsumo, tags=["Precios"])
def crear_precio(
    precio_in: PrecioConsumoCreate,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    now = datetime.datetime.utcnow()
    ins = precios_consumo.insert().values(**precio_in.dict(), created_at=now)
    result = db.execute(ins)
    db.commit()
    precio_id = result.lastrowid
    return {
        **precio_in.dict(),
        "id": precio_id,
        "created_at": now
    }

@app.get("/precios/", response_model=List[PrecioConsumo], tags=["Precios"])
def listar_precios(
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    result = db.execute(select(precios_consumo))
    return [dict(row._mapping) for row in result]

@app.put("/precios/{precio_id}", response_model=PrecioConsumo, tags=["Precios"])
def actualizar_precio(
    precio_id: int,
    precio_in: PrecioConsumoCreate,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    upd = update(precios_consumo).where(precios_consumo.c.id == precio_id).values(**precio_in.dict())
    result = db.execute(upd)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Precio no encontrado")
    r = db.execute(select(precios_consumo).where(precios_consumo.c.id == precio_id)).first()
    return dict(r._mapping)

@app.delete("/precios/{precio_id}", tags=["Precios"])
def eliminar_precio(
    precio_id: int,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    result = db.execute(delete(precios_consumo).where(precios_consumo.c.id == precio_id))
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Precio no encontrado")
    return {"detail": "Precio eliminado"}

# ----------- CRUD Cotizaciones -----------

@app.post("/cotizaciones/", response_model=Cotizacion, tags=["Cotizaciones"])
def crear_cotizacion(
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
    cot_id = result.lastrowid
    return {
        **cotizacion_in.dict(),
        "id": cot_id,
        "usuario_id": user["id"],
        "created_at": now
    }

@app.get("/cotizaciones/", response_model=List[Cotizacion], tags=["Cotizaciones"])
def listar_cotizaciones(
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    result = db.execute(select(cotizacion).where(cotizacion.c.usuario_id == user["id"]))
    return [dict(row._mapping) for row in result]

@app.get("/cotizaciones/{cotizacion_id}", response_model=Cotizacion, tags=["Cotizaciones"])
def obtener_cotizacion(
    cotizacion_id: int,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    result = db.execute(
        select(cotizacion).where(
            (cotizacion.c.id == cotizacion_id) & (cotizacion.c.usuario_id == user["id"])
        )
    ).first()
    if result:
        return dict(result._mapping)
    raise HTTPException(status_code=404, detail="Cotización no encontrada")

@app.put("/cotizaciones/{cotizacion_id}", response_model=Cotizacion, tags=["Cotizaciones"])
def actualizar_cotizacion(
    cotizacion_id: int,
    cotizacion_in: CotizacionCreate,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    upd = update(cotizacion).where(
        (cotizacion.c.id == cotizacion_id) & (cotizacion.c.usuario_id == user["id"])
    ).values(
        producto_id=cotizacion_in.producto_id,
        monto=cotizacion_in.monto,
        plazo_meses=cotizacion_in.plazo_meses,
        tasa_anual=cotizacion_in.tasa_anual,
        cuota_mensual=cotizacion_in.cuota_mensual,
        total_pagado=cotizacion_in.total_pagado,
        cae=cotizacion_in.cae
    )
    result = db.execute(upd)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    r = db.execute(select(cotizacion).where(cotizacion.c.id == cotizacion_id)).first()
    return dict(r._mapping)

@app.delete("/cotizaciones/{cotizacion_id}", tags=["Cotizaciones"])
def eliminar_cotizacion(
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

# ----------- Endpoints Públicos -----------

@app.get("/cotizar", tags=["Estado del Servicio"])
def cotizar_info():
    return {"message": "Cotizar servicio activo"}

@app.get("/cotizar/swagger", include_in_schema=False)
def redirigir_swagger():
    return RedirectResponse(url="/cotizar/swagger-ui/index.html")

@app.get("/health", tags=["Estado del Servicio"])
def health():
    return {"status": "ok"}