import React from "react";
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import FormLabel from '@mui/material/FormLabel';
import RadioGroup from '@mui/material/RadioGroup';
import Radio from '@mui/material/Radio';
import FormControlLabel from '@mui/material/FormControlLabel';
import Button from '@material-ui/core/Button';
import TextField from '@mui/material/TextField';
import { Text } from "react-native";
import { useState } from 'react';

export default function SurveyPage(){

    const bodyStyle = {
            display: 'flex',
            backgroundColor: '#D1D1D1',
            alighItems: 'center',
            justifyContent: 'center',
            flexWrap: 'wrap'
    }

    const headlineStyle = {
        display: 'flex',
        backgroundColor: '#990000',
        alighItems: 'center',
        justifyContent: 'center',
        width: '100%',
        height: 80
    }

    const textStyle = {
        fontSize: 28,
        color: 'white',
        alighItems: 'center'
    }

    const buttonStyle = {
        backgroundColor:'#FFC72C', 
        boxShadow:'none',
        color: 'white',
        fontWeight: 'bold',
        width:'100%',
        height: '8vh',
    }

    /* Adjust for iPhone minWidth 360 */
    const content = {
        display: 'flex',
        backgroundColor: 'white',
        minHeight: '100vh',
        justifyContent: 'flex-start',
        width: '60%',
        minWidth: 360,
        flexWrap: 'wrap'
    }
    const questionField = {
        margin: '3vw',
        justifyContent: 'flex-start',
        width: '50%'
    }

    const [room, setRoom] = useState('');
    const handleRoomChange = (event) => {
        setRoom(event.target.value);
      };

    return(
    
        <div style={bodyStyle}>
            <div style={headlineStyle}>
                <Text style={textStyle}>
                    Survey A
                </Text>
            </div>
            <div style={content}>
                <FormControl style={questionField}>
                    {/* Room number selection */}
                    <InputLabel id="demo-simple-select-label">Room Number</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={room}
                        label="RoomNumber"
                        onChange={handleRoomChange}
                    >
                        <MenuItem value={'A'}>A</MenuItem>
                        <MenuItem value={'B'}>B</MenuItem>
                        <MenuItem value={'C'}>C</MenuItem>
                        <MenuItem value={'D'}>D</MenuItem>
                        <MenuItem value={'E'}>E</MenuItem>
                        <MenuItem value={'F'}>F</MenuItem>
                    </Select>

                    {/* Radio group selection */}
                    {/* @yiwenwang Need to figure out how to dynamically generate useState hook */}
                    <FormLabel id="demo-radio-buttons-group-label">Question 1</FormLabel>
                    <RadioGroup
                        aria-labelledby="demo-radio-buttons-group-label"
                        defaultValue="female"
                        name="radio-buttons-group"
                    >
                        <FormControlLabel value="female" control={<Radio />} label="Female" />
                        <FormControlLabel value="male" control={<Radio />} label="Male" />
                        <FormControlLabel value="other" control={<Radio />} label="Other" />
                    </RadioGroup>

                    {/* Text field */}
                    <TextField id="standard-basic" label="Standard" variant="standard" />
                </FormControl>
            </div>
        </div>
        
        
    );
};
