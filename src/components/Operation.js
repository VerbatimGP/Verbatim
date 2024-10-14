import React, { useState } from 'react';
import { FaUserAlt } from "react-icons/fa";
import { FaCaretDown } from "react-icons/fa";
import { CiSearch } from "react-icons/ci";
import Transcript from './Transcript';

export default function Operation() {
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
    <div className='bg-blue-200 h-[100vh] w-full'>
      <div className='flex h-[60px] w-full bg-blue-200 border-black border-2'>
        <div className='text-center w-full'>
          <h2 className='font-bold text-2xl text-center py-5'>DashBoard</h2>
        </div>
        <div className='relative flex items-center'>
          <div className='h-10 w-10 rounded-full border-black border-2 flex justify-center items-center mt-3'>
            <FaUserAlt className='text-xl' />
          </div>
          <FaCaretDown className='text-xl cursor-pointer mt-3 ml-1' onClick={toggleDropdown} />

          {dropdownOpen && (
            <div className='absolute right-0 mt-[340px] mr-2 bg-white shadow-lg w-56 rounded-lg border border-gray-300'>
              <div className='p-4 bg-cyan-400 text-white rounded-t-lg'>
                <h3 className='font-bold text-lg'>{details.name}</h3>
                <p className='text-sm'>{details.roll}</p>
                <p className='text-sm'>{details.stream}</p>
              </div>
              <ul className='py-2'>
                <li className='px-4 py-2 hover:bg-gray-100 cursor-pointer border-t border-gray-300'>Profile</li>
                <li className='px-4 py-2 hover:bg-gray-100 cursor-pointer border-t border-gray-300'>Settings</li>
                <li className='px-4 py-2 hover:bg-gray-100 cursor-pointer border-t border-gray-300'>Notifications</li>
                <li className='px-4 py-2 hover:bg-gray-100 cursor-pointer border-t border-gray-300'>Logout</li>
              </ul>
            </div>
          )}
        </div>
      </div>
          <br/>
      <div className='flex flex-col gap-4 '>
        <div className='w-full h-10  text-center text-2xl flex justify-evenly'>
          <div>Go to live transcription</div>
          <div><a href='#'><u>click here</u></a></div>
        </div>

        <div className='w-full bg-blue-200 h-[550px] px-20 flex flex-col '>
          <div className='p-5  bg-blue-200 flex flex-col gap-3 rounded-3xl border-black border-2'>
            <div className='flex justify-between items-center px-10'>
              <div className='h-10 w-10 rounded-full border-2 flex items-center justify-center border-black'><CiSearch /></div>

              
              <div className='relative'>
                <div
                  className='h-10 w-28 rounded-full border-2 border-black flex items-center justify-center cursor-pointer'
                  onClick={toggleSortDropdown}
                >
                  {selectedSort} <FaCaretDown className='ml-2' />
                </div>

                {sortDropdownOpen && (
                  <div className='absolute mt-2 bg-white shadow-lg w-28 rounded-lg border border-gray-300'>
                    <ul className='py-2'>
                      <li className='px-4 py-2 hover:bg-gray-100 cursor-pointer' onClick={() => handleSortSelect('By Date')}> by Date</li>
                      <li className='px-4 py-2 hover:bg-gray-100 cursor-pointer' onClick={() => handleSortSelect('By Subject')}>by Subject</li>
                    </ul>
                  </div>
                )}
              </div>
            </div>

            <div className='border-black border-2 p-2 rounded-lg'>
              <Transcript />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
