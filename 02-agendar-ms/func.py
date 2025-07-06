from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.orm import sessionmaker
from models import metadata, reserva
from auth import get_current_user  # <--- Nuevo import para autenticación JWT
import config
import datetime

app = FastAPI(
    title="Agenda de Visitas CRUD",
    version="1.0.0",
    docs_url="/api-docs"
)

engine = create_engine(config.DATABASE_URL)
metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------- ENDPOINTS --------

@app.post("/reservas/", response_model=Reserva)
def crear_reserva(
    reserva_in: ReservaCreate,
    user=Depends(get_current_user),  # Usuario autenticado del token
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

@app.get("/reservas/", response_model=List[Reserva])
def listar_reservas(
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    # Solo lista las reservas del usuario autenticado
    result = db.execute(select(reserva).where(reserva.c.usuario_id == user["id"]))
    return [dict(row._mapping) for row in result]

@app.get("/reservas/{reserva_id}", response_model=Reserva)
def obtener_reserva(
    reserva_id: int,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    # Solo puede obtener reservas propias
    result = db.execute(
        select(reserva).where(
            (reserva.c.id == reserva_id) & (reserva.c.usuario_id == user["id"])
        )
    ).first()
    if result:
        return dict(result._mapping)
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

@app.put("/reservas/{reserva_id}", response_model=Reserva)
def actualizar_reserva(
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
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    # Retornar los datos actualizados
    r = db.execute(select(reserva).where(reserva.c.id == reserva_id)).first()
    return dict(r._mapping)

@app.delete("/reservas/{reserva_id}")
def eliminar_reserva(
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
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {"detail": "Reserva eliminada"}

@app.get("/health")
def health():
    return {"status": "ok"}