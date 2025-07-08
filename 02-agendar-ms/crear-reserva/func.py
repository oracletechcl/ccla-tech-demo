import io
import json
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from shared.models import reserva, metadata
from shared.auth import get_current_user
from shared.config import DATABASE_URL
from sqlalchemy import create_engine

def handler(ctx, data: io.BytesIO = None):
    try:
        payload = json.loads(data.read())
        user = get_current_user(ctx)

        engine = create_engine(DATABASE_URL)
        metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db = Session()

        now = datetime.datetime.utcnow()
        ins = reserva.insert().values(
            usuario_id=user["id"],
            sucursal=payload["sucursal"],
            fecha=payload["fecha"],
            hora=payload["hora"],
            created_at=now
        )
        result = db.execute(ins)
        db.commit()
        db.close()

        return json.dumps({
            "id": result.lastrowid,
            "usuario_id": user["id"],
            "sucursal": payload["sucursal"],
            "fecha": payload["fecha"],
            "hora": payload["hora"],
            "created_at": now.isoformat()
        })

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})