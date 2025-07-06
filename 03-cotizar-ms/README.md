
Crear la DB

```sql
-- Crear la base de datos para tu microservicio
DROP DATABASE IF EXISTS cotizar_ms;
CREATE DATABASE IF NOT EXISTS cotizar_ms;
USE cotizar_ms;

CREATE TABLE IF NOT EXISTS precios_consumo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto VARCHAR(128) NOT NULL,
    tasa FLOAT NOT NULL,
    max_monto INT NOT NULL,
    min_monto INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

