

---
## MySQL

Install client

```bash
sudo yum install mysql
```

Connect to Database

```bash
mysql -h <host> -u <usuario> -p
```
Password will be required

Then execute: 

```sql
-- Crear la base de datos para tu microservicio
DROP DATABASE IF EXISTS agenda_ms;
CREATE DATABASE agenda_ms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE agenda_ms;
-- Crear usuario solo si necesitas uno nuevo (reemplaza contraseña segura)
CREATE USER 'agenda_user'@'%' IDENTIFIED BY 'W3lc0m31.';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON agenda_ms.* TO 'agenda_user'@'%';

-- Refrescar permisos
FLUSH PRIVILEGES;
```


Create table:

```sql
USE agenda_ms;

CREATE TABLE reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,            -- ID del usuario autenticado (referencia a login-ms)
    sucursal VARCHAR(64) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL
);

ALTER TABLE reserva ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;
-- for audit

```


Output: 

```sql

mysql> DROP DATABASE IF EXISTS agenda_ms;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> CREATE DATABASE agenda_ms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
Query OK, 1 row affected (0.00 sec)


mysql> 
mysql> -- Crear usuario solo si necesitas uno nuevo (reemplaza contraseña segura)
mysql> CREATE USER 'agenda_user'@'%' IDENTIFIED BY 'W3lc0m31.';
Query OK, 0 rows affected (0.00 sec)

mysql> 
mysql> -- Otorgar permisos
mysql> GRANT ALL PRIVILEGES ON agenda_ms.* TO 'agenda_user'@'%';
Query OK, 0 rows affected (0.00 sec)

mysql> 
mysql> -- Refrescar permisos
mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE TABLE reserva (
    ->     id INT AUTO_INCREMENT PRIMARY KEY,
    ->     username VARCHAR(64) NOT NULL,    -- Viene del login-ms
    ->     sucursal VARCHAR(64) NOT NULL,
    ->     fecha DATE NOT NULL,
    ->     hora TIME NOT NULL,
    ->     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -> );
Query OK, 0 rows affected (0.01 sec)


```

Quick test

```sql
INSERT INTO reservas (nombre, rut, usuario, sucursal, fecha, hora)
VALUES ('Juan Perez', '12.345.678-9', 'juanp', 'Santiago Centro', '2025-07-10', '10:00');

```