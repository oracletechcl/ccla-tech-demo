import io
import json
import datetime
from auth import get_current_user
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from models import metadata, reserva
import config

def handler(ctx, data: io.BytesIO = None):
    try:
        # Leer y validar input JSON
        body = json.loads(data.read())
        sucursal = body.get("sucursal")
        fecha = body.get("fecha")
        hora = body.get("hora")

        if not all([sucursal, fecha, hora]):
            return json.dumps({"status": "error", "message": "Campos 'sucursal', 'fecha' y 'hora' son requeridos"})

        fecha = datetime.date.fromisoformat(fecha)
        hora = datetime.time.fromisoformat(hora)

        # Obtener usuario autenticado
        user = get_current_user(ctx)

        # Inicializar conexión DB
        db_url = config.DATABASE_URL
        if not db_url:
            raise Exception("DATABASE_URL no seteada en config")

        engine = create_engine(db_url)
        metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()

        # Crear reserva
        now = datetime.datetime.utcnow()
        stmt = insert(reserva).values(
            usuario_id=user["id"],
            sucursal=sucursal,
            fecha=fecha,
            hora=hora,
            created_at=now
        )
        result = db.execute(stmt)
        db.commit()

        return json.dumps({
            "status": "ok",
            "id": result.lastrowid,
            "usuario_id": user["id"],
            "sucursal": sucursal,
            "fecha": fecha.isoformat(),
            "hora": hora.isoformat(),
            "created_at": now.isoformat()
        })

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})