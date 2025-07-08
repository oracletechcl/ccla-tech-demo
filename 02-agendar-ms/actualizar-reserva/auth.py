import jwt
import os

JWT_SECRET = os.environ.get("JWT_SECRET", "98723bfdokjhfew897324kjhfsd98234j0120983120123hijahd")

def get_current_user(ctx):
    try:
        auth_header = ctx.Headers().get("authorization")
        if not auth_header:
            raise Exception("Authorization header missing")

        if not auth_header.startswith("Bearer "):
            raise Exception("Invalid Authorization header format")

        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload  # dict con info del usuario
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")
    except Exception as e:
        raise Exception(f"Error en autenticación: {str(e)}")