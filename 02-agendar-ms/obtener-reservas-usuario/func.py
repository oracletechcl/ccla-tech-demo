import io
import json
from auth import get_current_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from shared.models import reserva, metadata
import config

def handler(ctx, data: io.BytesIO = None):
    try:
        user = get_current_user(ctx)

        # Conexión DB
        db_url = config.DATABASE_URL
        if not db_url:
            raise Exception("DATABASE_URL no seteada en config")

        engine = create_engine(db_url)
        metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db = Session()

        try:
            result = db.execute(select(reserva).where(reserva.c.usuario_id == user["id"]))
            rows = [dict(row._mapping) for row in result]
        finally:
            db.close()

        return json.dumps(rows)

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})