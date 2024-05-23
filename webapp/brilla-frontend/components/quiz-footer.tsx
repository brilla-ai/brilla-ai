"use client";
import translations from "../public/i18n/en.json";

const QuizFooter = () => {
  return (
    <footer className="mx-auto px-4 sm:px6 lg:px-8 w-full bg-white shadow-lg py-6 flex justify-between items-center">
      <div className="flex-shrink-0">
        <a href="#" className="font-bold text-xl text-gray-800">
          {translations["logoText"]}
        </a>
      </div>
      <p>{translations["quizFooterText"]}</p>
    </footer>
  );
};

export default QuizFooter;
