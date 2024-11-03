import React from 'react';

export const Dsp = () => {
  const links = [
    { id: 1, name: 'first', url: 'https://example.com/home' },
    { id: 2, name: 'Second', url: 'https://example.com/about' },
    { id: 3, name: 'Third', url: 'https://example.com/services' },
    { id: 4, name: 'Fourh', url: 'https://example.com/contact' },
    { id: 5, name: 'Fifth', url: 'https://example.com/blog' },
  ];

  return (
    <div className='flex flex-col px-10 py-3 text-blue-600'>
      {links.map(link => (
        <a className='p-3' key={link.id} href={link.url} target="_blank" rel="noopener noreferrer">
          {link.name}
        </a>
      ))}
    </div>
  );
};
