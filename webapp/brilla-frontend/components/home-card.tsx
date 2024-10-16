import { ReactNode } from "react";

interface CardProps {
  icon: ReactNode;
  title: string;
  description: string;
}

const Card = ({ icon, title, description }: CardProps) => {
  return (
    <div className="bg-white border border-gray-200 shadow-lg rounded-lg p-6 flex flex-col items-center text-center">
      <div className="text-purple-500 mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2 bg-gradient-to-r from-purple-700 via-purple-900 to-indigo-500 inline-block text-transparent bg-clip-text">
        {title}
      </h3>
      <p className="text-gray-700">{description}</p>
    </div>
  );
};

export default Card;
