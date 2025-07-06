from pydantic import BaseModel
import datetime

class ReservaBase(BaseModel):
    usuario_id: int
    sucursal: str
    fecha: datetime.date
    hora: datetime.time

class ReservaCreate(ReservaBase):
    pass

class Reserva(ReservaBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
