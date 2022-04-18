import React, { useState } from "react";
import TextField from '@mui/material/TextField';
import Button from '@material-ui/core/Button';
import Container from '@mui/material/Container';
import Stack from '@mui/material/Stack';
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function StudentLogIn() {
  const navigate = useNavigate();

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

  const [code, setCode] = useState('');
  const [errorMessage, setErrorMessage] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    enterSurvey();
  }

  function enterSurvey() {
    axios.get(`/api/codes/${code}/`).then(res => {
      if (res.status === 200) {
        navigate(`/survey/${res.data.id}`, { state: { surveyID: res.data.survey } })
      } else {
        setErrorMessage(true);
      }
    }).catch((e) => { }).finally(() => {
      setErrorMessage(true);
    })
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
              ELC Survey Platform
            </strong>
          </div>

          <form onSubmit={handleSubmit}>
            <TextField id="surveyNumber"
              label="Survey Number"
              variant="filled"
              value={code}
              onChange={e => { setCode(e.target.value); setErrorMessage(false) }}
              style={textfield} />

            <div style={{ color: '#FFC72C', fontSize: '1rem', marginTop: '2rem' }} hidden={!errorMessage} >
              Survey Not Found, Please Try Again
            </div>

            <Button variant='contained'
              style={buttonStyle}
              disabled={code.length === 0}
              type='submit'>
              Enter
            </Button>
          </form>
        </Stack>
      </Container>
    </div>
  );
};
