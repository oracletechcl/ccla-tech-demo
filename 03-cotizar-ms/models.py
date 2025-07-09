from sqlalchemy import Table, Column, Integer, String, Float, MetaData, DECIMAL, DateTime, ForeignKey, func

metadata = MetaData()

cotizacion = Table(
    "cotizacion",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("usuario_id", Integer, nullable=False),
    Column("producto", String(32), nullable=False),
    Column("monto", DECIMAL(15, 2), nullable=False),
    Column("plazo_meses", Integer, nullable=False),
    Column("tasa_anual", DECIMAL(5, 2), nullable=False),
    Column("cuota_mensual", DECIMAL(15, 2), nullable=False),
    Column("total_pagado", DECIMAL(15, 2), nullable=False),
    Column("cae", DECIMAL(6, 2), nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)
