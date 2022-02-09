import React, { useState } from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DoneOutlineIcon from '@mui/icons-material/DoneOutline';
import IconButton from '@mui/material/IconButton';

export default function QuestionCreate(props) {

  const iconButtonStyle = {
    margin:'0 2vw'
  }
  const types = ['Multiple Choice', 'Dropdown', 'Short Answer', 'Grid'];
  const [questionType, setType] = useState(0);
  const [question, setQuestion] = useState('Question');
  const typeChange = (event) => {
    setType(event.target.value);
  };

  function reset(){
    setType(0);
    setQuestion('Question');
  }

  return (
    <div style={{ border: '1px solid #C4C4C4', width: '85%', padding:'1vw' }}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{
            minHeight: '30px',
            width: '50%',
            margin: '2vw',
            border: 'none',
            borderBottom: 'solid 1px #C4C4C4',
          }}
        />

        <FormControl sx={{ m: 1, minWidth: 50 }}>
          <Select
            defaultValue={0}
            onChange={typeChange}
            inputProps={{ 'aria-label': 'Without label' }}
          >
            <MenuItem value={0}>Multiple Choice</MenuItem>
            <MenuItem value={1}>Dropdown</MenuItem>
            <MenuItem value={2}>Short Answer</MenuItem>
            <MenuItem value={3}>Grid</MenuItem>
          </Select>
        </FormControl>
      </div>

          <div style={{display:'flex', justifyContent:'flex-end'}}>

            <IconButton style={iconButtonStyle} onClick={(e) => {
              e.preventDefault();
              //TODO:add to question list
              reset();
              props.setNewQuestion(false);
            }}> <DoneOutlineIcon/> </IconButton>

            <IconButton style={iconButtonStyle} onClick={(e) => {
              e.preventDefault();
              //TODO:add to question list
              props.setNewQuestion(false);
            }}> <ContentCopyIcon/> </IconButton>
            
            <IconButton style={iconButtonStyle} onClick={(e) => {
              e.preventDefault();
              reset();
              props.setNewQuestion(false);
            }}> <DeleteOutlineIcon/> </IconButton>
        
          </div>
    </div>
  );
}
