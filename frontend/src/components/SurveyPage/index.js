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
import axios from 'axios';
import TextField from '@mui/material/TextField';
import FormGroup from '@mui/material/FormGroup';
import Checkbox from '@mui/material/Checkbox';
import { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import { DataObject } from "@mui/icons-material";
import { useLocation } from "react-router-dom";

export default function SurveyPage() {

    const { sessionID } = useParams();

    const location = useLocation();
    const {surveyID} =location.state;

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
        textAlign: 'center',
        color: 'white',
        marginTop: '5vh',
        border: 0,
        height: 40,
        fontSize: '1em',
        cursor: 'pointer'
    };
    /* Survey Title */
    const [title, setTitle] = useState('Survey A');
    /* Group Number */
    const [group, setRoomList] = useState([]);
    /* Change group number */
    const [room, setRoom] = useState('');
    /* Other Questions */
    const [questionList, setQuestionList] = useState([]);
    /* Checkbox Questions */
    const [checkBoxChoices, setCheckBoxChoices] = useState(0);
    /* Dropdown OnChange*/
    const handleRoomChange = (event) => {
        /* Display value on the dropdown */
        setRoom(event.target.value);
        /* Update checkList for submission */
        setCheckList(checkList => {
            let temp = [...checkList];
            let obj = { "question": event.target.name, "choice": event.target.value }
            /* If choosing another option in the same room question, remove the existing option and then append the new option */
            if (checkList.some(item => item.question === event.target.name)) {
                let index = checkList.findIndex(x => x.question === event.target.name);
                temp.splice(index, 1);
                temp.push(obj)
            }
            else {
                temp.push(obj)
            }
            return temp;
        });
    };
    /* @yiwen: Delete after Testing*/
    const [checked, setCheck] = useState({
        option_1: false,
        option_2: false,
        option_3: false,
    });
    /* @yiwen: Delete after Testing*/
    const handleCheckChange = (event) => {
        setCheck({
            ...checked,
            [event.target.name]: event.target.checked,
        });
    };
    /* @yiwen: Delete after Testing*/
    const { op1, op2, op3 } = checked;

    /* Checkbox State in array */
    const [checkList, setCheckList] = useState([])
    const newHandleCheckChange = (event) => {
        setCheckList(checkList => {
            let temp = [...checkList];
            let obj = { "question": event.target.name, "choice": event.target.value }
            /* If the selected choice exist, remove it */
            if (checkList.some(item => item.choice === event.target.value)) {
                let index = checkList.findIndex(x => x.choice === event.target.value);
                temp.splice(index, 1);
            }
            else {
                temp.push(obj)
            }
            return temp;
        });
    };

    const newHandleRadioChange = (event) => {
        setCheckList(checkList => {
            let temp = [...checkList];
            let obj = { "question": event.target.id, "choice": event.target.value }
            /* If choosing another option in the same multiple choice question, remove the existing option and then append the new option */
            if (checkList.some(item => item.question === event.target.id)) {
                let index = checkList.findIndex(x => x.question === event.target.id);
                temp.splice(index, 1);
                temp.push(obj)
            }
            else {
                temp.push(obj)
            }
            return temp;
        });
    };

    const newHandleRankChange = (event) => {
        setCheckList(checkList => {
            let temp = [...checkList];
            let obj = { "question": event.target.id, "choice": event.target.name, "numeric_value": event.target.value }
            /* If choosing another option in the same ranking choice, remove the existing option and then append the new option */
            if (checkList.some(item => item.choice === event.target.name)) {
                let index = checkList.findIndex(x => x.choice === event.target.name);
                temp.splice(index, 1);
                temp.push(obj)
            }
            else {
                temp.push(obj)
            }
            return temp;
        });
    };

    const newHandleTextChange = (event) => {
        setCheckList(checkList => {
            let temp = [...checkList];
            let obj = { "question": event.target.id, "text": event.target.value }
            /* If choosing another option in the same ranking choice, remove the existing option and then append the new option */
            if (checkList.some(item => item.question === event.target.id)) {
                let index = checkList.findIndex(x => x.question === event.target.id);
                temp.splice(index, 1);
                temp.push(obj)
            }
            else {
                temp.push(obj)
            }
            return temp;
        });
    };


    // 测试state用
    /*
    useEffect(() => {
        //console.log("最新值")
        //console.log(checkBoxChoices)
        let temporary = []
        for (var i = 0; i < checkBoxChoices; i++) {
            //console.log('questionList');
            //console.log(questionList);
            temporary.push(false)
        }
        setCheckList([...temporary])
    }, [checkBoxChoices])
    */

    useEffect(() => {
        console.log("checkList最新值")
        console.log(checkList)
    }, [checkList])

    let roomQuestionId = '';
    useEffect(() => {
        axios
            .get(`/api/surveys/${surveyID}/`)
            .then((res) => { setTitle(res.data.title) })
        axios
            .get(`/api/surveys/${surveyID}/questions/`)
            .then((res) => res.data.map((question) => {
                /* Room Number Generator */
                let room_array = [];
                if (question.type === 'DP') {
                    question.choices.map((choice) => {
                        room_array.push(choice.value)
                    });
                    roomQuestionId = question.id;
                    setRoomList([...room_array]);
                }
                setQuestionList(questionList => {
                    return [...questionList, question]
                })

                /* Check box choices Counter */
                if (question.type === 'CB') {
                    let total = checkBoxChoices + question.choices.length;
                    setCheckBoxChoices(total);
                }
            }));
    }, []);

    return (
        <div style={bodyStyle}>
            <div style={headingStyle}>
                <strong>{title}</strong>
            </div>
            <div style={content}>


                {/* Radio group selection */}
                {questionList.map((q) => {
                    if (q.type === 'DP') {
                        return (
                            <div style={questionMargin}>
                                <FormControl style={{ width: '40%' }}>
                                    {/* Room number selection */}
                                    <InputLabel id="demo-simple-select-label">Room Number</InputLabel>
                                    <Select
                                        name={q.id}
                                        value={room}
                                        label="RoomNumber"
                                        onChange={handleRoomChange}
                                    >
                                        {q.choices.map((c) => {
                                            return (
                                                <MenuItem id={q.id} value={c.id}>{c.value}</MenuItem>
                                            );
                                        })}
                                    </Select>
                                </FormControl>
                            </div>
                        )
                    }
                })}

                {questionList.map((q) => {
                    if (q.type === 'MC') {
                        return (
                            <div style={questionMargin}>
                                <FormControl>
                                    <div>Question {q.number}. {q.title}</div>
                                    <RadioGroup
                                        aria-labelledby="demo-radio-buttons-group-label"
                                        defaultValue="female"
                                        name="radio-buttons-group"
                                    >
                                        {q.choices.map((c) => {
                                            return (
                                                <FormControlLabel value={c.value} control={<Radio id={q.id} value={c.id} onChange={newHandleRadioChange} />} label={c.description} />
                                            )
                                        })}
                                    </RadioGroup>
                                </FormControl>
                            </div>
                        );
                    }
                    else if (q.type === 'CB') {
                        return (
                            <div style={questionMargin}>
                                <FormControl component="fieldset" variant="standard">
                                    <div>Question {q.number}. {q.title}</div>
                                    <FormLabel component="legend">You may select more than one options</FormLabel>
                                    <FormGroup>
                                        {
                                            q.choices.map((c, index) => {
                                                let obj = { "question": q.id, "choice": c.id }
                                                return (
                                                    <FormControlLabel
                                                        control={
                                                            <Checkbox checked={checkList.some(item => item.choice === c.id)} onChange={newHandleCheckChange} name={q.id} value={c.id} />
                                                        }
                                                        label={c.description}
                                                    />
                                                );
                                            })}
                                    </FormGroup>
                                </FormControl>
                            </div>
                        );
                    }
                    else if (q.type === 'SA' || q.type === 'PA') {
                        return (
                            <div style={questionMargin}>
                                <div>Question {q.number}. {q.title}</div>
                                <TextField id={q.id} label="Type here..." variant="standard"
                                    style={{ width: '70%' }} onChange={newHandleTextChange} />
                            </div>
                        );
                    }
                    else if (q.type === 'RK') {
                        let choices = [];
                        for (let i = q.range_min; i <= q.range_max; i += q.range_step) {
                            choices.push(i);
                        }
                        return (
                            <div style={questionMargin}>
                                <div>Question {q.number}. {q.title}</div>

                                {q.choices.map((item) => {
                                    return (
                                        <div
                                            style={{ display: 'flex', fontSize: '0.8em', alignItems: 'center' }}
                                        >
                                            <div style={{ fontWeight: 'bold', width: '6em' }}>{item.description}</div>
                                            <FormControl style={{ marginLeft: '2%' }}>
                                                <RadioGroup row name={item.id}>
                                                    {choices.map((i) => {
                                                        return (
                                                            <FormControlLabel
                                                                value={i}
                                                                control={<Radio size="1.8%" id={q.id} name={item.id} value={i} onChange={newHandleRankChange} />}
                                                                label={i}
                                                                key={`${item.id}_${i} `}
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
                })}

                {/* Below is hardcoding MC question, need be deleted after test */}
                <div style={questionMargin}>
                    <FormControl>
                        <div>Question 1</div>
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
                        style={{ width: '70%' }} />
                </div>

                {/* Check box */}
                <div style={questionMargin}>
                    <div>Question 3</div>
                    <FormControl component="fieldset" variant="standard">
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

                <button id="submit" style={submitButton} onClick={() => { console.log('hi') }}>
                    <strong>Submit</strong>
                </button>
            </div>
        </div>
    );
};
