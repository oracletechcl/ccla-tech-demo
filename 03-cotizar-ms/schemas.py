# app/schemas.py

from pydantic import BaseModel
import datetime
from typing import Optional

class CotizacionBase(BaseModel):
    producto_id: Optional[int] = None
    monto: float
    plazo_meses: int

class CotizacionCreate(CotizacionBase):
    tasa_anual: float
    cuota_mensual: float
    total_pagado: float
    cae: float

class Cotizacion(CotizacionBase):
    id: int
    usuario_id: int
    tasa_anual: float
    cuota_mensual: float
    total_pagado: float
    cae: float
    created_at: datetime.datetime

    class Config:
        orm_mode = True

# Ejemplo para mantener productos/precios
class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class Precio(BaseModel):
    id: int
    producto_id: int
    tasa_anual: float
    created_at: datetime.datetime

class PrecioCreate(BaseModel):
    producto_id: int
    tasa_anual: float

class PrecioConsumoBase(BaseModel):
    producto: str
    tasa: float
    max_monto: int
    min_monto: int

class PrecioConsumoCreate(PrecioConsumoBase):
    pass

class PrecioConsumo(PrecioConsumoBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True