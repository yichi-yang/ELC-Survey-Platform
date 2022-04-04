import React from 'react';
import Button from '@material-ui/core/Button';

export default function StartPage(){
  const buttonStyle = {
    backgroundColor:'#880808', 
    boxShadow:'none',
    color: 'white',
    padding: '5% 5%',
    textTransform: 'none',
    fontSize:'50%',
    margin: '5vw',
    fontWeight: 'bold',
    width:'30%'
  }
  return(
    <div style={{backgroundColor:'#990000', minHeight: '100vh',display:'flex', alignContent: 'center', justifyContent: 'center', fontSize:'4vw', flexDirection:'column', alignItems:'center'}}>
    <div style={{display:'flex', alignContent: 'center', justifyContent: 'center', flexDirection:'column', alignItems:'center', paddingBottom:'5vh', width:'100%'}}>
       <div> 
         <strong style={{color:'#FFC72C'}}>ELC Survey Platform</strong>
      </div>

      <div style={{width:'80%', display:'flex', justifyContent:'center'}}> 
          <Button variant='contained' 
          style={buttonStyle} href="student">
            I'm Student
          </Button>

          <Button variant='contained' 
          style={buttonStyle} href="admin">
            I'm Admin
          </Button>

      </div>

    </div>
    </div>
  );
}