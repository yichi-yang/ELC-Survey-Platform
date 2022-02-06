import React from 'react';
import {Routes, Route} from 'react-router-dom';
import StartPage from './components/StartPage';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/"  element={<StartPage/>}/>
      </Routes>
    </div>
  );
}

export default App;
