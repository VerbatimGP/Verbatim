import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Corrected import

export default function Login() {
    const [isLogin, setIsLogin] = useState(true);

    function changetrue() {
        setIsLogin(true);
    }
    function changefalse() {
        setIsLogin(false);
    }

    const navigate = useNavigate();

    function gotohandler() {
        navigate('/Operation');
    }

    return (
        <div className="boder">  {/* Corrected class to className */}
            <div className="container">
                <div className="form-container">
                    <div className="form-toggle">
                        <button className={isLogin ? "active" : ""} onClick={changetrue}>Login</button>
                        <button className={!isLogin ? "active" : ""} onClick={changefalse}>Sign Up</button>
                    </div>

                    {isLogin ? (
                        <div className='form'>
                            <h2>Login Form</h2>
                            <input type='email' placeholder='Email' />
                            <input type='password' placeholder='password' />
                            <a href='#'>Forget Password?</a>
                            <button onClick={gotohandler}>Login</button>
                            <p>Not a member? <a href='#' onClick={changefalse}>Sign Up</a></p>
                        </div>
                    ) : (
                        <div className='form'>
                            <h2>Sign Up </h2>
                            <input type='email' placeholder='Email' />
                            <input type='password' placeholder='password' />
                            <input type='password' placeholder='confirm password' />
                            <button onClick={gotohandler}>Sign Up</button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
