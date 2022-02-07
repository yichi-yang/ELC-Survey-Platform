import React from "react";
import TextField from '@mui/material/TextField';
import Button from '@material-ui/core/Button';

export default function AdminLogIn(){

  const textfield = {
    backgroundColor: 'white',
    border:'solid 1px #FFC72C',
    width:'40%',
    margin:'1vw',
    minWidth: '200px'
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
      <div style={{marginBottom:'5vw'}}> 
         <strong style={{color:'#FFC72C', fontSize: '4vw'}}>Admin Login</strong>
      </div>
    
      <TextField id="username" label="Username" variant="filled"  style={textfield}/>
      <TextField id="password" type="password" label="Password" variant="filled"  style={textfield}/>
      
    {/* TODO: @shuyaoxie add href to admin homepage */}
      <Button variant='contained' 
          style={buttonStyle}>
            Login
      </Button>
    </div> 
    
  );
};
