import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import IconButton from '@mui/material/IconButton';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

// to be deleted
const SAs = ["Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.","This is another short answer", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", " Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.","Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "]

const resultArea={
  width:'90%',
  margin:'auto',
  paddingTop: '4%'
}

// TO BE DELETED Onces using .map questions
function title(number, title){
  return(
    <div style={{color:'#990000', margin:'0.8% 0'}}><strong>{number}. </strong>{title}</div>
  )
}


function shortAnswer(answers){
  return(<div style={{display:'flex', flexWrap:'wrap'}}>
    {answers.map((answer,i)=>{
      return(<div style={{margin:'0.3% 1%', fontSize:'0.8em'}}>{`${i+1}. ${answer}`}</div>)
    })}
  </div>);
}

export default function SurveyResult() {

  let { surveyID } = useParams();
  const navigate = useNavigate();
  
  return (
    <div style={{width:'100%'}}>
      
      {/* Heading */}
      <IconButton
          style={{ backgroundColor: '#FFC72C', position:'fix', margin:'3% 0 0 5%' }}
          onClick={() => {navigate('/template');}}>
          <ArrowBackIcon />
      </IconButton>
      <div style={{fontSize: '1.5em',textAlign:'center', margin:'-1%'}}>
        <strong>surveyName</strong>
      </div>
       {/* End Heading */}
      
      {/* Result */}
      <div style={resultArea}>
          
        {/* TODO: map out the results for each questions */}

        {title(1,"Short Answer Question Result Example")}
        {shortAnswer(SAs)}

        
      </div>
      {/* End Result */}

      




    </div>
  );
}
