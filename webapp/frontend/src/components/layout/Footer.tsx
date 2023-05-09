import Image from 'next/image';

import { FaGithub, FaLinkedin } from 'react-icons/fa';

const Footer = () => {
  return (
    <div className='flex justify-between items-center p-4 bg-grey text-gray-600 mb-4 px-10'>
      <div className='flex items-center space-x-4'>
        <Image
          src='/KwameAILogo.png'
          alt='Kwame AI Logo'
          width={20}
          height={20}
        />

        <span className='tracking-tight'>NSMQ - KWAME AI</span>
      </div>
      <div className='flex items-center space-x-4'>
        <span className='tracking-tight underline'>Privacy Policy</span>
        <span>|</span>
        <span className='tracking-tight underline'>Terms of Use</span>
      </div>

      <div className='flex items-center space-x-4'>
        <a href='' className='text-gray-600 hover:text-gray-800 '>
          <FaGithub />
        </a>
        <a href='' className='text-gray-600 hover:text-gray-800 '>
          <FaLinkedin />
        </a>
      </div>
    </div>
  );
};

export default Footer;
