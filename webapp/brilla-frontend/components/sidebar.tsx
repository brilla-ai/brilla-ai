"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  return (
    <div
      className={`flex flex-col h-full ${
        isOpen ? "w-40" : "w-20"
      } transition-width duration-300 bg-gray-100 p-1`}
    >
      <div className="flex flex-col w-full h-full space-y-4 p-2">
        <button
          className="self-start p-2 hidden sm:block"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4 mr-2 text-gray-600"
              viewBox="0 0 24 24"
            >
              <path
                fill="currentColor"
                d="M16.5 14.8V9.2q0-.35-.3-.475t-.55.125L13.2 11.3q-.3.3-.3.7t.3.7l2.45 2.45q.25.25.55.125t.3-.475M5 21q-.825 0-1.412-.587T3 19V5q0-.825.588-1.412T5 3h14q.825 0 1.413.588T21 5v14q0 .825-.587 1.413T19 21zm5-2h9V5h-9z"
              />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w- mr-2 text-gray-600"
              viewBox="0 0 24 24"
            >
              <path
                fill="currentColor"
                d="M7.5 14.8q0 .35.3.475t.55-.125l2.45-2.45q.3-.3.3-.7t-.3-.7L8.35 8.85q-.25-.25-.55-.125t-.3.475zM5 21q-.825 0-1.412-.587T3 19V5q0-.825.588-1.412T5 3h14q.825 0 1.413.588T21 5v14q0 .825-.587 1.413T19 21zm9-2V5H5v14z"
              />
            </svg>
          )}
        </button>
        <Link
          href="/users"
          className={`flex items-center p-1 rounded ${
            pathname === "/users" ? "text-blue-600" : "text-gray-600"
          } hover:bg-gray-100 hover:text-blue-600`}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 mr-2"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M12 12q-1.65 0-2.825-1.175T8 8t1.175-2.825T12 4t2.825 1.175T16 8t-1.175 2.825T12 12m-8 6v-.8q0-.85.438-1.562T5.6 14.55q1.55-.775 3.15-1.162T12 13t3.25.388t3.15 1.162q.725.375 1.163 1.088T20 17.2v.8q0 .825-.587 1.413T18 20H6q-.825 0-1.412-.587T4 18"
            />
          </svg>
          {isOpen && <span>Users</span>}
        </Link>
        <Link
          href="/settings"
          className={`flex items-center p-1 rounded ${
            pathname === "/settings"
              ? "text-blue-600 bg-slate-200"
              : "text-gray-600"
          } hover:bg-gray-100 hover:text-blue-600`}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 mr-2"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="m9.25 22l-.4-3.2q-.325-.125-.612-.3t-.563-.375L4.7 19.375l-2.75-4.75l2.575-1.95Q4.5 12.5 4.5 12.338v-.675q0-.163.025-.338L1.95 9.375l2.75-4.75l2.975 1.25q.275-.2.575-.375t.6-.3l.4-3.2h5.5l.4 3.2q.325.125.613.3t.562.375l2.975-1.25l2.75 4.75l-2.575 1.95q.025.175.025.338v.674q0 .163-.05.338l2.575 1.95l-2.75 4.75l-2.95-1.25q-.275.2-.575.375t-.6.3l-.4 3.2zm2.8-6.5q1.45 0 2.475-1.025T15.55 12t-1.025-2.475T12.05 8.5q-1.475 0-2.488 1.025T8.55 12t1.013 2.475T12.05 15.5"
            />
          </svg>
          {isOpen && <span>Settings</span>}
        </Link>
      </div>
    </div>
  );
};

export default Sidebar;
