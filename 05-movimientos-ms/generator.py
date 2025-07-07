import random
import datetime

SALDO_FIJO_INICIAL = 10_000_000.0

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

# Diccionario en memoria para guardar los movimientos por usuario
movimientos_por_usuario = {}

def inicializar_usuario(user_id: str):
    if user_id not in movimientos_por_usuario:
        movimientos_por_usuario[user_id] = []

def generar_movimiento(user_id: str):
    inicializar_usuario(user_id)

    tipo = random.choices(["ingreso", "egreso"], weights=[0.4, 0.6])[0]
    monto = round(random.uniform(5000, 300000), 2)

    descripcion = random.choice(
        DESCRIPCIONES_INGRESO if tipo == "ingreso" else DESCRIPCIONES_EGRESO
    )

    movimiento = {
        "fecha": datetime.datetime.now().isoformat(),
        "tipo": tipo,
        "descripcion": descripcion,
        "monto": monto
    }

    movimientos_por_usuario[user_id].append(movimiento)
    return movimiento

def generar_lote_de_movimientos(user_id: str, cantidad=5):
    inicializar_usuario(user_id)
    return [generar_movimiento(user_id) for _ in range(cantidad)]

def obtener_movimientos(user_id: str):
    inicializar_usuario(user_id)
    return _movimientos_con_saldo(user_id)

def _movimientos_con_saldo(user_id: str):
    saldo = SALDO_FIJO_INICIAL
    movimientos = []
    for m in movimientos_por_usuario[user_id]:
        if m["tipo"] == "ingreso":
            saldo += m["monto"]
        else:
            saldo -= m["monto"]
        movimientos.append({
            **m,
            "saldo": round(saldo, 2)
        })
    return movimientos

def obtener_saldo(user_id: str):
    inicializar_usuario(user_id)
    ingresos = sum(m["monto"] for m in movimientos_por_usuario[user_id] if m["tipo"] == "ingreso")
    egresos = sum(m["monto"] for m in movimientos_por_usuario[user_id] if m["tipo"] == "egreso")
    saldo_final = SALDO_FIJO_INICIAL + ingresos - egresos
    return round(saldo_final, 2)

def obtener_resumen(user_id: str):
    inicializar_usuario(user_id)
    ingresos = sum(m["monto"] for m in movimientos_por_usuario[user_id] if m["tipo"] == "ingreso")
    egresos = sum(m["monto"] for m in movimientos_por_usuario[user_id] if m["tipo"] == "egreso")
    return {
        "saldo_inicial": SALDO_FIJO_INICIAL,
        "saldo_actual": round(SALDO_FIJO_INICIAL + ingresos - egresos, 2),
        "total_ingresos": round(ingresos, 2),
        "total_egresos": round(egresos, 2),
        "cantidad_movimientos": len(movimientos_por_usuario[user_id])
    }