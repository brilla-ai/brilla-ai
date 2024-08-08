"use client";
import React, { useState } from "react";
import axios from "axios";

const AIOperations: React.FC = () => {
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  const startRound = async (round: number) => {
    try {
        // const response = await axios.post(`/api/start-round-${round}`);
        const response = await axios.post(`https://dummyjson.com/test`);
      console.log(response.data);
    } catch (error) {
      console.error("Error starting round:", error);
    }
  };

  const toggleProcessing = async () => {
    try {
      const endpoint = isProcessing
        ? "stop-processing-audio"
        : "start-processing-audio";
        // const response = await axios.post(`/api/${endpoint}`);
        const response = await axios.post(`https://dummyjson.com/test`);
        console.log(response.data);
      setIsProcessing(!isProcessing);
    } catch (error) {
      console.error("Error toggling audio processing:", error);
    }
  };

  return (
    <div className="border border-[#CBD5E1] rounded p-4">
      <h2 className="text-lg font-bold mb-4">AI Operations</h2>
      <div className="flex space-x-4 text-xs">
        <button
          className="bg-green-600 hover:bg-green-700 text-white px-2 py-2 rounded"
          onClick={() => startRound(4)}
        >
          Start Round 4
        </button>
        <button
          className="bg-green-600 hover:bg-green-700 text-white px-2 py-2 rounded"
          onClick={() => startRound(5)}
        >
          Start Round 5
        </button>
        <button
          className={`px-2 py-2 rounded ${
            isProcessing
              ? "bg-red-600 hover:bg-red-700"
              : "bg-green-600 hover:bg-green-700"
          } text-white`}
          onClick={toggleProcessing}
        >
          {isProcessing ? "Stop processing audio" : "Start processing audio"}
        </button>
      </div>
    </div>
  );
};

export default AIOperations;
