// components/ShimmerPlaceholder.tsx
import React from "react";

const ShimmerPlaceholder: React.FC = () => {
  return (
    <div className="absolute inset-0 top-0 left-0 w-full h-[47vh] bg-gray-300 animate-pulse"></div>
  );
};

export default ShimmerPlaceholder;