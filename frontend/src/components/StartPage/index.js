import React from 'react';
import Button from '@material-ui/core/Button';
// import {Link} from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';

export default function StartPage(){
  const buttonStyle = {
    backgroundColor:'#880808', 
    boxShadow:'none',
    color: 'white',
    padding: '5vw 7vw',
    textTransform: 'none',
    fontSize:'60%',
    margin: '5vw',
    fontWeight: 'bold',
    maxWidth: '500px',

  }
  return(
    <div style={{backgroundColor:'#990000', minHeight: '100vh',display:'flex', alignContent: 'center', justifyContent: 'center', fontSize:'4vw', flexDirection:'column', alignItems:'center'}}>
    <div style={{maxWidth:'1300px',display:'flex', alignContent: 'center', justifyContent: 'center', flexDirection:'column', alignItems:'center', paddingBottom:'5vh'}}>
       <div> 
         <strong style={{color:'#FFC72C'}}>ELC Survey Platform</strong>
      </div>

      <div> 
          <Button variant='contained' 
          style={buttonStyle}>
            I'm Student
          </Button>

          <Button variant='contained' 
          style={buttonStyle}>
            I'm Admin
          </Button>

      </div>

    </div>
    </div>
  );
}