import React, { useEffect, useState } from 'react';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DoneOutlineIcon from '@mui/icons-material/DoneOutline';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import CircleOutlinedIcon from '@mui/icons-material/CircleOutlined';
import CircleIcon from '@mui/icons-material/Circle';
import CropSquareIcon from '@mui/icons-material/CropSquare';
import SquareIcon from '@mui/icons-material/Square';
import Switch from '@mui/material/Switch';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import Alert from './Alert';
import RankQuestion from './Ranking';
import BackspaceIcon from '@mui/icons-material/Backspace';
import AddBoxIcon from '@mui/icons-material/AddBox';

// Survey edits are stored to database syncrously. When refreshed, created questions and edits should remain
export default function CreateSurvey() {

  const navigate = useNavigate();
  //use the url to determine if it is a survey that needs update
  const { updateID } = useParams();
   
  // Beginning of css styling
  const headingStyle = {
    height: '15vh',
    width: '100vw',
    color: 'white',
    backgroundColor: '#990000',
    margin: '0',
    padding: '0',
    fontSize: '1.6em',
    textAlign: 'center',
    position: 'fixed',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    top: '0',
    zIndex: '98'
  };

  const headingButtons = {
    width: '100%',
    display: 'flex',
    justifyContent: 'flex-end',
    position: 'fixed',
    top: '10vh',
    backgroundColor: '#990000',
    paddingRight: '9vw',
    zIndex: '99'
  };

  const editGround = {
    width: '60vw',
    maxWidth: '900px',
    minHeight: '80vh',
    backgroundColor: 'white',
    paddingTop: '20vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    paddingBottom: '10vh',
  };

  const addQuestion = {
    backgroundColor: '#FFC72C',
    width: '100%',
    textAlign: 'center',
    color: 'white',
    marginTop: '5vh',
  };

  const underLineInput = {
    minHeight: '10px',
    marginLeft: '1vw',
    width: '15%',
    border: 'none',
    borderBottom: 'solid 1px #C4C4C4',
    fontWeight: 'bold',
  };

  const groupInput = {
    minHeight: '10px',
    width: '15%',
    marginLeft: '1vw',
    border: 'none',
    borderBottom: 'solid 1px #C4C4C4',
    color: '#C4C4C4',
    fontWeight: 'bold',
    textAlign: 'center',
  };

  const rankInput = {
    minHeight: '10px',
    width: '30%',
    marginLeft: '1vw',
    border: 'none',
    borderBottom: 'solid 1px #C4C4C4',
    color: '#C4C4C4',
    fontWeight: 'bold',
    textAlign: 'center',
  };
  
  const iconButtonStyle = {
    margin: '0 0.5vw',
  };

  //used for rerender
  const [shouldRender, setUpdate] = useState(false);

  //question types
  const types = ['MC', 'CB', 'SA', 'RK'];
  //return index of the type return from backend
  function typeConverter(type) {
    for (let i = 0; i < types.length; i++) {
      if (types[i] === type) return i;
    }
  }

  const [surveyID, setSurveyID] = useState(localStorage.getItem('surveyID'));

  const [title, setTitle] = useState(''); // survey title

  const [description, setDescription] = useState(''); //survey description

  const [questions, setQuestions] = useState([]); //survey's created questions

  const [newQuestion, setNewQuestion] = useState(true); //whether to show the question create box

  const [groupNum, setGroupNum] = useState(1); //divide survey by group # 

  const [groupName, setGroupName] = useState('Group'); //what groups are called

  const [grouped, setGrouped] = useState(false); //if survey is divided by groups

  const [groupID, setGroupID] = useState(null); //determine if survey is grouped

  const [letterGroup, setLetterGroup] = useState(false); //whether group number is ABCD...

  const [cancelAlertOpen, setCancelAlertOpen] = useState(false); //Alert box for Cancel button

  const [createAlertOpen, setCreateAlertOpen] = useState(false); //for Create button

  const [deleteQuestionIndex, setDeleteQuestionIndex] = useState(-1); // keeps record of the index of the question to be deleted

  const [forceOptionsUpdate, setForceOptionsUpdate] = useState(1);

  const [editQuestion, setEditQuestion] = useState(undefined);

  //hooks for question create
  const [questionType, setType] = useState(0);
  const [question, setQuestion] = useState('');
  const [options, setOptions] = useState([]); //options for MC or CB question
  const [option, setOption] = useState(''); //single option content
  const [required, setRequired] = useState(false); //if question is required or optional
  //hooks for ranking question
  const [rankMax, setRankMax] = useState(1.0);
  const [rankMin, setRankMin] = useState(0.0);
  const [rankStep, setRankStep] = useState(1.0);

  //change question type
  const typeChange = (event) => {
    reset();
    setType(event.target.value);
  };

  function alertCancel() {
    setCancelAlertOpen(false);
    setCreateAlertOpen(false);
    setDeleteQuestionIndex(-1);
  }

  function deleteSurvey() {
    axios.delete(`/api/surveys/${surveyID}/`).then(() => {
      localStorage.removeItem('surveyID');
      navigate('/template');
    });
  }

  //set survey to complete by changing the draft status and localstorage of the survey's ID
  function createComplete() {
    axios.patch(`/api/surveys/${surveyID}/`,{"draft": false}).then(res=>{
      if(res.status===200){
        if(updateID!=='new'){
          axios.delete(`/api/surveys/${updateID}/`).then(()=>{
            localStorage.removeItem('surveyID');
            navigate('/template');
          })}else{
            localStorage.removeItem('surveyID');
            navigate('/template');
          }
      }else{
        window.location.reload();
      }
    }
    )
  }

  //converter for groupedQuestion API call
  function groupChoices(letter, name, number) {
    let groups = [];
    for (let i = 1; i <= number; i++) {
      let v = i.toString();
      if (letter) {
        v = String.fromCharCode('A'.charCodeAt() + i - 1);
      }
      groups.push({
        value: v,
        description: `${name} ${v}`,
      });
    }
    return groups;
  }

  //change groupQuestion status (Create OR Delete)
  function patchGroupQuestion() {
    if (!grouped) {
      let groups = groupChoices(letterGroup, groupName, groupNum);
      axios
        .post(`/api/surveys/${surveyID}/questions/`, {
          number: questions.length + 1,
          title: `Which ${groupName} are you in?`,
          required: true,
          type: 'DP',
          choices: groups,
        })
        .then((res) => {
          if (res.status === 201) {
            setGroupID(res.data.id);
            //update the new group_by_question ID to survey's entity
            axios.patch(`/api/surveys/${surveyID}/`,{"group_by_question":res.data.id});
          }else{
            window.location.reload();
          }
        });
    } else {
      axios.delete(`/api/surveys/${surveyID}/questions/${groupID}/`);
      axios.patch(`/api/surveys/${surveyID}/`,{"group_by_question":null})
    }
    setGrouped(!grouped);
  }

  //API call to change group name/number/alphabet_or_not
  function patchGroupChoices(letter, name, num) {
    if (grouped) {
      let choices = groupChoices(letter, name, num);
      axios
        .patch(`/api/surveys/${surveyID}/questions/${groupID}/`, {
          choices: choices,
          title: `Which ${name} are you in?`,
        })
        .then((res) => {});
    }
  }

  //handle changes to group number
  function updateGroupQuestionNum(e) {
    //if value is empty, then reset to groupnum==1 and disable the groupQuestion
    if (e.target.value === '') {
      setGroupNum(1);
      setGrouped(false);
      axios.delete(`/api/surveys/${surveyID}/questions/${groupID}/`);
    } else {
      try {
        let num = e.target.value;
        if (num > 1) {
          if (grouped && num > 1)
            patchGroupChoices(letterGroup, groupName, num);
        } else {
          setGrouped(false);
          setGroupNum(1);
          axios.delete(`/api/surveys/${surveyID}/questions/${groupID}/`);
        }
      } catch {}
    }
  }

  //reset the NEW Question create states
  function reset() {
    setType(0);
    setQuestion('');
    setOptions([]);
    setOption('');
    setRequired(false);
    setRankMax(1);
    setRankMin(0);
    setRankStep(1);
  }

  function updateTitle(e) {
    let value = e.target.value;
    if (value.length === 0) value = 'Untitled Survey';
    if (value !== title) {
      setTitle(value);
      axios.patch(`/api/surveys/${surveyID}/`, { title: value });
    }
  }

  const updateDescription = (e) => {
    let value = e.target.value;
    setDescription(value);
    axios
      .patch(`/api/surveys/${surveyID}/`, { description: e.target.value })
      .then();
  };

  //remove the question from created list 
  function deleteQuestion() {
    let questionId = questions[deleteQuestionIndex].id;
    axios
      .delete(`/api/surveys/${surveyID}/questions/${questionId}/`)
      .then((res) => {
        if (res.status === 204) {
          questions.splice(deleteQuestionIndex, 1);
          setUpdate(!shouldRender);
          setDeleteQuestionIndex(-1); //reset to -1 for index to close alert box
        }else {
          window.location.reload();
        }
      });
  }

  // set question's states for editing question in the box
  function editOnclick(i){
    let item = questions[i];
    setEditQuestion(i);
    setOptions([...questions[i].options]); //deep copy
    setType(item.type);
    setRequired(item.required);
    setQuestion(item.question);
    setRankMax(item.range_max);
    setRankMin(item.range_min);
    setRankStep(item.range_step);
    setOption('');
    setNewQuestion(true); //open the question edit box 
  } 

  // update the question to the database after edits
  function updateQuestion(duplicate=false, requestBody){
    axios.put(`/api/surveys/${surveyID}/questions/${questions[editQuestion].id}/`, requestBody).then(res=>{
      if (res.status === 200) {
        let newItem = {
          options: options,
          question: question,
          type: questionType,
          required: required,
          id: res.data.id,
          range_min: rankMin,
          range_max: rankMax,
          range_step: rankStep,
        };

        let tmp = [...questions];
        tmp[editQuestion]=newItem;
        setQuestions(tmp); //update to question list
        setEditQuestion(undefined); //change the edit status back to undefined
       
        if (!duplicate) { 
          reset(); //if duplicate is not clicked, then just reset the question's statuses
          setNewQuestion(false);
        }else{ // otherwise, post a new question
          appendQuestion(false,requestBody);
        }

      } else {
        window.location.reload();
      }
  });
  }

  // append newly created option item to list
  function addOption(){
    setOptions(options.concat(option));
    setOption('');
  }


  //edit created Option's content (Onchange)
  function editOption(e,i){
    options[i]=e.target.value;
    // force rerender once updated
    setForceOptionsUpdate(forceOptionsUpdate+1);
  }

  //delete a created option
  function deleteOption(i){
    options.splice(i,1);
    // force rerender once updated
    setForceOptionsUpdate(forceOptionsUpdate+1);
  }

  function finishQuestion(duplicate = false) {
    //Prepare API request content
    let requestContent = {
      number: questions.length + 1,
      title: question,
      required: required,
      type: types[questionType],
    };

    //Anything that is not a short answer type
    if (questionType !== 2) {
      let parsedOptions = [];
      for (let i = 0; i < options.length; i++) {
        parsedOptions.push({
          value: (i + 1).toString(),
          description: options[i],
        });
      }

      let ma = rankMax;
      let mi = rankMin;
      let st = rankStep;
      let rd = 1.0;

      //for non-ranking question
      if (questionType !== 3) {
        ma = undefined;
        mi = undefined;
        st = undefined;
        rd = undefined;
      }

      requestContent = {
        number: questions.length + 1,
        title: question,
        required: required,
        type: types[questionType],
        choices: parsedOptions,
        range_min: mi,
        range_max: ma,
        range_step: st,
        range_default: rd,
      };
    }
    
    console.log(editQuestion);
    //If it is updating a question
    if(editQuestion!==undefined){
      updateQuestion(duplicate,requestContent);
    }
    // otherwise, create a new question
    else{
      appendQuestion(duplicate, requestContent);
    }
  }

   //apped to question list when a new question is created
  function appendQuestion(duplicate = false, requestBody){
    console.log(requestBody);
    axios
      .post(`/api/surveys/${surveyID}/questions/`, requestBody)
      .then((res) => {
        if (res.status === 201) {
          let newItem = {
            options: options,
            question: question,
            type: questionType,
            required: required,
            id: res.data.id,
            range_min: rankMin,
            range_max: rankMax,
            range_step: rankStep,
          };
          setQuestions(questions.concat(newItem)); //add to question list
          if (!duplicate) { //if not duplicate, reset states and close question creation box
            reset();
            setNewQuestion(false);
          }
        } else {
          window.location.reload();
        }
      });
  }

  //list options for each created question
  function listOptions(options, questionType) {
    return (
      <div>
        {options.map((q, i) => {
          return (
            <div style={{ margin: '1px 5px', display:"flex", alignItems:'center' }} key={i}>
              {questionType ? (
                <CropSquareIcon fontSize="1%" />
              ) : (
                <CircleOutlinedIcon fontSize="1%" />
              )}
              <span style={{ padding: '0.5vw', fontSize: '90%' }}>{q}</span>
            </div>
          );
        })}
      </div>
    );
  }

  //list created questions
  function listQuestions() {
    return (
      <div>
         <Alert
          id="deleteAlert"
          open={deleteQuestionIndex>-1}
          message="Are you sure you want to delete this question?"
          content="Once confirmed, it will be discarded"
          choiceOne="No"
          choiceTwo="Yes"
          handleOne={alertCancel}
          close={alertCancel}
          handleTwo={deleteQuestion}
        />
        {questions.map((q, i) => {
          return (
            <div style={{ margin: '2% 6%', width:'90vw' }} key={i}>
              <strong>{i + 1 + '. ' + q.question}</strong>
              {/* if required */}
              {q.required ? '(*)' : ''}  
              <Button
                id={i}
                onClick={(e) => {
                 setDeleteQuestionIndex(i);
                }}
                size='small'
                style={{ color: 'grey',marginLeft:'1.5%' }}
              >
                Delete
              </Button>
              <Button onClick={e=>editOnclick(i)} size='small' style={{color:'#990000'}}>
                Edit
              </Button>
              {/* for multiple choice and selections */}
              {q.type === 0 || q.type === 1 ? (
                listOptions(q.options, q.type)
              ) : (
                <div></div>
              )}
              {/* for short answer */}
              {q.type === 2 ? (
                <textarea
                  disabled={true}
                  style={{
                    border: '1px solid grey',
                    width: '40%',
                  }}
                />
              ) : (
                <div></div>
              )}
              {/* for ranking question */}
              {q.type === 3 ? (
                <RankQuestion
                  key={q.id}
                  min={q.range_min}
                  max={q.range_max}
                  step={q.range_step}
                  items={q.options}
                  disable={true}
                />
              ) : (
                <div></div>
              )}
            </div>
          );
        })}
      </div>
    );
  }

  function rankValues(stateValue, name, stateChange, maxi, mini) {
    return (
      <div style={{ margin: '1%' }}>
        {name}:
        <input
          id={name}
          type="number"
          value={stateValue}
          onChange={(e) => {
            if (e.target.value) stateChange(parseFloat(e.target.value));
          }}
          max={maxi}
          min={mini}
          style={rankInput}
        />
      </div>
    );
  }

  // initial works for setting up the survey-create page.
  useEffect(() => {
    //if this is not refresh (no id in localstorage)
    if (surveyID === null || surveyID === 'null') {
      setTitle('Untitled Survey');
      axios
        .post('/api/surveys/', {
          title: 'Untitled Survey',
          description: description,
        })
        .then((response) => {
          if (response.status !== 201) {
            navigate('/admin');
          }
          setSurveyID(response.data.id);
          localStorage.setItem('surveyID', response.data.id);
        })
        .catch(() => {
          window.location.reload();
        });
    } 
    //if it is existing survey
    else { 
      axios.get(`/api/surveys/${surveyID}/`) //get survey
        .then((res) => {
          if (res.status === 200) {
            setTitle(res.data.title);
            setDescription(res.data.description);
            setGroupID(res.data.group_by_question);
          }
        })
        .catch(() => {
          localStorage.removeItem('surveyID');
          window.location.reload();
        });
      //get survey questions
      axios.get(`/api/surveys/${surveyID}/questions/`).then((res) => {
        if (res.status === 200) {
          let existingQuestions = [];
          let choices = [];
          res.data.forEach((q) => {
            // if this question is a group_by_question, set the states correspondingly
            if (q.type === 'DP') {
              setGrouped(true);
              setGroupID(q.id);
              setGroupNum(q.choices.length);
              let tmp = q.choices[0].description;
              let cut = q.choices.length.toString.length + 1;
              if (tmp[tmp.length - 1] === 'A') {
                setLetterGroup(true);
                cut = 2;
              }
              setGroupName(tmp.substr(0, tmp.length - cut));
            } else {
              choices = [];
              if (q.choices)
                q.choices.forEach((c) => choices.push(c.description));
              existingQuestions.push({
                options: choices,
                question: q.title,
                type: typeConverter(q.type),
                required: q.required,
                id: q.id,
                range_max: q.range_max,
                range_min: q.range_min,
                range_step: q.range_step,
              });
            }
          });
          setQuestions(existingQuestions); //update the questions state
        }
      });
    }
  }, []);

  // Beginning of the HTMLs
  return (
    <div
      style={{
        padding: '0',
        backgroundColor: '#C4C4C4',
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      <div style={headingStyle}>
        <strong>Survey Template Creation</strong>
      </div>
      {/* Create and Cancel buttons for survey */}
      <div style={headingButtons}>
        <Button
          id="SurveyCreateCancel"
          style={{ color: '#FFC72C' }}
          onClick={(e) => {
            setCancelAlertOpen(true);
          }}
          size='medium'
        >
          Cancel
        </Button>
        <Alert
          id="cancelAlert"
          open={cancelAlertOpen}
          message="Are You Sure You Want To Cancel?"
          content="This Survey Will Be Discarded If Confirmed"
          choiceOne="No"
          choiceTwo="Yes"
          handleOne={alertCancel}
          close={alertCancel}
          handleTwo={deleteSurvey}
        />
        <Button
          id="SurveyCreate"
          disabled={questions.length === 0}
          style={questions.length ? { color: 'white', fontWeight: 'bold' } : {}}
          onClick={() => setCreateAlertOpen(true)}
          size='medium'
        >
          Create
        </Button>
        <Alert
          id="createAlert"
          open={createAlertOpen}
          message="Have You Finished Editing The Survey?"
          content="This Survey Will Be Created If Confirmed"
          choiceOne="No"
          choiceTwo="Yes"
          handleOne={alertCancel}
          close={alertCancel}
          handleTwo={createComplete}
        />
      </div>

{/* Beginning of the edit area */}
      <div style={editGround}>
        {/* title input */}
        <input
          type="text"
          defaultValue={title}
          style={{
            width: '60%',
            textAlign: 'center',
            border: 'none',
            fontSize: '1.2em',
            color: 'grey',
          }}
          onBlur={(e) => updateTitle(e)}
        />
{/* description input */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-evenly',
            alignItems: 'center',
            width: '95%',
            marginLeft: '3%',
          }}
        >
          <h4 style={{ color: '#990000' }}>Description</h4>
          <textarea
            defaultValue={description}
            onBlur={updateDescription}
            style={{
              border: '1px solid grey',
              minHeight: '30px',
              width: '40vw',
              margin: '2vw',
            }}
          />
        </div>

        {/* list created questions */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-start',
            width: '100%',
          }}
        >
          {shouldRender && listQuestions()}
          {!shouldRender && listQuestions()}
        </div>
        
        {/* Create Question */}
        {newQuestion ? (
          <div
            style={{
              border: '1px solid #C4C4C4',
              width: '85%',
              padding: '1vw',
              marginTop: '2vw',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
              }}
            >
            <div style={{ width: '70%', display:'flex', flexWrap:'nowrap', alignItems:'flex-end', margin:'0.5vw'}}>
              <div><strong>Question:</strong></div>
              {/* Question content */}
              <input
                name='question'
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                style={{
                  minHeight: '20px',
                  width:'70%',
                  marginLeft: '0.5vw',
                  border: 'none',
                  borderBottom: 'solid 1px #C4C4C4',
                  fontWeight: 'bold',
                  textAlign: 'center',
                }}
              />
            </div>
            {/* Droptdown box for question types */}
              <FormControl sx={{ m: 1, minWidth: 50 }}>
                <Select
                  value={questionType}
                  onChange={typeChange}
                  inputProps={{ 'aria-label': 'Without label' }}
                  style={{ height: '3vw' }}
                >
                  <MenuItem value={0}>Multiple Choice</MenuItem>
                  <MenuItem value={1}>Selection</MenuItem>
                  <MenuItem value={2}>Short Answer</MenuItem>
                  <MenuItem value={3}>Ranking</MenuItem>
                  {/* <MenuItem value={3}>Grid</MenuItem> */}
                </Select>
              </FormControl>
            </div>
            
            {/* Non-Short-Answer types */}
            {questionType === 0 || questionType === 1 || questionType === 3 ? (
              <div>
                {/* Ranking */}
                {questionType === 3 ? (
                  <div
                    style={{ display: 'flex', width: '85%', fontSize: '1.2vw' }}
                  >
                    {rankValues(rankMin, 'Minimum', setRankMin, rankMax, '')}
                    {rankValues(rankMax, 'Maximum', setRankMax, '', rankMin)}
                    {/* {rankValues(rankStep, 'Step', setRankStep, '', 1)}  */}
                    {/* This section is commented out per request. */}
                  </div>
                ) : (
                  <div></div>
                )}
                {/* list created options */}
                {options.map((q, i) => {
                  return (
                    <div style={{ margin: '1px 5px', fontSize: '1.2vw', display:"flex", width:'95%', alignItems:'center', borderBottom:'0.5px solid #C4C4C4' }} key={i}>
                      {/*display different icon by question types  */}
                      {questionType === 1 ? (
                        <CropSquareIcon fontSize="1%" />
                      ) : (
                        <CircleOutlinedIcon fontSize="1%" />
                      )}
                      {/* show each created option as input box for possible edits */}
                      <input type="text" value={q}
                        style={{marginLeft:'0.5vw', paddingLeft:'0.5vw',border: 'none', width:`${(q.length+1)*8}px`, maxWidth:'90%'}} 
                        onChange={e=>editOption(e,i)}></input>
                      {/* option delete button */}
                      <IconButton style={{color:'#990000'}} onClick={e=>deleteOption(i)}><BackspaceIcon style={{fontSize:'65%'}}/></IconButton>
                    </div>
                  );
                })}

              {/* New Option Entering Field */}
                <div
                  style={{
                    margin: '5px',
                    content: 'flex',
                    alignItems: 'center',
                    width:'95%'
                  }}
                >
                  {questionType === 1 ? (
                    <SquareIcon fontSize="1%" />
                  ) : (
                    <CircleIcon fontSize="1%" />
                  )}
                  <input
                    type="text"
                    value={option}
                    placeholder="Add Option/Item Here"
                    onChange={(e) => setOption(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter' && option !== '') {
                        addOption();
                      }
                    }}
                    style={{
                      width: '50%',
                      border: 'none',
                      borderBottom: 'solid 1px #C4C4C4',
                      fontWeight: 'bold',
                      margin: '0.5vw 0 0 0.5vw',
                      paddingLeft: '0.5vw',
                    }}
                  />
                   <IconButton style={option===''?{color:'grey'}:{color:'#1976d2'}} onClick={addOption} disabled={option===''}><AddBoxIcon style={{fontSize:'65%'}}/></IconButton>
                </div>
              </div>
            ) : (
              <div></div>
            )} {/* End of Non-Short-Answer types */}

            {/* For short Answer */}
            {questionType === 2 ? (
              <div
                style={{
                  borderBottom: 'solid 1px #C4C4C4',
                  width: '50%',
                  margin: '2vw',
                  fontSize: '1vw',
                }}
              >
                Short answer text
              </div>
            ) : (
              <div></div>
            )}

            {/* Icon buttons */}
            <div
              style={{
                display: 'flex',
                justifyContent: 'flex-end',
                marginTop: '1.5vw',
              }}
            >
              <IconButton
                style={iconButtonStyle}
                disabled={question.length===0||(options.length === 0 && questionType !== 2)}
                onClick={(e) => {
                  e.preventDefault();
                  finishQuestion();
                }}
              >
                <DoneOutlineIcon />
              </IconButton>

              {/* Append the question to questions list, and keep the question-create-box with the same states of the contents */}
              <IconButton
                style={iconButtonStyle}
                disabled={question.length===0||(options.length === 0 && questionType !== 2)}
                onClick={(e) => {
                  e.preventDefault();
                  finishQuestion(true);
                }}
              >
                <ContentCopyIcon />
              </IconButton>

              {/* reset states of the question contents if delete, close the box  */}
              <IconButton
                style={iconButtonStyle}
                onClick={(e) => {
                  e.preventDefault();
                  reset();
                  setNewQuestion(false);
                }}
              >
                <DeleteOutlineIcon />
              </IconButton>
              
              {/* Toggle for whether the question is required */}
              <div
                style={{ borderLeft: '1px solid #C4C4C4', paddingLeft: '1vw' }}
              >
                Required
                <Switch
                  checked={required}
                  onChange={() => {
                    setRequired(!required);
                  }}
                />
              </div>
            </div>
          </div>
        ) : (
          <div></div>
        )}
        {/* END of Create Question */}
        
        {/* Group_by question */}
        <div
          style={{
            margin: '3vw 1vw 0vw 3vw',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'left',
            alignItems: 'center',
          }}
        >
          <strong style={{ color: '#990000' }}>Divide By</strong>
          {/* number input for number of groups */}
          <input
            id="SurveyGroupedNumber"
            type="number"
            min="1"
            max="30"
            value={groupNum}
            onChange={(e) => setGroupNum(e.target.value)}
            onBlur={(e) => updateGroupQuestionNum(e)}
            style={groupInput}
          />
          {/* How is the group calls (group, team, section, ect) */}
          <input
            type="text"
            value={groupName}
            onChange={(e) => setGroupName(e.target.value)}
            onBlur={(e) => {
              patchGroupChoices(letterGroup, e.target.value, groupNum);
            }}
            style={groupInput}
          />
          {/* On or Off for this group_by question */}
          <Switch
            checked={grouped}
            onChange={(e) => patchGroupQuestion()}
            disabled={groupNum <= 1 && !grouped}
          />

          {/* Whether this question's group enumeration should be in number or alphabet order */}
          <strong style={{ color: '#C4C4C4' }}> in alphabet</strong>
          <Switch
            checked={letterGroup}
            onChange={(e) => {
              patchGroupChoices(!letterGroup, groupName, groupNum);
              setLetterGroup(!letterGroup);
            }}
            disabled={groupNum <= 1 && !grouped}
          />
        </div> 
        {/* End of group_by question */}

        {/* Opens the 'Create Quesion' box */}
        <Button
          id="addQuestion"
          style={addQuestion}
          onClick={() => {
            if (newQuestion == false) setNewQuestion(true);
          }}
        >
          <strong>Add Question</strong>
        </Button>
        
      </div>
    </div>
  );
}
