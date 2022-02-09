import React from 'react';
import {Routes, Route} from 'react-router-dom';
import StartPage from './components/StartPage';
import StudentLogIn from './components/StudentLogIn';
import AdminLogIn from './components/AdminLogIn';
import AdminTemplate from './components/AdminTemplate';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/"  element={<StartPage/>}/>
        <Route path="/student" element={<StudentLogIn/>}/>
        <Route path="/admin" element={<AdminLogIn/>}/>
        <Route path="/template" element={<AdminTemplate/>}/>
      </Routes>
    </div>
  );
}

export default App;
