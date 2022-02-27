import React, {useState} from "react";
import TextField from '@mui/material/TextField';
import Button from '@material-ui/core/Button';
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function StudentLogIn(){
  const navigate = useNavigate();

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

  const [code, setCode] = useState('');
  
  function enterSurvey(){
    axios.get(`/api/codes/${code}/`).then(res=>{
      if(res.status===200){
        navigate(`/survey/${res.data.survey}`);
      }
    }).catch((e)=>{}).finally(()=>{
      // TODO: error message
    })
  }

  return(
    <div style={{backgroundColor:'#990000', minHeight: '100vh', display: 'flex', alignItems:'center', justifyContent:'center', flexDirection:'column'}}>
      <div> 
         <strong style={{color:'#FFC72C', fontSize: '5vw'}}>ELC Survey Platform</strong>
      </div>

      <TextField id="surveyNumber" label="Survey Number" variant="filled" value={code} onChange={e=>setCode(e.target.value)} style={textfield}/>

    {/* TODO: @shuyaoxie add href to survey */}
      <Button variant='contained' 
          style={buttonStyle} onClick={enterSurvey} disabled={code.length===0}>
            Enter
      </Button>
      
    </div>
    
  );
};
