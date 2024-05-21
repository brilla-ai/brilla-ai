import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faTwitter,
  faGithub,
  faLinkedin,
  faDiscord,
} from "@fortawesome/free-brands-svg-icons";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

import translation from "../public/i18n/en.json";

const Footer = () => {
  return (
    <footer className="bg-[#0C0315] text-white py-2 absolute bottom-0 w-full">
      <div className="flex mx-6 items-center justify-center border-b-2 border-neutral-200 py-2 dark:border-neutral-500 lg:justify-between">
        <div className="mr-4 lg:block">
          <span className="text-2xl font-medium mb-4">
            {translation["logoText"]}{" "}
          </span>
        </div>
        {/* <!-- Social network icons container --> */}
        <div className="flex justify-center gap-4">
          {/* Avatar with Github */}
          <div className="flex items-center">
            <Avatar className="h-6 w-6  item-center">
              <FontAwesomeIcon
                icon={faGithub}
                className="h-5 w-5 m-auto"
                size="sm"
              />
            </Avatar>
          </div>

          {/* Avatar with LinkedIn */}
          <div className="flex items-center">
            <Avatar className="h-6 w-6 item-center  ">
              <FontAwesomeIcon
                icon={faLinkedin}
                className="h-5 w-5 m-auto"
                size="sm"
              />
            </Avatar>
          </div>

          {/* Avatar with Discord */}
          <div className="flex items-center">
            <Avatar className="h-6 w-6 item-center">
              <FontAwesomeIcon
                icon={faDiscord}
                className="h-5 w-5 m-auto"
                size="sm"
              />
            </Avatar>
          </div>
        </div>
      </div>

      <div className="mx-6 py-2 text-center md:text-left">
        <div className="grid-1 grid md:gap-10 md:grid-cols-2 lg:grid-cols-2">
          <div className="">
            <h6 className="mb-4 flex items-center justify-center md:justify-start">
              <div>{translation["heroText"]}</div>{" "}
            </h6>
          </div>
          <div className="flex justify-center lg:justify-end gap-10">
            {" "}
            {/* <!-- Resources section --> */}
            <div className="">
              <h6 className="mb-2 flex justify-center font-semibold uppercase md:justify-start">
                Resources
              </h6>
              <p className="mb-2">
                <a className="text-neutral-600 dark:text-neutral-200">Demos</a>
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* <!--Copyright section--> */}
      <div className="bg-[#0C0315] border-neutral-20 text-white px-4 py-1 text-center">
        <span>© {new Date().getFullYear()} Copyright: </span>
        <a
          className="font-semibold text-neutral-600 dark:text-neutral-400"
          href=""
        >
          BrillaAI
        </a>
      </div>
    </footer>
  );
};

export default Footer;
