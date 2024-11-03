import React from 'react';
import { useNavigate } from 'react-router-dom';

export const Cards = () => {
    const navigate = useNavigate();

    const handleClick1 = () => {
        navigate('/softcomputing');
    };
    const handleClick2 = () => {
        navigate('/Dsp');
    };
    const handleClick3 = () => {
        navigate('/Se');
    };
    const handleClick4 = () => {
        navigate('/Ai');
    };
    const handleClick5 = () => {
        navigate('/Pdc');
    };


    return (
        <div className='w-full h-full mx-auto bg-stone-100 p-5'>
            <div className='grid justify-center items-center p-5 mx-auto'>
                <div className='md:flex md:py-3 md:gap-2'>
                    <button onClick={handleClick1} className='py-2'>
                        <div className='h-[150px] w-[300px] md:w-[500px] bg-gradient-to-r from-stone-900 to-stone-500 text-white'>
                        </div>
                        <p className='text-start px-5'><b>IMA 121 Soft Computing</b></p>
                    </button>

                    <button 
                    onClick={handleClick2}
                    className='py-2'>
                        <div className='h-[150px] w-[300px] md:w-[500px] bg-gradient-to-r from-blue-900 to-blue-400 text-center'>
                        </div>
                        <p className='text-start px-5'><b>IMA 121 Digital Signal Processing</b></p>
                    </button>
                </div>

                <div className='md:flex md:py-3 md:gap-2'>
                    <button 
                    onClick={handleClick5}
                    className='py-2'>
                        <div className='h-[150px] w-[300px] md:w-[500px] bg-gradient-to-r from-red-900 to-red-400 text-center'>
                        </div>
                        <p className='text-start px-5'><b>IMA 121 Parallel and Distributed</b></p>
                    </button>

                    <button 
                    onClick={handleClick3}
                    className='py-2'>
                        <div className='h-[150px] w-[300px] md:w-[500px] bg-gradient-to-r from-yellow-900 to-yellow-400 text-center'>
                        </div>
                        <p className='text-start px-5'><b>IMA 121 Software Engineering</b></p>
                    </button>
                </div>

                <div className='md:flex md:py-3 md:gap-2'>
                    <button 
                    onClick={handleClick4}
                    className='py-2'>
                        <div className='h-[150px] w-[300px] md:w-[500px] bg-gradient-to-r from-lime-900 to-lime-400 text-center'>
                        </div>
                        <p className='text-start px-5'><b>IMA 121 Artificial Intelligence</b></p>
                    </button>

                    <button className='py-2'>
                        <div className='h-[150px] w-[300px] md:w-[500px] bg-gradient-to-r from-emerald-900 to-emerald-400 text-center'>
                        </div>
                        <p className='text-start px-5'><b>IMA 121 Machine Learning</b></p>
                    </button>
                </div>
            </div>
        </div>
    );
};
