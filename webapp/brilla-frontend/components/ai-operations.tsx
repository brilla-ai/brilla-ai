"use client";
import React, { useState } from "react";
import axios from "axios";
import {
  useStartProcessingAudioQuery,
  useUpdateAiOperationsMutation,
} from "@/hooks/requests/use-start-processing-audio";
import { AIOperationsEventProps } from "@/types";

const AIOperations: React.FC<AIOperationsEventProps> = ({
  lastJsonMessage,
}) => {
  const { refetch: startProcessingAudio } = useStartProcessingAudioQuery();

  const { mutateAsync: updateAiOperations } = useUpdateAiOperationsMutation();
  const [isProcessing, setIsProcessing] = React.useState(false);
  const [stageRound, setStageRound] = React.useState("");
  const [aiOperationsId, setAiOperationsId] = React.useState("");

  const startRound = async (round: string) => {
    try {
      await updateAiOperations({
        id: aiOperationsId,
        data: {
          stage_round: round,
          start_audio_processing: isProcessing,
        },
      });
    } catch (error) {
      console.error("Error starting round:", error);
    }
  };

  const toggleProcessing = async () => {
    try {
      await updateAiOperations({
        id: aiOperationsId,
        data: {
          stage_round: stageRound,
          start_audio_processing: !isProcessing,
        },
      });
      if (!isProcessing) {
        await startProcessingAudio();
      }
      // setIsProcessing(!isProcessing);
    } catch (error) {
      console.error("Error toggling audio processing:", error);
    }
  };

  React.useEffect(() => {
    if (lastJsonMessage) {
      if (lastJsonMessage.ai_operations) {
        console.log(
          "lastJsonMessage",
          lastJsonMessage.ai_operations.stage_round
        );
        setIsProcessing(lastJsonMessage.ai_operations.start_audio_processing);
        setStageRound(lastJsonMessage.ai_operations.stage_round);
        setAiOperationsId(lastJsonMessage.ai_operations.id);
      }

      if (lastJsonMessage.target === "update_ai_operations") {
        const { start_audio_processing, stage_round, id } =
          lastJsonMessage.arguments.data;
        setIsProcessing(start_audio_processing);
        setStageRound(stage_round);
        setAiOperationsId(id);
      }
    }
  }, [lastJsonMessage]);

  return (
    <div className="border border-[#CBD5E1] rounded p-4">
      <h2 className="text-lg font-bold mb-4">AI Operations</h2>
      <div className="flex space-x-4 text-xs">
        <button
          className={`bg-blue-600 hover:bg-blue-700 text-white px-2 py-2 rounded disabled:opacity-50 disabled:cursor-not-allowed ${
            stageRound === "STAGE4" ? "!bg-green-600 hover:bg-green-700" : ""
          }`}
          onClick={() => startRound("STAGE4")}
          disabled={isProcessing}
        >
          {stageRound === "STAGE4" ? "Round 4 Active" : "Start Round 4"}
        </button>
        <button
          className={`bg-blue-600 hover:bg-blue-700 text-white px-2 py-2 rounded disabled:opacity-50 disabled:cursor-not-allowed ${
            stageRound === "STAGE5" ? "!bg-green-600 hover:bg-green-700" : ""
          }`}
          onClick={() => startRound("STAGE5")}
          disabled={isProcessing}
        >
          {stageRound === "STAGE5" ? "Round 5 Active" : "Start Round 5"}
        </button>
        <button
          className={`px-2 py-2 rounded disabled:opacity-50 disabled:cursor-not-allowed ${
            isProcessing
              ? "bg-red-600 hover:bg-red-700"
              : "bg-green-600 hover:bg-green-700"
          } text-white`}
          onClick={toggleProcessing}
          disabled={!stageRound}
        >
          {isProcessing ? "Stop processing audio" : "Start processing audio"}
        </button>
      </div>
    </div>
  );
};

export default AIOperations;
