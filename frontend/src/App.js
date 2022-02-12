import React from 'react';
import {Routes, Route} from 'react-router-dom';
import StartPage from './components/StartPage';
import StudentLogIn from './components/StudentLogIn';
import AdminLogIn from './components/AdminLogIn';
import SurveyPage from './components/SurveyPage'
import AdminTemplate from './components/AdminTemplate';
import CreateSurvey from './components/CreateSurvey';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/"  element={<StartPage/>}/>
        <Route path="/student" element={<StudentLogIn/>}/>
        <Route path="/admin" element={<AdminLogIn/>}/>
        <Route path="/survey" element={<SurveyPage/>}/>
        <Route path="/admin/create_survey" element={<CreateSurvey/>}/>
        <Route path="/template" element={<AdminTemplate/>}/>
      </Routes>
    </div>
  );
}

export default App;
