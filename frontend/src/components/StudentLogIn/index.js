import React from "react";
import TextField from '@mui/material/TextField';
import Button from '@material-ui/core/Button';

export default function StudentLogIn(){

  const textfield = {
    backgroundColor: 'white',
    border:'solid 1px #FFC72C',
    width:'40%',
    margin: '5vw',
    marginTop: '7vw'
  }

  const buttonStyle = {
    backgroundColor:'#880808', 
    boxShadow:'none',
    color: 'white',
    padding: '1vw 5vw',
    textTransform: 'none',
    fontSize:'100%',
    margin: '5vw',
    fontWeight: 'bold',
    minWidth: '20%',
  }

  return(
    <div style={{backgroundColor:'#990000', minHeight: '100vh', display: 'flex', alignItems:'center', justifyContent:'center', flexDirection:'column'}}>
      <div> 
         <strong style={{color:'#FFC72C', fontSize: '5vw'}}>ELC Survey Platform</strong>
      </div>

      <TextField id="surveyNumber" label="Survey Number" variant="filled"  style={textfield}/>

    {/* TODO: @shuyaoxie add href to survey */}
      <Button variant='contained' 
          style={buttonStyle}>
            Enter
      </Button>
      
    </div>
    
  );
};
