"use client";

import { useState } from "react";
import Modal from "@/components/waitlist-modal";
import WaitlistForm from "@/components/waitlist-form";
import Card from "../components/home-card";
import {
  FaMicrophone,
  FaQuestionCircle,
  FaCommentAlt,
  FaVolumeUp,
} from "react-icons/fa";
import Image from "next/image";

export default function HomeBase() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleContributeButton = () => {
    window.open("https://github.com/brilla-ai/brilla-ai", "_blank");
  };

  return (
    <div className="flex flex-col h-full">
      <section className="flex flex-col md:flex-row justify-center md:justify-between p-10 items-center py-12 bg-gradient-to-r from-purple-200 via-purple-300 to-blue-200">
        <div className="md:w-[50%] md:text-start text-center">
          <div className=" text-purple-700 mb-4 space-y-3">
            <p className="md:text-5xl text-2xl font-bold bg-gradient-to-r from-purple-600 via-purple-800 to-indigo-500 inline-block text-transparent bg-clip-text">
              Brilla AI:
            </p>
            <h1 className="md:text-5xl text-3xl font-bold text-[#0C0315]">
              An Educational AI to win Ghana’s NSMQ
            </h1>
          </div>
          <p className="text-lg md:w-[80%] text-gray-700 mb-8">
            We are on the journey to win Ghana NSMQ with an open source AI
            software, looking forward to a better context with our AI software
          </p>
          <div className="flex md:gap-x-4 justify-center gap-3 md:justify-normal mb-6">
            <button
              onClick={handleOpenModal}
              className="bg-gradient-to-r from-blue-800 to-blue-400 text-white md:px-6 md:py-3 px-3 py-2 rounded-full text-sm"
            >
              Join the waitlist
            </button>
            <button onClick={handleContributeButton} className="bg-gray-100 text-black md:px-6 md:py-3 rounded-full px-3 py-2 text-sm">
              Contribute on GitHub
            </button>
          </div>
        </div>
        <div className="md:w-[50%] flex justify-center items-center">
          <Image
            src={`/images/img.png`}
            alt="Brilla AI"
            width={500}
            height={500}
          />
        </div>
      </section>

      <section className="py-12 text-center">
        <h2 className="md:text-5xl text-3xl font-bold  mb-8 bg-gradient-to-r from-purple-600 via-purple-800 to-indigo-500 inline-block text-transparent bg-clip-text ">
          Our Features
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 px-4">
          <Card
            icon={<FaMicrophone size={40} />}
            title="Speech-to-text model"
            description="Transcribes Ghanaian-accented speech of scientific riddles"
          />
          <Card
            icon={<FaQuestionCircle size={40} />}
            title="Question Extraction model"
            description="Extracts relevant portions of the riddles (clues) by inferring the start and end of each riddle and segmenting the clues"
          />
          <Card
            icon={<FaCommentAlt size={40} />}
            title="Question Answering model"
            description="Provides an answer to the riddle"
          />
          <Card
            icon={<FaVolumeUp size={40} />}
            title="Text-to-Speech model"
            description="Says the answer with a Ghanaian accent"
          />
        </div>
      </section>

      <Modal isOpen={isModalOpen} onClose={handleCloseModal}>
        <WaitlistForm />
      </Modal>
    </div>
  );
}
