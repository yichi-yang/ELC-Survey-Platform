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
import FormGroup from '@mui/material/FormGroup';
import Checkbox from '@mui/material/Checkbox';
import { useState } from 'react';

export default function SurveyPage(){

    const bodyStyle = {
        display: 'flex',
        backgroundColor: '#D1D1D1',
        alighItems: 'center',
        justifyContent: 'center',
        flexWrap: 'wrap',
    }

    const headingStyle = {
        height: '15vh',
        width: '100vw',
        color: 'white',
        backgroundColor: '#990000',
        margin: '0',
        padding: '0',
        fontSize: '1.6em',
        textAlign: 'center',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        top: '0',
      };

    /* Adjust for iPhone minWidth 360 */
    const content = {
        display: 'flex',
        backgroundColor: 'white',
        minHeight: '100vh',
        justifyContent: 'flex-start',
        width: '60%',
        minWidth: 360,
        flexDirection: 'column'
    }

    const questionMargin = {
        flexDirection: 'column',
        margin: '3vw',
    }

    const submitButton = {
        backgroundColor: '#FFC72C',
        width: '100%',
        textAlign: 'center',
        color: 'white',
        marginTop: '5vh',
      };

    const [room, setRoom] = useState('');
    const handleRoomChange = (event) => {
        setRoom(event.target.value);
      };
    const [checked, setCheck] = useState({
        option_1: false,
        option_2: false,
        option_3: false,
    });
    const handleCheckChange = (event) => {
        setCheck({
            ...checked,
            [event.target.name]: event.target.checked,
        });
    };
    const { op1, op2, op3 } = checked;

    return(
    
        <div style={bodyStyle}>
            <div style={headingStyle}>
                Survey A
            </div>
            <div style={content}>
            <div style={questionMargin}>
                <FormControl style={{width: '40%'}}>
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
                </FormControl>
            </div>
                {/* Radio group selection */}
                {/* @yiwenwang Need to figure out how to dynamically generate useState hook */}

                <div style={questionMargin}>
                <FormControl>
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
                </FormControl>
                </div>


                {/* Text field */}
                <div style={questionMargin}>
                    <div>Question 2</div>
                    <TextField id="standard-basic" label="Type here..." variant="standard" 
                    style={{width: '70%'}}/>
                </div>

                {/* Check box */}
                <div style={questionMargin}>
                    <div>Question 3</div>
                    <FormControl sx={{ m: 3 }} component="fieldset" variant="standard">
                        <FormLabel component="legend">You may select more than one options</FormLabel>
                        <FormGroup>
                        <FormControlLabel
                            control={
                            <Checkbox checked={op1} onChange={handleCheckChange} name="option_1" />
                            }
                            label="Option1"
                        />
                        <FormControlLabel
                            control={
                            <Checkbox checked={op2} onChange={handleCheckChange} name="option_2" />
                            }
                            label="Option2"
                        />
                        <FormControlLabel
                            control={
                            <Checkbox checked={op3} onChange={handleCheckChange} name="option_3" />
                            }
                            label="Option3"
                        />
                        </FormGroup>
                    </FormControl>
                </div>
                <Button id="addQuestion" style={submitButton} onClick={() => {}}>
                    <strong>Submit</strong>
                </Button>     
            </div>
        </div>     
    );
};