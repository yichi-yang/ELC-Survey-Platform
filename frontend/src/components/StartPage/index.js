import * as React from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';

const RedButton = styled(Button)({
  backgroundColor: '#880808',
  boxShadow: 'none',
  color: 'white',
  textTransform: 'none',
  fontSize: '2rem',
  margin: 0,
  fontWeight: 'bold',
  width: '100%',
  minHeight: '25vh',
  '&:hover': {
    backgroundColor: '#880808'
  },
});

export default function StartPage() {
  return (
    <div style={{
      backgroundColor: '#990000',
      minHeight: '100vh',
      display: 'flex',
      alignContent: 'center',
      justifyContent: 'center',
      fontSize: '4vw',
      flexDirection: 'column',
      alignItems: 'center',
      paddingLeft: '10vw',
      paddingRight: '10vw'
    }}>
      <Container maxWidth="lg"
        style={{ paddingBottom: '5vh' }}>

        <Grid container rowSpacing={{ xs: 5, md: 10 }} columnSpacing={{ xs: 5, md: 16, lg: 26 }}>
          <Grid item xs={12} style={{ textAlign: 'center' }}>
            <div>
              <strong style={{ color: '#FFC72C', fontSize: '3rem' }}>ELC Survey Platform</strong>
            </div>
          </Grid>
          <Grid item xs={12} md={6}>
            <RedButton variant='contained'
              href="student">
              I'm Student
            </RedButton>
          </Grid>
          <Grid item xs={12} md={6}>
            <RedButton variant='contained'
              href="admin">
              I'm Admin
            </RedButton>
          </Grid>
        </Grid>

      </Container>

    </div>
  );
}