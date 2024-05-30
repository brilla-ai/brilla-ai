import React from "react";

const Spinner: React.FC = () => {
  return (
    <div className="flex justify-center items-center h-[28vh] md:h-[65vh] w-full absolute">
      <div className="w-10 h-10 border-3 border-t-4 border-gray-200 border-t-blue-500 rounded-full animate-spin"></div>
    </div>
  );
};

export default Spinner;
