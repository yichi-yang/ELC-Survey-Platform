import React from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';

export default function RankQuestion(props) {
  let choices = [];
  for (let i = props.min; i <= props.max; i += props.step) {
    choices.push(i);
  }
  let maxWidth = 0;
  props.items.map((item)=>maxWidth=Math.max(maxWidth,item.length));

  return (
    <div>
      {props.items.map((item) => {
        return (
          <div
            style={{ display: 'flex', fontSize: '0.8em', alignItems: 'center' }}
            key={item}
          >
            <div style={{ fontWeight: 'bold', width: `${maxWidth+1}ch` }}>{item}</div>
            <FormControl style={{ marginLeft: '2%' }}>
              <RadioGroup row name={item.id}>
                {choices.map((i) => {
                  return (
                    <FormControlLabel
                      value={i}
                      control={<Radio size="1.5%" />}
                      label={i}
                      disabled={true}
                      key={`${item}_${i} `}
                    />
                  );
                })}
              </RadioGroup>
            </FormControl>
          </div>
        );
      })}
    </div>
  );
}
