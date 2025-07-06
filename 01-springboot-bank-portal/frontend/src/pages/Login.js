import React, { useState } from 'react';
import { Container, Box, TextField, Button, Typography, Paper } from '@mui/material';

// Simulate a call to an authentication API (mock)
async function mockLoginApi(username, password) {
  // Simulate network delay
  await new Promise((res) => setTimeout(res, 800));
  // Accept only user: demo, pass: demo
  if (username === 'demo' && password === 'demo') {
    return { username: 'demo', name: 'Demo User', token: 'fake-jwt-token' };
  }
  throw new Error('Credenciales incorrectas');
}

export default function Login({ setUser }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const user = await mockLoginApi(username, password);
      setUser(user);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="xs" sx={{ my: 10 }}>
      <Paper elevation={6} sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom align="center">
          Iniciar Sesión
        </Typography>
        <Box component="form" onSubmit={handleLogin}>
          <TextField
            label="Usuario"
            fullWidth
            margin="normal"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoFocus
          />
          <TextField
            label="Contraseña"
            fullWidth
            margin="normal"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {error && (
            <Typography color="error" sx={{ mt: 1, mb: 2 }}>
              {error}
            </Typography>
          )}
          <Button
            variant="contained"
            fullWidth
            type="submit"
            sx={{ mt: 2 }}
            disabled={loading}
          >
            {loading ? 'Ingresando...' : 'Ingresar'}
          </Button>
          <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 2, textAlign: 'center' }}>
            Usuario demo: <b>demo</b> | Contraseña: <b>demo</b>
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
}
