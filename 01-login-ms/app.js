const express = require('express');
const cors = require('cors');
require('dotenv').config();
const jwt = require('jsonwebtoken');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');
const pool = require('./db');
const verifyJWT = require('./jwtMiddleware');

const app = express();
app.use(express.json());
app.use(cors());

// --- Swagger/OpenAPI ---
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Login Microservice API',
      version: '1.0.0',
      description: 'API para autenticación y usuarios con JWT'
    },
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT'
        }
      }
    },
    security: [{ bearerAuth: [] }]
  },
  apis: ['./app.js']
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

/**
 * @swagger
 * tags:
 *   - name: Auth
 *     description: Autenticación de usuarios
 *   - name: Usuarios
 *     description: Operaciones CRUD sobre usuarios
 *
 * components:
 *   schemas:
 *     Usuario:
 *       type: object
 *       properties:
 *         id:
 *           type: integer
 *         username:
 *           type: string
 *         nombre:
 *           type: string
 *         password:
 *           type: string
 *         email:
 *           type: string
 */

// --- ENDPOINT: Login ---
/**
 * @swagger
 * /login:
 *   post:
 *     tags: [Auth]
 *     summary: Autentica un usuario y devuelve un JWT
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
 *                 token:
 *                   type: string
 *                 username:
 *                   type: string
 *                 nombre:
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
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  try {
    const [rows] = await pool.execute(
      'SELECT * FROM usuario WHERE username = ? AND password = ?',
      [username, password]
    );
    if (rows.length === 1) {
      const user = rows[0];
      const token = jwt.sign(
        { id: user.id, username: user.username, nombre: user.nombre },
        process.env.JWT_SECRET,
        { expiresIn: '2h' }
      );
      return res.json({ token, username: user.username, nombre: user.nombre });
    } else {
      return res.status(401).json({ error: 'Credenciales incorrectas' });
    }
  } catch (err) {
    console.error('Error autenticando usuario:', err);
    return res.status(500).json({ error: 'Error interno de autenticación' });
  }
});

// --- CRUD USUARIOS ---
/**
 * @swagger
 * /usuarios:
 *   get:
 *     tags: [Usuarios]
 *     summary: Lista todos los usuarios
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Lista de usuarios
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Usuario'
 */
app.get('/usuarios', verifyJWT, async (req, res) => {
  try {
    const [rows] = await pool.execute('SELECT id, username, nombre, email FROM usuario');
    res.json(rows);
  } catch (err) {
    console.error('Error obteniendo usuarios:', err);
    res.status(500).json({ error: 'Error al obtener usuarios' });
  }
});

/**
 * @swagger
 * /usuarios:
 *   post:
 *     tags: [Usuarios]
 *     summary: Crea un nuevo usuario
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [username, nombre, password]
 *             properties:
 *               username:
 *                 type: string
 *               nombre:
 *                 type: string
 *               password:
 *                 type: string
 *               email:
 *                 type: string
 *     responses:
 *       201:
 *         description: Usuario creado exitosamente
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Usuario'
 */
app.post('/usuarios', verifyJWT, async (req, res) => {
  const { username, nombre, password, email } = req.body;
  try {
    const [result] = await pool.execute(
      'INSERT INTO usuario (username, nombre, password, email) VALUES (?, ?, ?, ?)',
      [username, nombre, password, email || null]
    );
    res.status(201).json({ id: result.insertId, username, nombre, email });
  } catch (err) {
    console.error('Error creando usuario:', err);
    res.status(500).json({ error: 'Error al crear usuario' });
  }
});

/**
 * @swagger
 * /usuarios/{id}:
 *   put:
 *     tags: [Usuarios]
 *     summary: Actualiza un usuario por ID
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               nombre:
 *                 type: string
 *               password:
 *                 type: string
 *               email:
 *                 type: string
 *     responses:
 *       200:
 *         description: Usuario actualizado
 */
app.put('/usuarios/:id', verifyJWT, async (req, res) => {
  const { id } = req.params;
  const { nombre, password, email } = req.body;
  try {
    await pool.execute(
      'UPDATE usuario SET nombre = ?, password = ?, email = ? WHERE id = ?',
      [nombre, password, email || null, id]
    );
    res.json({ id, nombre, email });
  } catch (err) {
    console.error('Error actualizando usuario:', err);
    res.status(500).json({ error: 'Error al actualizar usuario' });
  }
});

/**
 * @swagger
 * /usuarios/{id}:
 *   delete:
 *     tags: [Usuarios]
 *     summary: Elimina un usuario por ID
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     responses:
 *       204:
 *         description: Usuario eliminado
 */
app.delete('/usuarios/:id', verifyJWT, async (req, res) => {
  const { id } = req.params;
  try {
    await pool.execute('DELETE FROM usuario WHERE id = ?', [id]);
    res.status(204).send();
  } catch (err) {
    console.error('Error eliminando usuario:', err);
    res.status(500).json({ error: 'Error al eliminar usuario' });
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

const PORT = process.env.PORT || 80;
app.listen(PORT, '0.0.0.0', () => console.log(`login-ms running on port ${PORT}`));
