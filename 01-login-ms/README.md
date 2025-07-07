# login-ms — Microservicio de Autenticación (Node.js + Express)

**NOTA** Este servicio fue desplegado en: OCI Container Instance. 

Su swagger esta disponible en: http://192.18.141.177/api-docs/ 

Este microservicio provee un endpoint `/login` para autenticar usuarios, y se puede utilizar como backend para aplicaciones tipo portal bancario. Ideal para pruebas en OCI (Oracle Cloud Infrastructure) como Container Instance, OKE, o incluso OCI Functions (con pequeños ajustes).

---

## 🚀 Pasos de Instalación y Uso

### 1. Crear el directorio y entrar

```bash
mkdir 02-login-ms
cd 02-login-ms
```

2. Inicializar el proyecto Node.js

```bash
npm init -y
````

3. Instalar dependencias
```bash
npm install express cors swagger-ui-express swagger-jsdoc jsonwebtoken mysql2 dotenv
```
*express*: Framework web para Node.js
*cors*: Permite llamadas desde otros orígenes (ej: tu frontend React)
*swagger-ui-express swagger-jsdoc*: Permite testear webservice 

4. Crear archivo principal index.js

5. Crear database

```sql
-- Conéctate como root u otro usuario con privilegios
DROP DATABASE IF EXISTS login_ms;
CREATE DATABASE IF NOT EXISTS login_ms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE login_ms;

CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    nombre VARCHAR(128) NOT NULL,
    password VARCHAR(128) NOT NULL, -- En producción usar hashes seguros
    email VARCHAR(128) UNIQUE
);


```

Ingresar usuarios dummy

```sql
INSERT INTO usuario (username, nombre, password, email)
VALUES ('demo', 'Demo User', 'demo', 'demo@demo.cl'),
       ('jdoe', 'John Doe', 'welcome1', 'jdoe@demo.cl'),
       ('dralquinta', 'Denny Alquinta', 'welcome2', 'dralquinta@demo.cl'),
       ('admin', 'Administrador', 'admin', 'admin@admin.cl');


```


---

📖 Guía de Consumo e Integración – login-ms
1. Autenticación (Login)


POST /login
Content-Type: application/json



Body

{
  "username": "demo",
  "password": "demo"
}
Respuesta Exitosa



{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSw...",
  "username": "demo",
  "name": "Demo User"
}



token: JWT que debes guardar en el cliente (por ejemplo, en localStorage/cookies).
username, name: información básica del usuario.

Errores
401 Unauthorized si las credenciales son incorrectas.

2. Cómo usar el JWT Token en requests posteriores
Todos los endpoints protegidos requieren el header Authorization:


Authorization: Bearer <JWT_TOKEN>

3. Consumo de Endpoints Protegidos
Ejemplo: Listar usuarios


GET /usuarios
Authorization: Bearer <JWT_TOKEN>


Respuesta

[
  {
    "id": 1,
    "username": "demo",
    "name": "Demo User"
  },
  ...
]
Ejemplo: Crear un usuario


POST /usuarios
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json


{
  "username": "nuevo",
  "name": "Nuevo Usuario",
  "password": "claveSegura"
}


{
  "id": 2,
  "username": "nuevo",
  "name": "Nuevo Usuario"
}
Ejemplo: Actualizar usuario


PUT /usuarios/2
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json


{
  "name": "Nombre Actualizado",
  "password": "nuevaClave"
}

Ejemplo: Eliminar usuario


DELETE /usuarios/2
Authorization: Bearer <JWT_TOKEN>
Respuesta: HTTP 204 No Content

4. Healthcheck


GET /health
Respuesta:
OK

5. Explorador interactivo
Puedes explorar y probar todos los endpoints en:


GET /api-docs
Usa el botón "Authorize" arriba a la derecha para ingresar tu JWT en Swagger.

6. Ejemplo de consumo desde JavaScript/React


// 1. LOGIN y guardar el token
fetch('http://tu-servidor/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'demo', password: 'demo' })
})
  .then(res => res.json())
  .then(data => {
    localStorage.setItem('token', data.token);
  });

// 2. Usar token en endpoints protegidos
const token = localStorage.getItem('token');
fetch('http://tu-servidor/usuarios', {
  method: 'GET',
  headers: { Authorization: `Bearer ${token}` }
})
  .then(res => res.json())
  .then(users => {
    // ... usar users
  });


7. Flujo recomendado de integración

El usuario ingresa credenciales en tu frontend → /login.

Guardas el JWT en el cliente.

Toda petición a endpoints protegidos debe enviar el JWT en el header Authorization: Bearer ....

El backend valida el JWT antes de responder.

Si el token es inválido o expiró, el backend responde 401 y el cliente debe pedir nuevo login.

8. Notas de Seguridad
Nunca expongas el JWT en URLs ni en formularios.

No almacenar el JWT en localStorage si tienes requisitos estrictos de seguridad (prefiere cookies httpOnly si aplica).

Cambia la secret de JWT (.env) por una clave segura antes de producción.

