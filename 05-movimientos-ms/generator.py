import threading
import time
import random
import datetime

movimientos_por_usuario = {}
saldos_por_usuario = {}

descripciones_ingreso = [
    "Depósito sueldo", "Transferencia familiar", "Reembolso salud",
    "Pago freelance", "Venta artículos usados", "Intereses cuenta",
    "Devolución impuestos", "Ingreso inversión", "Ingreso extra",
    "Subsidio estatal", "Premio concurso", "Aporte familiar"
]

descripciones_egreso = [
    "Compra supermercado", "Pago luz", "Transferencia a tercero",
    "Retiro cajero", "Compra online", "Pago arriendo", "Suscripción streaming",
    "Pago colegio", "Cafetería", "Bencina", "Farmacia", "Salida a comer",
    "Pago gimnasio", "Compra vestuario", "Taxi o Uber", "Donación"
]

def generar_movimiento_usuario(user_id):
    if user_id not in movimientos_por_usuario:
        movimientos_por_usuario[user_id] = []
        saldos_por_usuario[user_id] = {"saldo": 0.0, "ingresos": 0.0, "egresos": 0.0}

    data = saldos_por_usuario[user_id]
    tipo = random.choices(["ingreso", "egreso"], weights=[0.4, 0.6])[0]

    if tipo == "ingreso":
        descripcion = random.choice(descripciones_ingreso)
        monto = round(random.uniform(10000, 300000), 2)
        data["saldo"] += monto
        data["ingresos"] += monto
    else:
        descripcion = random.choice(descripciones_egreso)
        monto = round(random.uniform(5000, 250000), 2)
        data["saldo"] -= monto
        data["egresos"] += monto

    movimientos_por_usuario[user_id].append({
        "fecha": datetime.datetime.now().isoformat(),
        "tipo": tipo,
        "descripcion": descripcion,
        "monto": monto,
        "saldo": round(data["saldo"], 2)
    })

def generador_continuo():
    usuarios_mock = [1, 2, 3]  # Puedes reemplazar esto con una lista dinámica si deseas
    while True:
        for user_id in usuarios_mock:
            generar_movimiento_usuario(user_id)
        time.sleep(random.uniform(3, 6))  # Genera para todos cada 3–6 segundos

def iniciar_generador():
    thread = threading.Thread(target=generador_continuo, daemon=True)
    thread.start()