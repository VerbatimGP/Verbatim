import { useState } from 'react'
import './App.css'
import Login from './components/Login'
import FacultyDashboard from './components/FacultyDashboard'

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import StudentDashboard from './components/StudentDashboard'
import { Softcomputing } from './components/Softcomputing'
import { Dsp } from './components/Dsp'
import { Ai } from './components/Ai'
import { Pdc } from './components/Pdc'
import { Se } from './components/Se'
function App() {
  return (
    <BrowserRouter>
      <div>
        <Routes>
          <Route path='/' element={<Login/>}/>
          <Route path='/faculty' element={<FacultyDashboard/>}/>
          <Route path='/student' element={<StudentDashboard/>}/>
          <Route path='/softcomputing' element={<Softcomputing/>}/>
          <Route path='/Dsp' element={<Dsp/>}/>
          <Route path='/Se' element={<Se/>}/>
          <Route path='/Ai' element={<Ai/>}/>
          <Route path='/Pdc' element={<Pdc/>}/>
            {/* Add other routes as needed */}
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
