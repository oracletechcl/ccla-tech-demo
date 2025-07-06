import React from 'react';
import { Container, Typography, Button, Card, CardContent, Grid, Box, Paper, Divider, List, ListItem, ListItemText } from '@mui/material';

export default function Home() {
  return (
    <Container maxWidth="md" sx={{ my: 4 }}>
      {/* Banner */}
      <Paper elevation={4} sx={{ background: 'linear-gradient(90deg, #003366 60%, #00c6d7 100%)', p: 4, mb: 3, color: '#fff', textAlign: 'center' }}>
        <Typography variant="h3" fontWeight="bold">Portal Bancario</Typography>
      </Paper>
      <Grid container spacing={3}>
        {/* Actions */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Agenda tu visita a sucursal</Typography>
              <Typography variant="body2" gutterBottom>Agenda fácilmente tu atención presencial.</Typography>
              <Button fullWidth variant="contained" color="primary">Agendar Visita</Button>
            </CardContent>
          </Card>
          <Box height={2} />
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Cotiza tu seguro automotriz</Typography>
              <Typography variant="body2" gutterBottom>Obtén tu cotización en minutos.</Typography>
              <Button fullWidth variant="outlined" color="secondary">Cotizar Seguro</Button>
            </CardContent>
          </Card>
          <Box height={2} />
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Paga tu crédito</Typography>
              <Typography variant="body2" gutterBottom>Realiza el pago de tus créditos activos.</Typography>
              <Button fullWidth variant="contained" color="success">Pagar Crédito</Button>
            </CardContent>
          </Card>
        </Grid>
        {/* Account + Credit Card */}
        <Grid item xs={12} md={8}>
          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h5" gutterBottom>Cuenta Corriente</Typography>
              <Typography variant="body1" fontWeight="bold" color="primary">
                Saldo actual: <span style={{ fontWeight: 700 }}>1,234,567.89 CLP</span>
              </Typography>
              <Divider sx={{ my: 2 }} />
              <Typography variant="subtitle1" fontWeight="bold">Últimos movimientos:</Typography>
              <List dense>
                <ListItem><ListItemText primary="2025-07-05 - Pago luz: -35,000.00 CLP" /></ListItem>
                <ListItem><ListItemText primary="2025-07-04 - Transferencia recibida: 200,000.00 CLP" /></ListItem>
                <ListItem><ListItemText primary="2025-07-03 - Compra supermercado: -45,000.00 CLP" /></ListItem>
                <ListItem><ListItemText primary="2025-06-29 - Abono nómina: 1,200,000.00 CLP" /></ListItem>
              </List>
            </CardContent>
          </Card>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>Tarjeta de Crédito</Typography>
              <Typography variant="body2">N° **** **** **** 9876</Typography>
              <Typography variant="body2">Cupo: 2,000,000.00 CLP</Typography>
              <Typography variant="body2">Usado: 850,000.00 CLP</Typography>
              <Typography variant="body2">Vencimiento: 2025-07-30</Typography>
              <Divider sx={{ my: 2 }} />
              <Typography variant="subtitle1" fontWeight="bold">Movimientos recientes:</Typography>
              <List dense>
                <ListItem><ListItemText primary="2025-07-05 - Restaurante: -45,000.00 CLP" /></ListItem>
                <ListItem><ListItemText primary="2025-07-04 - Bencina: -60,000.00 CLP" /></ListItem>
                <ListItem><ListItemText primary="2025-06-26 - Pago anterior: 500,000.00 CLP" /></ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
}
