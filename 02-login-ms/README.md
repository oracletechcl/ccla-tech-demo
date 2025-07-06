# login-ms — Microservicio de Autenticación (Node.js + Express)

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
npm install express cors swagger-ui-express swagger-jsdoc
```
*express*: Framework web para Node.js
*cors*: Permite llamadas desde otros orígenes (ej: tu frontend React)
*swagger-ui-express swagger-jsdoc*: Permite testear webservice 

4. Crear archivo principal index.js


