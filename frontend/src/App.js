import React from 'react';
import {Routes, Route} from 'react-router-dom';
import StartPage from './components/StartPage';
import StudentLogIn from './components/StudentLogIn';
import AdminLogIn from './components/AdminLogIn';
import SurveyPage from './components/SurveyPage';
import {AdminTemplate} from './components/AdminTemplate';
import CreateSurvey from './components/CreateSurvey';
import FormReleased from './components/FormReleased';
import SurveyResult from './components/SurveyResult';
import ConfirmationPage from './components/SurveyPage/confirmation';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/"  element={<StartPage/>}/>
        <Route path="/student" element={<StudentLogIn/>}/>
        <Route path="/admin" element={<AdminLogIn/>}/>
        <Route path="/survey/:sessionID" element={<SurveyPage/>}/>
        <Route path="/admin/create_survey/:updateID" element={<CreateSurvey/>}/>
        <Route path="/template" element={<AdminTemplate/>}/>
        <Route path="/released/:id" element={<FormReleased/>}/>
        <Route path="/result/:surveyID/:sessionID" element={<SurveyResult/>}/>
        <Route path="/confirmation" element={<ConfirmationPage/>}/>
      </Routes>
    </div>
  );
}

export default App;
