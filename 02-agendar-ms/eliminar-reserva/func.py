import io
import json
from auth import get_current_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, delete
from shared.models import reserva, metadata
import config


def handler(ctx, data: io.BytesIO = None):
    try:
        if data is None:
            return json.dumps({"status": "error", "message": "No input data provided"})

        try:
            body = json.loads(data.getvalue())
            reserva_id = body.get("reserva_id")
            if not reserva_id:
                return json.dumps({"status": "error", "message": "Missing reserva_id in input"})
        except Exception as ex:
            return json.dumps({"status": "error", "message": f"Invalid input: {str(ex)}"})

        # Autenticación
        user = get_current_user(ctx)

        # DB Configuración
        db_url = config.DATABASE_URL
        if not db_url:
            raise Exception("DATABASE_URL no seteada en config")

        engine = create_engine(db_url)
        metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db = Session()

        try:
            result = db.execute(
                delete(reserva).where(
                    (reserva.c.id == reserva_id) & (reserva.c.usuario_id == user["id"])
                )
            )
            db.commit()

            if result.rowcount == 0:
                return json.dumps({"status": "error", "message": "Reserva no encontrada"})

            return json.dumps({"status": "ok", "message": "Reserva eliminada"})
        finally:
            db.close()

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})