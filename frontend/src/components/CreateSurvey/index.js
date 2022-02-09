import React, { useEffect, useState } from 'react';
import QuestionCreate from './QuestionCreate';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
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
import { useNavigate } from 'react-router-dom';

export default function CreateSurvey(props) {
  const navigate = useNavigate();
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
  };

  const headingButtons = {
    width: '100%',
    display: 'flex',
    justifyContent: 'flex-end',
    position: 'fixed',
    top: '10vh',
    backgroundColor: '#990000',
    paddingRight: '9vw',
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
    width: '60vw',
    textAlign: 'center',
    color: 'white',
    marginTop: '5vh',
  };

  const [shouldRender, setUpdate] = useState(false);

  const types = ['Multiple Choice', 'Selection', 'Short Answer'];

  const [title, setTitle] = useState('Untitled Survey');
  const [description, setDescription] = useState('');
  const [questions, setQuestions] = useState([]);

  const [newQuestion, setNewQuestion] = useState(true);

  const [options, setOptions] = useState([]);

  const [option, setOption] = useState('Add Option');

  const [required, setRequired] = useState(false);

  // const [groupNum, setGroupNum] = useState(1);

  // const [grouped, setGrouped] = useState(false);

  // const [letterGroup, setLetterGroup] = useState(false);

  const iconButtonStyle = {
    margin: '0 0.5vw',
  };

  const [questionType, setType] = useState(0);
  const [question, setQuestion] = useState('Question');
  const typeChange = (event) => {
    reset();
    setType(event.target.value);
  };

  function reset() {
    setType(0);
    setQuestion('Question');
    setOptions([]);
    setOption('Add Option');
    setRequired(false);
  }

  function appendQuestion() {
    let newItem = {
      options: options,
      question: question,
      type: questionType,
      required: required,
    };
    setQuestions(questions.concat(newItem));
  }

  function listOptions(options, questionType) {
    return (
      <div>
        {options.map((q) => {
          return (
            <div style={{ margin: '5px', fontSize: '1.2vw' }}>
              {questionType ? (
                <CropSquareIcon fontSize="1vw" />
              ) : (
                <CircleOutlinedIcon fontSize="1vw" />
              )}
              {q}
            </div>
          );
        })}
      </div>
    );
  }

  function listQuestions() {
    return (
      <div>
        {questions.map((q, i) => {
          return (
            <div style={{ margin: '1vw 4vw' }} key={i}>
              <strong>{i + 1 + '. ' + q.question}</strong>
              {q.required ? '(*)' : ''}
              <Button
                id={i}
                onClick={(e) => {
                  questions.splice(e.target.id, 1);
                  setUpdate(!shouldRender);
                }}
                style={{ color: '#990000', fontSize: '1vw' }}
              >
                Delete
              </Button>
              {q.type === 0 || q.type === 1 ? (
                listOptions(q.options, q.type)
              ) : (
                <div></div>
              )}
              {q.type === 2 ? (
                <textarea
                  disabled={true}
                  style={{
                    border: '1px solid grey',
                    width: '40vw',
                  }}
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
      <div style={headingButtons}>
        <Button
          id="SurveyCreateCancel"
          style={{ color: '#FFC72C' }}
          onClick={(e) => {
            e.preventDefault();
            //TODO:add alert maybe?
            //TODO: change Admin route
            navigate('/Admin');
          }}
        >
          Cancel
        </Button>
        <Button
          id="SurveyCreate"
          disabled={questions.length === 0}
          style={{ color: 'white', fontWeight: 'bold' }}
          onClick={(e) => {
            e.preventDefault();
            //TODO:add alert maybe?
            //TODO: save to db
            //TODO: change Admin route
            navigate('/Admin');
          }}
        >
          Create
        </Button>
      </div>

      <div style={editGround}>
        <input
          type="text"
          value={title}
          style={{
            width: '60%',
            textAlign: 'center',
            border: 'none',
            fontSize: '1.2em',
            color: 'grey',
          }}
          onChange={(e) => setTitle(e.target.value)}
        />

        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <h4 style={{ color: '#990000' }}>Description</h4>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
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
                  <MenuItem value={1}>Selection</MenuItem>
                  <MenuItem value={2}>Short Answer</MenuItem>
                  {/* <MenuItem value={3}>Grid</MenuItem> */}
                </Select>
              </FormControl>
            </div>

            {questionType === 0 || questionType === 1 ? (
              <div>
                {options.map((q) => {
                  return (
                    <div style={{ margin: '5px', fontSize: '1.2vw' }}>
                      {questionType ? (
                        <CropSquareIcon fontSize="1vw" />
                      ) : (
                        <CircleOutlinedIcon fontSize="1vw" />
                      )}
                      {q}
                    </div>
                  );
                })}

                <div style={{ margin: '5px', fontSize: '1.2vw' }}>
                  {questionType ? (
                    <SquareIcon fontSize="1vw" />
                  ) : (
                    <CircleIcon fontSize="1vw" />
                  )}
                  <input
                    type="text"
                    value={option}
                    onChange={(e) => setOption(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter' && option !== '') {
                        setOptions(options.concat(option));
                        setOption('Add Option');
                      }
                    }}
                    style={{
                      width: '50%',
                      border: 'none',
                      borderBottom: 'solid 1px #C4C4C4',
                    }}
                  />
                </div>
              </div>
            ) : (
              <div></div>
            )}

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

            <div
              style={{
                display: 'flex',
                justifyContent: 'flex-end',
                marginTop: '1.5vw',
              }}
            >
              <IconButton
                style={iconButtonStyle}
                disabled={options.length === 0 && questionType !== 2}
                onClick={(e) => {
                  e.preventDefault();
                  //TODO:add to question list
                  appendQuestion();
                  reset();
                  setNewQuestion(false);
                }}
              >
                <DoneOutlineIcon />
              </IconButton>

              <IconButton
                style={iconButtonStyle}
                disabled={options.length === 0}
                onClick={(e) => {
                  e.preventDefault();
                  appendQuestion();
                }}
              >
                <ContentCopyIcon />
              </IconButton>

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

        {/* <div>
          <strong style={{color:'#990000'}}>Divide By</strong>  */}
        {/*           
          <input
                type="text"
                value={groupNum}
                onChange={(e) => {
                  setGroupNum(e.target.value);
                }}
                style={{
                  minHeight: '30px',
                  width: '5%',
                  margin: '2vw',
                  border: 'none',
                  borderBottom: 'solid 1px #C4C4C4',
                }}
              />

<input
                type="text"
                value={}
                onChange={(e) => {
                  setGroupNum(e.target.value);
                }}
                style={{
                  minHeight: '30px',
                  margin: '2vw',
                  border: 'none',
                  borderBottom: 'solid 1px #C4C4C4',
                }}
              /> */}
        {/* </div> */}

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
