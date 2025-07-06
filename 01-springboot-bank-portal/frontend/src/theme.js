// frontend/src/theme.js
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: { main: '#003366' },
    secondary: { main: '#005a9e' },
    background: { default: '#f4f8fb' }
  },
  shape: { borderRadius: 14 }
});

export default theme;
