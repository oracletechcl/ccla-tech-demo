import io
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from shared.models import reserva, metadata
from shared.auth import get_current_user
from shared.config import DATABASE_URL
from sqlalchemy import create_engine

def handler(ctx, data: io.BytesIO = None):
    try:
        user = get_current_user(ctx)

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

        engine = create_engine(DATABASE_URL)
        metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db = Session()

        result = db.execute(
            select(reserva).where(
                (reserva.c.usuario_id == user["id"]) & (reserva.c.id == reserva_id)
            )
        ).first()
        db.close()

        if result:
            return json.dumps(dict(result._mapping))
        else:
            return json.dumps({"status": "error", "message": "Reserva no encontrada"})

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})