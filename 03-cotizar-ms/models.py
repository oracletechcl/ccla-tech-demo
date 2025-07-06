# app/models.py

from sqlalchemy import (
    Table, Column, Integer, String, Float, MetaData, TIMESTAMP, ForeignKey,
    DECIMAL, DateTime, func
)

metadata = MetaData()

# Tabla de productos o tipos de crédito (puedes expandir con más detalles después)
producto = Table(
    "producto",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(64), nullable=False),
    Column("descripcion", String(255)),
)

# Mantenedor de tasas y condiciones comerciales
precios_consumo = Table(
    "precios_consumo",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("producto", String(128), nullable=False),
    Column("tasa", Float, nullable=False),
    Column("max_monto", Integer, nullable=False),
    Column("min_monto", Integer, nullable=False),
    Column("created_at", TIMESTAMP, nullable=False, server_default=func.now())
)

# Registro de cotizaciones realizadas por usuario
cotizacion = Table(
    "cotizacion",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("usuario_id", Integer, nullable=False),  # ID del usuario autenticado
    Column("producto_id", Integer, ForeignKey("producto.id"), nullable=True),
    Column("monto", DECIMAL(15, 2), nullable=False),
    Column("plazo_meses", Integer, nullable=False),
    Column("tasa_anual", DECIMAL(5, 2), nullable=False),
    Column("cuota_mensual", DECIMAL(15, 2), nullable=False),
    Column("total_pagado", DECIMAL(15, 2), nullable=False),
    Column("cae", DECIMAL(6, 2), nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)