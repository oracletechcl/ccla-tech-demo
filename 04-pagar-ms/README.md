Crear DB

```sql

DROP DATABASE IF EXISTS pagar_ms;
CREATE DATABASE IF NOT EXISTS pagar_ms;
USE pagar_ms;
```

Crear tabla

```sql
CREATE TABLE deuda (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario_id BIGINT NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    monto DECIMAL(15,2) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_pago TIMESTAMP NULL
);

```