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

        engine = create_engine(DATABASE_URL)
        metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db = Session()

        result = db.execute(select(reserva).where(reserva.c.usuario_id == user["id"]))
        rows = [dict(row._mapping) for row in result]
        db.close()

        return json.dumps(rows)

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})