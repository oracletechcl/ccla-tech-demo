import io
import json
from auth import get_current_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from models import reserva, metadata
import config

def handler(ctx, data: io.BytesIO = None):
    try:
        user = get_current_user(ctx)

        # Leer y validar input
        if data is None:
            return json.dumps({"status": "error", "message": "No input data provided"})

        try:
            body = json.loads(data.getvalue())
            reserva_id = body.get("reserva_id")
            if reserva_id is None:
                return json.dumps({"status": "error", "message": "Missing reserva_id in input"})
        except Exception as ex:
            return json.dumps({"status": "error", "message": f"Invalid input: {str(ex)}"})

        # Conexión DB
        db_url = config.DATABASE_URL
        if not db_url:
            raise Exception("DATABASE_URL no seteada en config")

        engine = create_engine(db_url)
        metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db = Session()

        try:
            result = db.execute(
                select(reserva).where(
                    (reserva.c.usuario_id == user["id"]) & (reserva.c.id == reserva_id)
                )
            ).first()
        finally:
            db.close()

        if result:
            return json.dumps(dict(result._mapping))
        else:
            return json.dumps({"status": "error", "message": "Reserva no encontrada"})

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})