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
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Alert from './Alert';
import RankQuestion from './Ranking';

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
    zIndex: '99'
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

  const [shouldRender, setUpdate] = useState(false);

  const types = ['MC', 'CB', 'SA', 'RK'];
  function typeConverter(type) {
    for (let i = 0; i < types.length; i++) {
      if (types[i] === type) return i;
    }
  }

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [questions, setQuestions] = useState([]);

  const [newQuestion, setNewQuestion] = useState(true);

  const [options, setOptions] = useState([]);

  const [option, setOption] = useState('Add Option/Item');

  const [required, setRequired] = useState(false);

  const [groupNum, setGroupNum] = useState(1);

  const [groupName, setGroupName] = useState('Group');

  const [grouped, setGrouped] = useState(false);

  const [groupID, setGroupID] = useState(null);

  const [letterGroup, setLetterGroup] = useState(false);

  const [cancelAlertOpen, setCancelAlertOpen] = useState(false);

  const [createAlertOpen, setCreateAlertOpen] = useState(false);

  const [rankMax, setRankMax] = useState(1.0);
  const [rankMin, setRankMin] = useState(0.0);
  const [rankStep, setRankStep] = useState(1.0);

  const iconButtonStyle = {
    margin: '0 0.5vw',
  };

  const [questionType, setType] = useState(0);
  const [question, setQuestion] = useState('Question');
  const typeChange = (event) => {
    reset();
    setType(event.target.value);
  };

  function alertCancel() {
    setCancelAlertOpen(false);
    setCreateAlertOpen(false);
  }

  function deleteSurvey() {
    axios.delete(`/api/surveys/${surveyID}`).then(() => {
      localStorage.removeItem('surveyID');
      navigate('/template');
    });
  }

  function createComplete() {
    localStorage.removeItem('surveyID');
    navigate('/template');
  }

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

  function createGroupQuestion() {
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
            axios.patch(`/api/surveys/${surveyID}/`,{"group_by_question":res.data.id});
          }

        });
    } else {
      axios.delete(`/api/surveys/${surveyID}/questions/${groupID}/`);
      axios.patch(`/api/surveys/${surveyID}/`,{"group_by_question":null})
    }
    setGrouped(!grouped);
  }

  function patchGroupChoices(letter, name, num) {
    if (grouped) {
      let choices = groupChoices(letter, name, num);
      axios
        .patch(`/api/surveys/${surveyID}/questions/${groupID}/`, {
          choices: choices,
        })
        .then((res) => {});
    }
  }

  function updateGroupQuestionNum(e) {
    if (e.target.value === '') {
      setGroupNum(1);
      setGrouped(false);
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

  function reset() {
    setType(0);
    setQuestion('Question');
    setOptions([]);
    setOption('Add Option/Item');
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

  function deleteQuestion(e) {
    let questionId = questions[e.target.id].id;
    axios
      .delete(`/api/surveys/${surveyID}/questions/${questionId}/`)
      .then((res) => {
        if (res.status === 204) {
          questions.splice(e.target.id, 1);
          setUpdate(!shouldRender);
        }
      });
  }

  function appendQuestion(duplicate = false) {
    let requestContent = {
      number: questions.length + 1 + grouped,
      title: question,
      required: required,
      type: types[questionType],
    };

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

      if (questionType !== 3) {
        ma = undefined;
        mi = undefined;
        st = undefined;
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
        range_default: 1.0,
      };
    }

    axios
      .post(`/api/surveys/${surveyID}/questions/`, requestContent)
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
          setQuestions(questions.concat(newItem));
          if (!duplicate) {
            reset();
            setNewQuestion(false);
          }
        } else {
          //TODO: @shuyaoxie add alert maybe
        }
      });
  }

  function listOptions(options, questionType) {
    return (
      <div>
        {options.map((q, i) => {
          return (
            <div style={{ margin: '5px' }} key={i}>
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

  function listQuestions() {
    return (
      <div>
        {questions.map((q, i) => {
          return (
            <div style={{ margin: '2% 6%' }} key={i}>
              <strong>{i + 1 + '. ' + q.question}</strong>
              {q.required ? '(*)' : ''}
              <Button
                id={i}
                onClick={(e) => {
                  deleteQuestion(e);
                }}
                style={{ color: '#990000', fontSize: '1%' }}
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
                    width: '40%',
                  }}
                />
              ) : (
                <div></div>
              )}

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

  const [surveyID, setSurveyID] = useState(localStorage.getItem('surveyID'));

  useEffect(() => {
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
    } else {
      axios
        .get(`/api/surveys/${surveyID}/`)
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

      axios.get(`/api/surveys/${surveyID}/questions/`).then((res) => {
        if (res.status === 200) {
          let existingQuestions = [];
          let choices = [];
          res.data.forEach((q) => {
            if (q.type === 'DP') {
              setGrouped(true);
              // setGroupID(q.id);
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
          setQuestions(existingQuestions);
        }
      });
    }
  }, []);

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
            setCancelAlertOpen(true);
          }}
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

      <div style={editGround}>
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
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                style={{
                  minHeight: '20px',
                  width: '50%',
                  margin: '0.5vw',
                  border: 'none',
                  borderBottom: 'solid 1px #C4C4C4',
                  fontWeight: 'bold',
                  textAlign: 'center',
                }}
              />

              <FormControl sx={{ m: 1, minWidth: 50 }}>
                <Select
                  defaultValue={0}
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

            {questionType === 0 || questionType === 1 || questionType === 3 ? (
              <div>
                {questionType === 3 ? (
                  <div
                    style={{ display: 'flex', width: '85%', fontSize: '1.2vw' }}
                  >
                    {rankValues(rankMin, 'Minimum', setRankMin, rankMax, '')}
                    {rankValues(rankMax, 'Maximum', setRankMax, '', rankMin)}
                    {rankValues(rankStep, 'Step', setRankStep, '', 1)}
                  </div>
                ) : (
                  <div></div>
                )}

                {options.map((q, i) => {
                  return (
                    <div style={{ margin: '5px', fontSize: '1.2vw' }} key={i}>
                      {questionType === 1 ? (
                        <CropSquareIcon fontSize="1%" />
                      ) : (
                        <CircleOutlinedIcon fontSize="1%" />
                      )}
                      <span style={{ padding: '0.8vw', fontSize: '1vw' }}>
                        {q}
                      </span>
                    </div>
                  );
                })}

                <div
                  style={{
                    margin: '5px',
                    fontSize: '1.2vw',
                    content: 'flex',
                    alignItems: 'center',
                  }}
                >
                  {questionType === 1 ? (
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
                        setOption('');
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
                  appendQuestion();
                }}
              >
                <DoneOutlineIcon />
              </IconButton>

              <IconButton
                style={iconButtonStyle}
                disabled={options.length === 0}
                onClick={(e) => {
                  e.preventDefault();
                  appendQuestion(true);
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

          <input
            type="text"
            value={groupName}
            onChange={(e) => setGroupName(e.target.value)}
            onBlur={(e) => {
              patchGroupChoices(letterGroup, e.target.value, groupNum);
            }}
            style={groupInput}
          />
          <Switch
            checked={grouped}
            onChange={(e) => createGroupQuestion()}
            disabled={groupNum <= 1 && !grouped}
          />
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
