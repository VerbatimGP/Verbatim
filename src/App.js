import Login from './components/Login';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Operation from './components/Operation';
import react from "react";
import './App.css';
import Transcription from './components/Transcription';
import Transcript from './components/Transcript';

const router=createBrowserRouter([
  {path:"/"
    ,
    element:
    <div>
      <Login/>
    </div>
    
  },
  {path:"/Operation"
    ,element:
    <div><Operation/></div>
  }
  ,{
    path:"/Transcription",
    element:<Transcription/>
  },
  {
    path:"/Transcript",
    element:<Transcript/>
  }
]);

function App() {
  return (
    <div className="main">
      <RouterProvider router={router} />
       
        
    </div>
  );
}

export default App;
