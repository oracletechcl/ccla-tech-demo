from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.orm import sessionmaker
from models import metadata, reserva
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
    usuario_id: int
    sucursal: str
    fecha: datetime.date
    hora: datetime.time

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/reservas/", response_model=Reserva)
def crear_reserva(reserva_in: ReservaCreate, db=Depends(get_db)):
    now = datetime.datetime.utcnow()
    ins = reserva.insert().values(**reserva_in.dict(), created_at=now)
    result = db.execute(ins)
    db.commit()
    reserva_id = result.lastrowid
    return {
        **reserva_in.dict(),
        "id": reserva_id,
        "created_at": now
    }

@app.get("/reservas/", response_model=List[Reserva])
def listar_reservas(db=Depends(get_db)):
    result = db.execute(select(reserva))
    return [dict(row._mapping) for row in result]

@app.get("/reservas/usuario/{usuario_id}", response_model=List[Reserva])
def listar_reservas_por_usuario(usuario_id: int, db=Depends(get_db)):
    result = db.execute(select(reserva).where(reserva.c.usuario_id == usuario_id))
    return [dict(row._mapping) for row in result]

@app.get("/reservas/{reserva_id}", response_model=Reserva)
def obtener_reserva(reserva_id: int, db=Depends(get_db)):
    result = db.execute(select(reserva).where(reserva.c.id == reserva_id)).first()
    if result:
        return dict(result._mapping)
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

@app.put("/reservas/{reserva_id}", response_model=Reserva)
def actualizar_reserva(reserva_id: int, reserva_in: ReservaCreate, db=Depends(get_db)):
    upd = update(reserva).where(reserva.c.id == reserva_id).values(**reserva_in.dict())
    result = db.execute(upd)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    # Retornar los datos actualizados
    r = db.execute(select(reserva).where(reserva.c.id == reserva_id)).first()
    return dict(r._mapping)

@app.delete("/reservas/{reserva_id}")
def eliminar_reserva(reserva_id: int, db=Depends(get_db)):
    result = db.execute(delete(reserva).where(reserva.c.id == reserva_id))
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {"detail": "Reserva eliminada"}

@app.get("/health")
def health():
    return {"status": "ok"}
