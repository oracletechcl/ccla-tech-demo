from sqlalchemy import Table, Column, Integer, String, Float, MetaData, DECIMAL, DateTime, ForeignKey, func


metadata = MetaData()

cotizacion = Table(
    "cotizacion",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("usuario_id", Integer, nullable=False),
    Column("producto_seguro_id", Integer, ForeignKey("producto_seguro.id"), nullable=False),
    Column("monto", DECIMAL(15, 2), nullable=False),
    Column("plazo_meses", Integer, nullable=False),
    Column("tasa_anual", DECIMAL(5, 2), nullable=False),
    Column("cuota_mensual", DECIMAL(15, 2), nullable=False),
    Column("total_pagado", DECIMAL(15, 2), nullable=False),
    Column("cae", DECIMAL(6, 2), nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)

# New table for insurance products
producto_seguro = Table(
    "producto_seguro",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(64), nullable=False, unique=True),
    Column("descripcion", String(256)),
    Column("tipo", String(32)),
    Column("cobertura", String(128)),
    Column("prima_base", DECIMAL(15, 2)),
    Column("deducible", DECIMAL(15, 2)),
    Column("aseguradora", String(64)),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)
