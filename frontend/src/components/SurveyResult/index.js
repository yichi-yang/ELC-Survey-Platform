import React, { useState, useEffect } from 'react';
import PieChart from './PieChart';
import DataTable from './table';
import { useParams, useNavigate } from 'react-router-dom';
import IconButton from '@mui/material/IconButton';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CircularProgress from '@mui/material/CircularProgress';
import axios from 'axios';

const data = [65, 59, 80, 81, 56];

const resultArea = {
  width: '90%',
  margin: 'auto',
  paddingTop: '4%',
};

function title(number, title) {
  return (
    <div style={{ color: '#990000', margin: '0.8% 0' }}>
      <strong>{number}. </strong>
      {title}
    </div>
  );
}

export default function SurveyResult() {
  let { surveyID } = useParams();
  const navigate = useNavigate();
  const [session, setSession] = useState(null);
  const [summary, setSummary] = useState(null);
  const [count, setCount] = useState(0);
  const [groups, setGroups] = useState([]);
  const [surveyName, setSurveyName] = useState('');


  //Load summary data
  useEffect(() => {
    axios
      .get(`/api/sessions/?survey=${surveyID}`)
      .then(response => {
        if (response.data.results.length == 0) {
          setSession(false);
        } else {
          const sessionID = response.data.results[0].id;
          return axios
            .get(`/api/sessions/${sessionID}/submissions/summarize/`)
            .then((response) => {
              setSession(true);
              setSummary(response.data.question_summary);
              setCount(response.data.submission_count);
              setSurveyName(response.data.survey.title);
              if (response.data.group_by_question) {
                setGroups(response.data.group_by_question.choices);
              }
              //  The group choices: Array(2)
              // 0: {id: 'PyplYyj', value: 'A', description: 'Team A'}
              // 1: {id: '4NJMYOp', value: 'B', description: 'Team B'}
            });
        }
      });
  }, []);

  function shortAnswer(answers) {
    const answerList = (list) => {

      if (list.length === 0) {
        return <div style={{ color: 'grey', fontSize: '0.8em', margin: '0.3% 1%' }}>No Answers Yet</div>
      } else {
        return (
          list.map((answer, i) => {
            return (
              <div
                style={{ margin: '0.3% 1%', fontSize: '0.8em' }}
                key={i}
              >{`${i + 1}. ${answer}`}</div>
            );
          })
        )
      }
    }
    return (
      <div>
        {answers.by_group ? <div>
          {groups.map(group => (
            <div style={{ margin: '1%' }} key={group.id}>
              <strong>{group.description}</strong>
              {answerList(answers.by_group[group.id].answers)}
            </div>
          ))}
        </div> : <div> {answers.all ? answerList(answers.all.answers) : null} </div>}
      </div>
    );
  }

  function PieChartAnswer(answers) {
    return (
      <div>
        {answers.by_group ? <div>
          {groups.map(group => (
            <div style={{ margin: '1%' }} key={group.id}>
              <strong>{group.description}</strong>
              <PieChart question={answers} index={group.id} />
            </div>
          ))}
        </div> : <div> {answers.all ? <PieChart question={answers} index={0} /> : null} </div>}
      </div>
    );
  }

  function getResult() {
    return <>
      <div
        style={{ fontSize: '1.5em', textAlign: 'center', margin: '-1%' }}
      >
        <strong>{surveyName}</strong>
      </div>
      <div
        style={{
          fontSize: '1em',
          textAlign: 'center',
          marginTop: '1.5%',
          marginBottom: '-1%',
        }}
      >
        Submissions: {count}
      </div>
      {/* End Heading */}

      {/* Result */}
      <div style={resultArea}>
        {/* map out the results for each questions */}
        {summary.map((question, i) => {
          let type = question.question.type;
          return (
            <div key={i}>
              {title(i + 1, question.question.title)}
              {type === 'SA' ? shortAnswer(question) : <div></div>}
              {/* TODO: ranking and piecharts(selections+multiple) */}
              {type === 'MC' ? PieChartAnswer(question) : <div></div>}
              {type === 'CB' ? PieChartAnswer(question) : <div></div>}
              {type === 'RK' ? <DataTable question={question} groups={groups} /> : <div></div>}
            </div>
          );
        })}
      </div>
    </>;
  }

  return (
    <div style={{ width: '100%' }}>
      {/* Heading */}
      <IconButton
        style={{
          backgroundColor: '#FFC72C',
          position: 'fix',
          margin: '3% 0 0 5%',
        }}
        onClick={() => {
          navigate('/template');
        }}
      >
        <ArrowBackIcon />
      </IconButton>
      <div>
        {session === false &&
          <div
            style={{ fontSize: '1.5em', textAlign: 'center', margin: '-1%' }}
          >
            <strong>This survey hasn't been released yet.</strong>
          </div>}
        {summary && getResult()}
        {session === null && summary === null &&
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            position: 'fixed',
            top: 0,
            height: '100%',
            width: '100%'
          }}>
            <CircularProgress size={100} />
          </div>}
      </div>
    </div>
  );
}
