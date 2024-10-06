"use client";
import { useState, useEffect, useRef } from "react";
import CursorSVG from "./icons";
import translation from "../public/i18n/en.json";

interface ChatContainerProps {
  chatHistory: string[]; // Change the type to an array of strings
}

const AnswerBox = ({ chatHistory }: ChatContainerProps) => {
  const [displayResponse, setDisplayResponse] = useState("");
  const [completedTyping, setCompletedTyping] = useState(false);
  const [isPulsating, setIsPulsating] = useState(false);
  const lastMessageRef =  useRef<HTMLDivElement>(null);
  const containerRef = useRef(null);

  const [textValue, setTextValue] = useState('Rigid Body');

  const handleIconClick = () => {
    // Access the value of the textarea
    
    const text = (document?.getElementById('textInput') as HTMLInputElement)?.value || '';

    // Use the Web Speech API for text-to-speech
    const speech = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(speech);

    setIsPulsating(true);

    // Remove pulsating effect after speech ends
    speech.onend = () => {
      setIsPulsating(false);
    };
  }

  useEffect(() => {
    if (!chatHistory?.length) {
      return;
    }

    setCompletedTyping(false);

    let i = 0;
    const stringResponse = chatHistory[chatHistory.length - 1];

    const intervalId = setInterval(() => {
      setDisplayResponse(stringResponse.slice(0, i));

      i++;

      if (i > stringResponse.length) {
        clearInterval(intervalId);
        setCompletedTyping(true);
      }
    }, 60);

    return () => clearInterval(intervalId);
  }, [chatHistory]);

  useEffect(() => {
    // Scroll to the last message when typing is completed or when a new message is added
    if (lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({ behavior: "auto" });
    }
  }, [chatHistory, completedTyping]);

  return (
    <div className="flex flex-col h-full relative no-scrollbar">
      <div className="max-w-lg  ">
        <div
          ref={containerRef}
          className="shadow-xl rounded-lg flex flex-col m-6 border-2 border-slate-300 h-[47vh]"
        >
       
          {!completedTyping ? (
            <div className="w-4 h-4 bg-blue-600 rounded-full border-violet-100 border-2 ml-2 m-3 animate-pulse-custom"></div>
            
          ) : (
            <div className="w-3 h-3 bg-blue-400 rounded-full border-blue-200 ml-2 mt-3"></div>
          )}
          <div className="overflow-y-auto h-[40vh] no-scrollbar">
            {chatHistory.map((chat, index) => (
              <div
                key={index}
                ref={index === chatHistory.length - 1 ? lastMessageRef : null}
                className="px-2 py-2 mb-2"
              >
                {index === chatHistory.length - 1 && !completedTyping ? (
                  <div className="flex justify-start">
                    <span className="chat-bubble bg-gradient-to-r from-blue-400 to-violet-400 text-white rounded-lg p-2 whitespace-normal">
                      {displayResponse}
                      {!completedTyping && <CursorSVG />}
                    </span>
                  </div>
                ) : (
                  <div className="flex justify-start">
                    <div className="chat-bubble-other bg-gradient-to-r from-gray-300 to-gray-200 text-gray-800 rounded-lg p-2 whitespace-normal">
                      {chat}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="mx-6 shadow-lg flex flex-col border-2 border-white bg-white rounded-lg px-3 py-1 md:mt-2 order-first md:order-last mt-4">
      <div className="flex items-center flex-1 justify-center">
        <span
          className="h-12 w-12 flex items-center justify-center bg-[#F1F5F9] text-white rounded-md self-center shadow border-2 border-[#E2E8F0] cursor-pointer ${isPulsating ? 'pulsate' : 'bg-[#F1F5F9]'}`"
          onClick={handleIconClick}
          style={{
            borderColor: isPulsating ? 'rgba(255, 0, 0, 0.5)' : '#E2E8F0',
            transition: 'border-color 0.5s',
            animation: isPulsating ? 'pulsate 1s infinite' : 'none'
          }}
          
        >
          🔊
        </span>
        <div className="flex flex-col ml-2 flex-1 items-center">
          <textarea
            className="px-4 py-2 overflow-auto bg-white font-bold text-[#0F172A] text-xl rounded-md border-2 w-full border-[#F1F5F9] focus:ring-violet-400 outline-none resize-none"
            id="textInput"
            readOnly
            value={textValue}
            wrap="soft"
            rows={1}
          />
        </div>
      </div>
      <span className="text-sm text-[#D4DCEF] font-sans font-semibold self-end">
        {translation["answerText"]}
      </span>
    </div>
    

      
    </div>
  );


};


export default AnswerBox;
