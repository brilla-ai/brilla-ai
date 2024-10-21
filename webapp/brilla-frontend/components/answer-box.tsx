"use client";
import { useState, useEffect, useRef } from "react";
import CursorSVG from "./icons";
import translation from "../public/i18n/en.json";

const AnswerBox = ({
  lastMessage,
}: {
  lastMessage: MessageEvent<any> | null;
}) => {
  const [displayResponse, setDisplayResponse] = useState("");
  const [completedTyping, setCompletedTyping] = useState(false);
  const [isPulsating, setIsPulsating] = useState(false);
  const lastMessageRef =  useRef<HTMLDivElement>(null);
  const containerRef = useRef(null);

  const [textValue, setTextValue] = useState("");
  const [chat, setChat] = useState("");

  // const { lastMessage, sendJsonMessage, lastJsonMessage } = useWebSocket(
  //   ENV_VARS.WS_BASE_URL || "" // Provide a fallback empty string
  // );

  const handleIconClick = () => {
    const textInput = document?.getElementById(
      "textInput"
    ) as HTMLTextAreaElement; // Cast to HTMLTextAreaElement
    const text = textInput ? textInput.value : ""; // Ensure textInput is not null

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
    if (!chat?.length) {
      return;
    }

    setCompletedTyping(false);

    let i = 0;
    const stringResponse = chat[chat.length - 1];

    const intervalId = setInterval(() => {
      setDisplayResponse(stringResponse.slice(0, i));

      i++;

      if (i > stringResponse.length) {
        clearInterval(intervalId);
        setCompletedTyping(true);
      }
    }, 60);

    return () => clearInterval(intervalId);
  }, [chat]);

  useEffect(() => {
    // Scroll to the last message when typing is completed or when a new message is added
    if (lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({ behavior: "auto" });
    }
  }, [chat, completedTyping]);

  useEffect(() => {
    if (lastMessage) {
      const message = JSON.parse(lastMessage.data);

      if (message.answer_text) {
        console.log("message.answer_text", message.answer_text);
        setTextValue(message.answer_text);
      }

      if (message.extracted_question) {
        setChat(message.extracted_question);
      }

      // if (message.connection_id) {
      //   sendJsonMessage({
      //     type: 1,
      //     target: "add_to_group",
      //     arguments: [message.connection_id, "live_video"],
      //   });
      // }
    }
  }, [lastMessage]);

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
            
              <div
                className="px-2 py-2 mb-2"
              >
                {!completedTyping ? (
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
