import threading
import time
import random
import datetime

# ==== Catálogos de descripciones ====
DESCRIPCIONES_INGRESO = [
    "Depósito sueldo", "Transferencia familiar", "Reembolso salud",
    "Pago freelance", "Venta artículos usados", "Intereses cuenta",
    "Devolución impuestos", "Ingreso inversión", "Ingreso extra",
    "Subsidio estatal", "Premio concurso", "Aporte familiar"
]

DESCRIPCIONES_EGRESO = [
    "Compra supermercado", "Pago luz", "Transferencia a tercero",
    "Retiro cajero", "Compra online", "Pago arriendo", "Suscripción streaming",
    "Pago colegio", "Cafetería", "Bencina", "Farmacia", "Salida a comer",
    "Pago gimnasio", "Compra vestuario", "Taxi o Uber", "Donación"
]

# ==== Clase Usuario ====
class Usuario:
    def __init__(self, user_id):
        self.user_id = user_id
        self.saldo = 0.0
        self.total_ingresos = 0.0
        self.total_egresos = 0.0
        self.movimientos = []

    def generar_movimiento(self):
        tipo = random.choices(["ingreso", "egreso"], weights=[0.4, 0.6])[0]

        if tipo == "ingreso":
            descripcion = random.choice(DESCRIPCIONES_INGRESO)
            monto = round(random.uniform(10000, 300000), 2)
            self.saldo += monto
            self.total_ingresos += monto
        else:
            descripcion = random.choice(DESCRIPCIONES_EGRESO)
            monto = round(random.uniform(5000, 250000), 2)
            self.saldo -= monto
            self.total_egresos += monto

        movimiento = {
            "fecha": datetime.datetime.now().isoformat(),
            "tipo": tipo,
            "descripcion": descripcion,
            "monto": monto,
            "saldo": round(self.saldo, 2)
        }

        self.movimientos.append(movimiento)

    def obtener_ultimo_movimiento(self):
        return self.movimientos[-1] if self.movimientos else None

    def obtener_estado_actual(self):
        return {
            "user_id": self.user_id,
            "saldo": round(self.saldo, 2),
            "total_ingresos": round(self.total_ingresos, 2),
            "total_egresos": round(self.total_egresos, 2),
            "cantidad_movimientos": len(self.movimientos)
        }

# ==== Repositorio de usuarios (en memoria) ====
usuarios_registrados = {}

def registrar_usuario(user_id):
    if user_id not in usuarios_registrados:
        usuarios_registrados[user_id] = Usuario(user_id)

def obtener_usuario(user_id):
    return usuarios_registrados.get(user_id)

def listar_usuarios():
    return list(usuarios_registrados.values())

# ==== Generador continuo de movimientos ====
def generador_continuo():
    while True:
        for usuario in listar_usuarios():
            usuario.generar_movimiento()
        time.sleep(random.uniform(3, 6))

def iniciar_generador():
    thread = threading.Thread(target=generador_continuo, daemon=True)
    thread.start()