import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTwitter, faFacebook, faInstagram } from '@fortawesome/free-brands-svg-icons';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

import translation from "../public/i18n/en.json";

const Footer = () => {
  return (
    <footer className="bg-[#0C0315] text-white py-8 absolute bottom-0 w-full">
      <div className="mx-10  flex flex-col items-start">
        <span className='text-2xl font-medium mb-4'>{translation["logoText"]} </span>
        <div>{translation["heroText"]}</div>

        <div className="flex gap-6 mt-6">
      {/* Avatar with Twitter */}
      <div className="flex items-center">
      <Avatar className='h-10 w-10  border-2 border-white  item-center' >
            <FontAwesomeIcon icon={faTwitter}  className="h-7 w-7 m-auto" size="sm" />
        </Avatar>     
      </div>

      {/* Avatar with Facebook */}
      
      <div className="flex items-center">
      <Avatar className='h-10 w-10 border-2 border-white  item-center  '>
      <FontAwesomeIcon icon={faFacebook} className="h-7 w-7 m-auto" size="sm" />
        </Avatar>  
      </div>

      {/* Avatar with Instagram */}
      <div className="flex items-center">
      <Avatar className='h-10 w-10  border-2 border-white  item-center' >
      <FontAwesomeIcon icon={faInstagram} className="h-7 w-7 m-auto" size="sm" />
        </Avatar>  
       
      </div>
    </div>
    <hr className="w-full mt-12 border-1 border-[#39373A] "/>


        </div>
    </footer>
  );
};

export default Footer;
