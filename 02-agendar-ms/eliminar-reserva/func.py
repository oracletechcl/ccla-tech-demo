import io
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete
from shared.models import reserva, metadata
from shared.auth import get_current_user
from shared.config import DATABASE_URL
from sqlalchemy import create_engine

def handler(ctx, data: io.BytesIO = None):
    try:
        # Parse reserva_id from input data
        if data is None:
            return json.dumps({"status": "error", "message": "No input data provided"})
        try:
            body = json.loads(data.getvalue())
            reserva_id = body.get("reserva_id")
            if reserva_id is None:
                return json.dumps({"status": "error", "message": "Missing reserva_id in input"})
        except Exception as ex:
            return json.dumps({"status": "error", "message": f"Invalid input: {str(ex)}"})

        user = get_current_user(ctx)

        engine = create_engine(DATABASE_URL)
        metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        db = session()

        result = db.execute(
            delete(reserva).where(
                (reserva.c.id == reserva_id) & (reserva.c.usuario_id == user["id"])
            )
        )
        db.commit()
        db.close()

        if result.rowcount == 0:
            return json.dumps({"status": "error", "message": "Reserva no encontrada"})

        return json.dumps({"status": "ok", "message": "Reserva eliminada"})

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})