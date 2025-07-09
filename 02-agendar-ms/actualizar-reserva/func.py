import io
import json
import datetime
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker
from models import metadata, reserva
import config
from auth import get_current_user


def handler(ctx, data: io.BytesIO = None):
    try:
        # Inicializar conexión a la base de datos
        engine = create_engine(config.DATABASE_URL)
        metadata.create_all(engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        # Leer cuerpo JSON
        body = json.loads(data.read())
        reserva_id = body["reserva_id"]
        sucursal = body["sucursal"]
        fecha = datetime.date.fromisoformat(body["fecha"])
        hora = datetime.time.fromisoformat(body["hora"])

        user = get_current_user(ctx)  # Autenticación mock o real

        db = SessionLocal()
        try:
            upd = update(reserva).where(
                (reserva.c.id == reserva_id) & (reserva.c.usuario_id == user["id"])
            ).values(
                sucursal=sucursal,
                fecha=fecha,
                hora=hora
            )
            result = db.execute(upd)
            db.commit()
            if result.rowcount == 0:
                return json.dumps({"status": "error", "message": "Reserva no encontrada"})
            
            r = db.execute(select(reserva).where(reserva.c.id == reserva_id)).first()
            # Serialize any date/time fields to ISO format
            result_dict = dict(r._mapping)
            for k, v in result_dict.items():
                if isinstance(v, (datetime.date, datetime.time, datetime.datetime)):
                    result_dict[k] = v.isoformat()
            return json.dumps(result_dict)
        finally:
            db.close()

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})