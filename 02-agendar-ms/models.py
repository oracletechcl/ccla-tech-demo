from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Time, DateTime

metadata = MetaData()

# Solo la tabla de reservas, con usuario_id como referencia
reserva = Table(
    "reserva",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("usuario_id", Integer, nullable=False),
    Column("sucursal", String(64), nullable=False),
    Column("fecha", Date, nullable=False),
    Column("hora", Time, nullable=False),
    Column("created_at", DateTime, nullable=False)
)
