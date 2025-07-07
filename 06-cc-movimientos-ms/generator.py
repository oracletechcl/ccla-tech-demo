import random
from collections import defaultdict
from datetime import datetime

movimientos_por_usuario = defaultdict(list)
cupo_por_usuario = defaultdict(lambda: 700000)  # Cupo inicial
ingresos_por_usuario = defaultdict(int)
egresos_por_usuario = defaultdict(int)

descripciones_gasto = [
    "Compra en tienda", "Pago de servicio streaming", "Restaurante", "Combustible",
    "Hotel", "Suscripción software", "Ropa", "Electrodomésticos", "Entrada al cine",
    "Compras online", "Delivery", "Parqueadero", "Suscripción gimnasio", "Viaje"
]

def generar_movimiento(usuario: str):
    tipo = "egreso"
    if random.randint(1, 100) == 1:  # 1% de probabilidad de ingreso (pago)
        tipo = "ingreso"

    if tipo == "ingreso":
        monto = random.randint(20000, 150000)
        descripcion = "Pago tarjeta de crédito"
        cupo_por_usuario[usuario] += monto
        ingresos_por_usuario[usuario] += monto
    else:
        monto = random.randint(5000, 150000)
        descripcion = random.choice(descripciones_gasto)
        cupo_por_usuario[usuario] -= monto
        egresos_por_usuario[usuario] += monto

    movimiento = {
        "fecha": datetime.utcnow().isoformat(),
        "tipo": tipo,
        "monto": monto,
        "descripcion": descripcion
    }
    movimientos_por_usuario[usuario].insert(0, movimiento)
    if len(movimientos_por_usuario[usuario]) > 100:
        movimientos_por_usuario[usuario] = movimientos_por_usuario[usuario][:100]

def generar_si_es_necesario(usuario: str):
    if len(movimientos_por_usuario[usuario]) < 10 or random.random() < 0.25:
        generar_movimiento(usuario)