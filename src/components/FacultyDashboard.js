import React, { useState } from 'react';
import { FaUserAlt } from "react-icons/fa";
import { Cards } from './Cards';

export default function Dashboard() {
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        topic: ''
    });

    const toggleDropdown = () => {
        setDropdownOpen(!dropdownOpen);
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const handleStartClick = () => {
        setIsFormOpen(true);
    };

    const handleFormSubmit = (e) => {
        e.preventDefault();
        console.log(formData);
        setIsFormOpen(false); // Close the form after submission
    };

    const details = {
        name: "Dakshayani",
        roll: "2022BCS0174",
        stream: "CSE"
    };

    return (
        <div>
            <div className='bg-stone-300 h-full w-full'>
                <div className='flex h-[70px] w-full bg-stone-200 border-black border-2'>
                    <div className='text-center w-full'>
                        <h2 className='font-bold text-2xl text-center py-5'>Dashboard</h2>
                    </div>
                    <div className='relative flex items-center '>
                        <div onClick={toggleDropdown} className='h-10 w-10 rounded-full border-black border-2 flex justify-center items-center mr-5 mt-3'>
                            <FaUserAlt className='text-xl' />
                        </div>

                        {dropdownOpen && (
                            <div className='absolute right-0 mt-[250px] mr-2 bg-white shadow-lg w-56 rounded-lg border z-10 border-gray-300'>
                                <div className='p-2 bg-cyan-400 text-white rounded-t-lg'>
                                    <h3 className='font-bold text-lg'>{details.name}</h3>
                                    <p className='text-sm'>{details.roll}</p>
                                    <p className='text-sm'>{details.stream}</p>
                                </div>
                                <ul className='py-2'>
                                    <li className='px-4 py-2 hover:bg-gray-100 cursor-pointer border-t border-gray-300'>Settings</li>
                                    <li className='px-4 py-2 hover:bg-gray-100 cursor-pointer border-t border-gray-300'>Logout</li>
                                </ul>
                            </div>
                        )}
                    </div>
                </div>

                <div className='justify-center items-center py-10 bg-stone-200 mx-auto'>
                    <div className='flex gap-8 justify-center text-xl'>
                        <button onClick={handleStartClick} className='bg-blue-700 p-3 rounded-xl text-white'>Start</button>
                        <button className='bg-blue-700 p-3 rounded-xl text-white'>Pause</button>
                    </div>
                </div>

                {isFormOpen && (
                    <div className='flex justify-center items-center py-5 bg-stone-200 '>
                        <form onSubmit={handleFormSubmit} className='bg-white w-[300px]  p-5 shadow-md rounded'>
                            <h3 className='text-xl font-bold mb-4'>Enter Details</h3>
                            <div className='mb-3'>
                                <label className='block font-medium mb-1'>Course Code</label>
                                <input
                                    type='text'
                                    name='name'
                                    value={formData.name}
                                    onChange={handleInputChange}
                                    className='border border-gray-300 rounded p-2 w-full'
                                    required
                                />
                            </div>
                            <div className='mb-3'>
                                <label className='block font-medium mb-1'>Topic</label>
                                <input
                                    type='text'
                                    name='topic'
                                    value={formData.topic}
                                    onChange={handleInputChange}
                                    className='border border-gray-300 rounded p-2 w-full'
                                    required
                                />
                            </div>
                            <button type='submit' className='bg-blue-500 text-white px-4 py-2 rounded'>
                                Submit
                            </button>
                        </form>
                    </div>
                )}

                <div className='bg-stone-300 h-full w-full'>
                    <div className='flex flex-col bg-stone-200'>
                        <div className='w-full text-center sm:text-2xl flex text-red-900 py-6 justify-evenly'>
                            <div><b>Go to live transcription</b></div>
                            <div><a href='#'><u>click here</u></a></div>
                        </div>
                    </div>
                </div>
            </div>
            <Cards />
        </div>
    );
}
