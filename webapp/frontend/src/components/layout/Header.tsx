import Image from "next/image";
import Link from "next/link";

const navigationPages = [
  {
    name: "Demo",
    href: "/",
  },
  {
    name: "Live",
    href: "/live",
  },
  {
    name: "About",
    href: "/about",
  },
];

const Header = () => {
  return (
    <nav className="bg-grey border-gray-200 max-w-7xl mx-auto mt-4 rounded shadow-md px-6">
      <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <div className="flex items-center space-x-4">
          <Image
            src="/KwameAILogo.png"
            alt="Kwame AI Logo"
            width={20}
            height={20}
          />
          <span className="font-semibold text-xl tracking-tight">
            NSMQ - KWAME AI
          </span>
        </div>

        <button
          data-collapse-toggle="navbar-default"
          type="button"
          className="inline-flex items-center p-2 ml-3 text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
        ></button>
        <div className="hidden w-full md:block md:w-auto" id="navbar-default">
          <ul className="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg  md:flex-row md:space-x-8 md:mt-0 md:border-0  text-black">
            {navigationPages.map((page) => (
              <li key={page.name}>
                <Link
                  href={page.href}
                  className="block py-2 pl-3 pr-4  rounded md:bg-transparent  md:p-0 dark: "
                >
                  {page.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Header;
