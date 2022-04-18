import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@material-ui/core/Button';
import Container from '@mui/material/Container';
import Stack from '@mui/material/Stack';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { TokenStorage } from '../../utils';

export default function AdminLogIn() {
  let navigate = useNavigate();

  const textfield = {
    backgroundColor: 'white',
    border: 'solid 1px #FFC72C',
    width: '100%',
    marginTop: '3rem',
    minWidth: '200px'
  };

  const buttonStyle = {
    backgroundColor: '#880808',
    boxShadow: 'none',
    color: 'white',
    lineHeight: '3rem',
    textTransform: 'none',
    fontSize: '1rem',
    marginLeft: 'auto',
    marginRight: 'auto',
    marginTop: '4rem',
    fontWeight: 'bold',
    width: '100%',
    maxWidth: '20rem'
  };

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    logIn();
  }

  function logIn() {
    axios.post(
      '/api/auth/login/',
      { username: username, password: password },
      { useJWT: false }
    ).then((res) => {
      if (res.status === 200 && res.data.access_token) {
        console.log(res);
        TokenStorage.setAccessToken(res.data.access_token);
        TokenStorage.setRefreshToken(res.data.refresh_token);
        navigate('/template');
      } else {
        setErrorMessage(true);
      }
    }).catch((error) => { console.log(error); setErrorMessage(true) });
  }

  function changePassword(e) {
    setErrorMessage(false);
    setPassword(e.target.value);
  }

  function changeUsername(e) {
    setErrorMessage(false);
    setUsername(e.target.value);
  }

  return (
    <div
      style={{
        backgroundColor: '#990000',
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        paddingLeft: '10vw',
        paddingRight: '10vw'
      }}
    >

      <Container maxWidth="sm" style={{ width: '100%' }}>
        <Stack align="center">
          <div style={{ marginBottom: '1rem', textAlign: "center" }}>
            <strong style={{ color: '#FFC72C', fontSize: '3rem', }}>
              Admin Login
            </strong>
          </div>

          <form onSubmit={handleSubmit}>
            <TextField
              id="username"
              label="Username"
              variant="filled"
              style={textfield}
              value={username}
              onChange={changeUsername}
            />
            <TextField
              id="password"
              type="password"
              label="Password"
              variant="filled"
              style={textfield}
              value={password}
              onChange={changePassword}
            />

            <div style={{ color: '#FFC72C', fontSize: '1rem', marginTop: '2rem' }} hidden={!errorMessage} >
              Incorrect Password or Username, Please Try Again
            </div>

            <Button variant="contained" style={buttonStyle} type="submit">
              Login
            </Button>
          </form>
        </Stack>
      </Container>
    </div>
  );
}
