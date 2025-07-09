import io
import json
from auth import get_current_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, delete
from models import reserva, metadata
import config


def handler(ctx, data: io.BytesIO = None):

    try:
        reserva_id = None
        # Try to get reserva_id from JSON body if present
        if data is not None and data.getvalue():
            try:
                body = json.loads(data.getvalue())
                reserva_id = body.get("reserva_id")
            except Exception as ex:
                # If body is not valid JSON, ignore and try to get from path
                pass
        # If not in body, try to get from path (Oracle Functions passes path params in ctx if configured)
        if not reserva_id:
            # Try to extract from ctx if possible (for RESTful DELETE /eliminar-reserva/<id>)
            path = None
            # Try to get path from ctx attributes or dict
            # Print ctx for debugging if still not found
            debug_ctx = str(ctx)
            # Try to get path from ctx attributes using __dict__ (for fdk.context.InvokeContext)
            if not path and hasattr(ctx, '__dict__'):
                d = ctx.__dict__
                # Try all keys in d for a string containing '/eliminar-reserva/'
                for k, v in d.items():
                    if isinstance(v, str) and '/eliminar-reserva/' in v:
                        path = v
                        break
            # Try all possible locations for path
            if hasattr(ctx, 'RequestURL') and isinstance(ctx.RequestURL, str):
                path = ctx.RequestURL
            elif hasattr(ctx, 'request_url') and isinstance(ctx.request_url, str):
                path = ctx.request_url
            elif isinstance(ctx, dict):
                if 'RequestURL' in ctx and isinstance(ctx['RequestURL'], str):
                    path = ctx['RequestURL']
                elif 'request_url' in ctx and isinstance(ctx['request_url'], str):
                    path = ctx['request_url']
            # Try to get from headers (sometimes path is in headers)
            if not path and hasattr(ctx, 'headers'):
                headers = getattr(ctx, 'headers')
                if isinstance(headers, dict):
                    if 'RequestURL' in headers and isinstance(headers['RequestURL'], str):
                        path = headers['RequestURL']
                    elif 'request_url' in headers and isinstance(headers['request_url'], str):
                        path = headers['request_url']
            # Defensive: only try regex if path is a string
            if isinstance(path, str):
                import re
                m = re.search(r'/eliminar-reserva/(\d+)', path)
                if m:
                    reserva_id = int(m.group(1))
            # If still not found, return debug info
            if not reserva_id:
                return json.dumps({"status": "error", "message": f"Missing reserva_id in input or path. Debug ctx: {debug_ctx}"})
        if not reserva_id:
            return json.dumps({"status": "error", "message": "Missing reserva_id in input or path"})

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