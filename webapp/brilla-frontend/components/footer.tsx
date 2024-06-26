import {
  FontAwesomeIcon,
} from "@fortawesome/react-fontawesome";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

import translation from "../public/i18n/en.json";
import Contributors from "./ui/contributors";
import { Suspense } from "react";
import { socialLinks } from "../mocks/social-links";

const Footer = () => {
  return (
    <footer className="bg-[#0C0315] text-white py-8 absolute bottom-0 w-full px-5 md:px-10 flex  flex-col gap-4 md:flex-row justify-between">
      <div className="  flex flex-col items-start">
        <span className="text-2xl font-medium mb-4">
          {translation["logoText"]}{" "}
        </span>
        <div>{translation["heroText"]}</div>

        <div className="flex gap-6 mt-6">
          {/* Avatar with Socials */}
          {socialLinks.map((social, index) => {
            return (
              <div key={index}>
                {social.link && (
                  <a href={social.link} className="flex items-center">
                    <Avatar className="h-10 w-10  border-2 border-white  item-center">
                      <FontAwesomeIcon
                        icon={social.icon}
                        className="h-7 w-7 m-auto"
                        size="sm"
                      />
                    </Avatar>
                  </a>
                )}
              </div>
            );
          })}
        </div>
      </div>
      <div>
        <p className="text-xl">{translation["resources"]}</p>
        <div>
          <a
            href="https://github.com/brilla-ai/brilla-ai"
            className="text-[#b7b7b7]"
          >
            Demos
          </a>
        </div>
      </div>
      <div>
        <p className="text-xl">{translation["contributors"]}</p>
        <Suspense fallback={<div className="text-white">Loading...</div>}>
          <Contributors />
        </Suspense>
        <p className="mt-4 text-[#b7b7b7]">{translation["copyright"]}</p>
      </div>
    </footer>
  );
};

export default Footer;
