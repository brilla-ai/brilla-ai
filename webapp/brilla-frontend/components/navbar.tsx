"use client";
import { useState } from "react";
import translations from "../public/i18n/en.json";
import { Button } from "./ui/button";
import classNames from "classnames";
import { usePathname } from "next/navigation";
import Link from "next/link";
const Navbar = ({ gradientBg = true }) => {
  const [isOpen, setIsOpen] = useState(false);
  const handleTryLive = () => {
    window.location.href = "/live";
  }
  const pathname = usePathname();
  const githubRepo = "https://github.com/brilla-ai/brilla-ai";
  return (
    <nav
      className={classNames(
        gradientBg
          ? "bg-gradient-to-br to-[#ede1fd] via-[#fefaff] from-white"
          : "bg-white",
        "shadow-lg"
      )}
    >
      <div className=" mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex-shrink-0">
            <Link href="/" className="font-bold text-xl text-gray-800">
              {translations["logoText"]}
            </Link>
          </div>
          <div className="hidden md:block">
            <div className="ml-4 flex items-center md:ml-6 gap-4">
              <a
                href="#"
                className="text-gray-800 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                {translations["about"]}
              </a>
              <a
                href={githubRepo} target="_blank"
                className="text-gray-800 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                {translations["github"]}
              </a>
              {/* Hide live button when on live page */}
              {pathname !== "/live" && (
                <Button
                  className="rounded-3xl font-sans font-medium text-sm"
                  onClick={handleTryLive}
                >
                  {translations["trybrillaAiLive"]}
                </Button>
              )}
            </div>
          </div>
          <div className="-mr-2 flex md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-800 hover:text-gray-900 focus:outline-none focus:bg-gray-100 focus:text-gray-900"
            >
              <svg
                className={`${isOpen ? "hidden" : "block"} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
              <svg
                className={`${isOpen ? "block" : "hidden"} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div className={`${isOpen ? "block" : "hidden"} md:hidden`}>
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <a
            href="#"
            className="text-gray-800 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
          >
            {translations["about"]}
          </a>
          <a
            href={githubRepo} target="_blank"
            className="text-gray-800 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
          >
            {translations["github"]}
          </a>
          {/* Hide live button when on live page */}
          {pathname !== "/live" && (
            <Button
              className="rounded-3xl font-sans font-medium text-sm"
              onClick={handleTryLive}
            >
              {translations["trybrillaAiLive"]}
            </Button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
