import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@material-ui/core/Button';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { TokenStorage } from '../../utils';

export default function AdminLogIn() {
  let navigate = useNavigate();

  const textfield = {
    backgroundColor: 'white',
    border: 'solid 1px #FFC72C',
    width: '40%',
    margin: '1vw',
    minWidth: '200px',
  };

  const buttonStyle = {
    backgroundColor: '#880808',
    boxShadow: 'none',
    color: 'white',
    padding: '1vw 5vw',
    textTransform: 'none',
    fontSize: '100%',
    margin: '5vw',
    fontWeight: 'bold',
    minWidth: '20%',
  };

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  function logIn() {
    axios.post('/api/auth/login/', { username: username, password: password })
      .then((res) => {
        if (res.status === 200 && res.data.access_token) {
          console.log(res);
          TokenStorage.setAccessToken(res.data.access_token);
          TokenStorage.setRefreshToken(res.data.refresh_token);
          navigate('/template');
        }
      }).catch((error)=>{console.log(error)});
  }

  function changePassword(e) {
    setPassword(e.target.value);
  }

  function changeUsername(e) {
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
      }}
    >
      <div style={{ marginBottom: '5vw' }}>
        <strong style={{ color: '#FFC72C', fontSize: '4vw' }}>
          Admin Login
        </strong>
      </div>

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

      <Button variant="contained" style={buttonStyle} onClick={logIn}>
        Login
      </Button>
    </div>
  );
}
