import React, { useState } from 'react';
import { FaUserAlt } from "react-icons/fa";
import { Cards } from './Cards';


export default function StudentDashboard() {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [sortDropdownOpen, setSortDropdownOpen] = useState(false);
  const [selectedSort, setSelectedSort] = useState('Sort By');

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  const toggleSortDropdown = () => {
    setSortDropdownOpen(!sortDropdownOpen);
  };

  const handleSortSelect = (sortOption) => {
    setSelectedSort(sortOption);
    setSortDropdownOpen(false);
  };

  const details = {
    name: "Lokesh Kumar",
    roll: "2022BCS0174",
    stream: "CSE"
  };

  return (
    <div className='bg-stone-300 h-full w-full'>
      <div className='flex h-[70px] w-full bg-stone-300 border-black border-2'>
        <div className='text-center w-full'>
          <h2 className='font-bold text-2xl text-center py-5'>DashBoard</h2>
        </div>
        <div className='relative flex items-center '>
          <div 
          onClick={toggleDropdown}
          className='h-10 w-10 rounded-full border-black border-2 flex justify-center items-center mr-5 mt-3'>
            <FaUserAlt className='text-xl'  />
          </div>
          {/* <FaCaretDown className='text-xl cursor-pointer mt-3 ml-1 '  /> */}

          {dropdownOpen && (
            <div className='absolute right-0 mt-[300px] mr-2 bg-white shadow-lg w-56 rounded-lg border z-10 border-gray-300'>
              <div className='p-4 bg-cyan-400 text-white rounded-t-lg'>
                <h3 className='font-bold text-lg'>{details.name}</h3>
                <p className='text-sm'>{details.roll}</p>
                <p className='text-sm'>{details.stream}</p>
              </div>
              <ul className='py-2'>
                <li className='px-4 py-2 hover:bg-gray-100 cursor-pointer border-t border-gray-300'>Profile</li>
                <li className='px-4 py-2 hover:bg-gray-100 cursor-pointer border-t border-gray-300'>Settings</li>
                <li className='px-4 py-2 hover:bg-gray-100 cursor-pointer border-t border-gray-300'>Logout</li>
              </ul>
            </div>
          )}


        </div>
      </div>
      <br />
      <div className='flex flex-col bg-stone-300 gap-4 py-5'>
        <div className='w-full h-10  text-center text-2xl text-red-900 bg-stone-300 flex justify-evenly'>
          <div><b>Go to live transcription</b></div>
          <div><a href='#'><u>click here</u></a></div>
        </div>

       
      </div>
      <Cards/>


    </div>
  );
}
