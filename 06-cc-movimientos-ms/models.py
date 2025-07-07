from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TipoMovimiento(str, Enum):
    ingreso = "ingreso"
    egreso = "egreso"

class Movimiento(BaseModel):
    fecha: datetime
    descripcion: str
    tipo: TipoMovimiento
    monto: float
    saldo: float