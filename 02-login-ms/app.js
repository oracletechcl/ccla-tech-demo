// 02-login-ms/app.js

const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

// Swagger/OpenAPI
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');

const app = express();
app.use(express.json());
app.use(cors());

// ---- Swagger setup ----
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Login Microservice API',
      version: '1.0.0',
      description: 'API para autenticación mock en el microservicio login-ms'
    }
  },
  apis: ['./app.js']
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// ---- Endpoint POST /login ----
/**
 * @swagger
 * /login:
 *   post:
 *     summary: Autentica un usuario (mock, desde users.json)
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [username, password]
 *             properties:
 *               username:
 *                 type: string
 *                 example: demo
 *               password:
 *                 type: string
 *                 example: demo
 *     responses:
 *       200:
 *         description: Autenticación exitosa
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 username:
 *                   type: string
 *                 name:
 *                   type: string
 *                 token:
 *                   type: string
 *       401:
 *         description: Credenciales incorrectas
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error:
 *                   type: string
 */
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const usersPath = path.join(__dirname, 'users.json');
  let users = [];
  try {
    users = JSON.parse(fs.readFileSync(usersPath, 'utf8'));
  } catch (err) {
    console.error('Error leyendo users.json:', err);
    return res.status(500).json({ error: 'Error interno de autenticación' });
  }
  const user = users.find(u => u.username === username && u.password === password);
  if (user) {
    return res.json({ username: user.username, name: user.name, token: 'fake-jwt-token' });
  } else {
    return res.status(401).json({ error: 'Credenciales incorrectas' });
  }
});

/**
 * @swagger
 * /health:
 *   get:
 *     summary: Healthcheck simple
 *     responses:
 *       200:
 *         description: OK
 */
app.get('/health', (req, res) => res.send('OK'));

// ---- Server setup ----
const PORT = process.env.PORT || 80;
app.listen(PORT, '0.0.0.0', () => console.log(`login-ms running on port ${PORT}`));
